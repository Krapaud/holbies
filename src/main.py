from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import traceback
import io

from app.database import engine, get_db
from app.models import Base
from app.routers import auth, quiz, users, ai_quiz
from app.routers import performance
from app.auth import get_current_user
from sqlalchemy.orm import Session

# Charger les variables d'environnement
load_dotenv()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Holbies Learning Hub",
    description="Système de quiz interactif avec thème Matrix",
    version="1.0.0"
)

# Ajouter le middleware de session
app.add_middleware(SessionMiddleware, secret_key="holbies-learning-hub-secret-key-2025")

# Montage des fichiers statiques
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Nouvelle route pour servir les fichiers statiques
@app.get("/files/{filename:path}")
async def serve_static_files(filename: str):
    file_path = Path("src/static") / filename
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

# Templates
templates = Jinja2Templates(directory="src/templates")

# Helper function pour le contexte des templates
def get_template_context(request: Request, **kwargs):
    """Ajoute le contexte de session à tous les templates"""
    context = {
        "request": request,
        "session": request.session,
        "user_id": request.session.get("user_id"),
        "username": request.session.get("username"),
        "is_authenticated": bool(request.session.get("user_id")),
        "url_for_static": lambda p: f"/files{p}", # Nouvelle fonction pour les URLs statiques
        **kwargs
    }
    return context


# Inclusion des routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(ai_quiz.router, prefix="/api/ai-quiz", tags=["ai-quiz"])
app.include_router(performance.router, prefix="/api/performance", tags=["performance"])

# Route directe pour les stats du site (pour compatibilité frontend)
from app.routers.quiz import get_site_stats
@app.get("/quiz/stats")
def public_site_stats(request: Request, db=Depends(get_db)):
    return get_site_stats(db)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", get_template_context(request))

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", get_template_context(request))

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", get_template_context(request))

# Dépendance pour vérifier si l'utilisateur est connecté
async def login_required(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    return request



@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    await login_required(request)
    return templates.TemplateResponse("quiz.html", get_template_context(request))

@app.get("/learning", response_class=HTMLResponse)
async def learning_page(request: Request):
    await login_required(request)
    return templates.TemplateResponse("learning.html", get_template_context(request))

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    await login_required(request)
    return templates.TemplateResponse("dashboard.html", get_template_context(request))

@app.get("/ai-quiz", response_class=HTMLResponse)
async def ai_quiz_page(request: Request):
    await login_required(request)
    return templates.TemplateResponse("ai-quiz.html", get_template_context(request))

@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect(request: Request):
    """Redirection vers le dashboard admin"""
    return RedirectResponse(url="/api/users/admin/dashboard", status_code=302)

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, db: Session = Depends(get_db)):
    """Page de profil utilisateur"""
    try:
        # Récupérer l'utilisateur depuis la session uniquement
        user_id = request.session.get("user_id")
        
        if not user_id:
            # Pas d'utilisateur en session, rediriger vers login
            return RedirectResponse(url="/login", status_code=302)
        
        # Récupérer l'utilisateur depuis la base de données
        from app.models import User
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            # Utilisateur introuvable, nettoyer la session et rediriger
            request.session.clear()
            return RedirectResponse(url="/login", status_code=302)
        
        context = get_template_context(request, user=user)
        return templates.TemplateResponse("profile.html", context)
        
    except Exception as e:
        # En cas d'erreur, nettoyer la session et rediriger vers login
        print(f"Erreur profile: {e}")  # Pour debug
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect(request: Request):
    """Redirection vers le dashboard admin"""
    return RedirectResponse(url="/api/users/admin/dashboard", status_code=302)

@app.post("/api/visualize")
async def visualize_code(request: Request):
    data = await request.json()
    code = data.get("code", "")
    trace = []
    output = io.StringIO()
    def tracer(frame, event, arg):
        if event == "line":
            trace.append({
                "lineno": frame.f_lineno,
                "locals": frame.f_locals.copy(),
            })
        return tracer
    try:
        compiled = compile(code, "<user_code>", "exec")
        sys.settrace(tracer)
        exec(compiled, {})
        sys.settrace(None)
        error = None
    except Exception as e:
        sys.settrace(None)
        error = traceback.format_exc()
    finally:
        sys.settrace(None)
    return JSONResponse({"trace": trace, "error": error, "output": output.getvalue()})

# Routes d'authentification
@app.post("/auth/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Route de connexion avec session"""
    from app.auth import authenticate_user
    from app.models import User
    
    # Authentifier l'utilisateur
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect"
        )
    
    # Créer la session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["email"] = user.email
    request.session["is_admin"] = user.is_admin
    
    # Rediriger vers dashboard
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/logout")
async def logout(request: Request):
    """Route pour se déconnecter"""
    # Vider la session
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)

@app.get("/debug-session")
async def debug_session(request: Request, db: Session = Depends(get_db)):
    """Page de debug pour voir les informations de session"""
    from app.models import User
    
    session_info = {
        "session_data": dict(request.session),
        "user_from_session": None
    }
    
    user_id = request.session.get("user_id")
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            session_info["user_from_session"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
    
    return JSONResponse(session_info)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )

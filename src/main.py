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
from app.models import Base, PLDCategory, PLDTheme, PLDQuestion, User, QuizSession, AIQuizSession
from app.routers import auth, quiz, users, ai_quiz, pld_admin, pld
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
app.include_router(pld.router, prefix="/api", tags=["pld-public"])  # Nouveau router PLD public
app.include_router(ai_quiz.router, prefix="/api/pld", tags=["pld"])
app.include_router(pld_admin.router, prefix="/api/pld", tags=["pld-admin"])
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
async def dashboard_redirect(request: Request):
    """Redirection vers le profil utilisateur"""
    return RedirectResponse(url="/profile", status_code=302)

@app.get("/pld", response_class=HTMLResponse)
async def pld_page(request: Request):
    await login_required(request)
    
    # Récupérer les catégories PLD avec le nombre de questions par catégorie
    db = next(get_db())
    try:
        categories_data = []
        categories = db.query(PLDCategory).order_by(PLDCategory.name).all()
        
        for category in categories:
            # Compter le nombre total de questions dans cette catégorie
            question_count = db.query(PLDQuestion).join(PLDTheme).filter(
                PLDTheme.category_id == category.id
            ).count()
            
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'question_count': question_count
            })
    finally:
        db.close()
    
    context = get_template_context(request)
    context['categories'] = categories_data
    return templates.TemplateResponse("pld.html", context)

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
        from app.models import User, QuizSession, AIQuizSession
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            # Utilisateur introuvable, nettoyer la session et rediriger
            request.session.clear()
            return RedirectResponse(url="/login", status_code=302)
        
        # Calculer les statistiques réelles
        # Quiz complétés
        completed_quiz_sessions = db.query(QuizSession).filter(
            QuizSession.user_id == user_id,
            QuizSession.completed == True
        ).count()
        
        completed_ai_quiz_sessions = db.query(AIQuizSession).filter(
            AIQuizSession.user_id == user_id,
            AIQuizSession.completed == True
        ).count()
        
        total_quiz_completed = completed_quiz_sessions + completed_ai_quiz_sessions
        
        # Score moyen
        all_sessions = db.query(QuizSession).filter(
            QuizSession.user_id == user_id,
            QuizSession.completed == True,
            QuizSession.total_questions > 0
        ).all()
        
        ai_sessions = db.query(AIQuizSession).filter(
            AIQuizSession.user_id == user_id,
            AIQuizSession.completed == True,
            AIQuizSession.total_questions > 0
        ).all()
        
        all_scores = []
        for session in all_sessions:
            score_percentage = (session.score / session.total_questions) * 100
            all_scores.append(score_percentage)
            
        for session in ai_sessions:
            score_percentage = (session.total_score / session.total_questions) * 100
            all_scores.append(score_percentage)
        
        average_score = round(sum(all_scores) / len(all_scores)) if all_scores else 0
        
        # Série actuelle (nombre de quiz complétés cette semaine)
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        
        current_streak = db.query(QuizSession).filter(
            QuizSession.user_id == user_id,
            QuizSession.completed == True,
            QuizSession.completed_at >= week_ago
        ).count()
        
        current_streak += db.query(AIQuizSession).filter(
            AIQuizSession.user_id == user_id,
            AIQuizSession.completed == True,
            AIQuizSession.completed_at >= week_ago
        ).count()
        
        # Ajouter les statistiques au contexte
        context = get_template_context(request, user=user)
        context.update({
            'total_quiz_completed': total_quiz_completed,
            'average_score': average_score,
            'current_streak': current_streak
        })
        
        return templates.TemplateResponse("profile.html", context)
        
    except Exception as e:
        # En cas d'erreur, nettoyer la session et rediriger vers login
        print(f"Erreur profile: {e}")  # Pour debug
        request.session.clear()
        return RedirectResponse(url="/login", status_code=302)

@app.get("/coding-lab-home", response_class=HTMLResponse)
async def coding_lab_home(request: Request):
    """Page d'accueil du Coding Lab - Présentation des fonctionnalités"""
    context = get_template_context(request)
    return templates.TemplateResponse("coding-lab-home.html", context)

@app.get("/coding-lab", response_class=HTMLResponse)
async def coding_lab(request: Request, db: Session = Depends(get_db)):
    """Page Coding Lab - Apprentissage interactif comme Coddy.tech"""
    try:
        # Vérifier l'authentification
        user_id = request.session.get("user_id")
        if not user_id:
            return RedirectResponse(url="/login", status_code=302)
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            request.session.clear()
            return RedirectResponse(url="/login", status_code=302)
        
        context = get_template_context(request, user=user)
        return templates.TemplateResponse("coding-lab.html", context)
        
    except Exception as e:
        print(f"Erreur coding-lab: {e}")
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

@app.post("/api/coding-lab/save-progress")
async def save_coding_lab_progress(request: Request, db: Session = Depends(get_db)):
    """Sauvegarder la progression du Coding Lab"""
    try:
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Non authentifié")
        
        data = await request.json()
        
        # Ici vous pourriez sauvegarder en base de données
        # Pour cette démo, on retourne juste un succès
        
        return {
            "success": True,
            "message": "Progression sauvegardée",
            "data": {
                "user_id": user_id,
                "progress": data
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/api/coding-lab/progress")
async def get_coding_lab_progress(request: Request, db: Session = Depends(get_db)):
    """Récupérer la progression du Coding Lab"""
    try:
        user_id = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Non authentifié")
        
        # Ici vous pourriez récupérer depuis la base de données
        # Pour cette démo, on retourne une progression fictive
        
        return {
            "success": True,
            "data": {
                "completedExercises": [1],
                "points": 50,
                "streak": 1,
                "level": 1,
                "achievements": []
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/api/coding-lab/run-code")
async def run_coding_lab_code(request: Request):
    """Exécuter du code dans le Coding Lab"""
    try:
        data = await request.json()
        code = data.get("code", "")
        language = data.get("language", "python")
        
        # Simulation d'exécution de code
        if language == "python":
            # Ici vous pourriez utiliser un vrai interpréteur Python sécurisé
            if "print" in code and "Hello" in code:
                return {
                    "success": True,
                    "output": "Hello, World!\n",
                    "error": None
                }
            else:
                return {
                    "success": True,
                    "output": "Code exécuté avec succès\n",
                    "error": None
                }
        
        return {
            "success": False,
            "output": "",
            "error": f"Langage {language} non supporté"
        }
        
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }

@app.post("/api/sync-session")
async def sync_session(request: Request, db: Session = Depends(get_db)):
    """Synchronise la session utilisateur côté serveur"""
    try:
        # Récupérer les données de la requête
        data = await request.json()
        user_id = data.get("user_id")
        username = data.get("username")
        
        if not user_id:
            return JSONResponse({"error": "user_id manquant"}, status_code=400)
        
        # Vérifier que l'utilisateur existe en base
        from app.models import User
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return JSONResponse({"error": "Utilisateur introuvable"}, status_code=404)
        
        # Synchroniser la session
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        request.session["email"] = user.email
        request.session["is_admin"] = user.is_admin
        
        return JSONResponse({
            "success": True,
            "message": "Session synchronisée",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin
            }
        })
        
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

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
    
    # Rediriger vers profil
    return RedirectResponse(url="/profile", status_code=302)

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

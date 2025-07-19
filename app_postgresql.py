"""
Dev Learning Hub Matrix - FastAPI avec PostgreSQL
Version sécurisée avec bcrypt et SQLAlchemy
"""

import os
import bcrypt
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Annotated
from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Imports locaux
from database import get_db, User, QuizScore, UserSession, TutorHistory
from quiz_data import questions, answers, categories
from tutor_engine import TutorEngine

# Charger les variables d'environnement
load_dotenv()

# Initialisation FastAPI
app = FastAPI(
    title="Dev Learning Hub Matrix - PostgreSQL Edition",
    description="Plateforme d'apprentissage sécurisée avec PostgreSQL et bcrypt",
    version="3.0.0"
)

# Configuration des templates et fichiers statiques avec chemin absolu
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Initialiser le moteur de tuteur
tutor_engine = TutorEngine()

# Configuration sécurisée
SECRET_KEY = os.getenv("SECRET_KEY", "matrix_dev_hub_super_secret_key_2025")
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
SESSION_LIFETIME = int(os.getenv("SESSION_LIFETIME", "86400"))  # 24h

# Models Pydantic
class UserLogin(BaseModel):
    username: str
    password: str

class TutorRequest(BaseModel):
    code: str
    language: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

# Fonctions utilitaires sécurisées
def hash_password(password: str) -> str:
    """Hasher un mot de passe avec bcrypt"""
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Vérifier un mot de passe avec bcrypt"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_session(user_id: int, request: Request, db: Session) -> str:
    """Créer une session sécurisée en base de données"""
    session_id = hashlib.sha256(f"{user_id}{datetime.now()}{SECRET_KEY}".encode()).hexdigest()
    expires_at = datetime.now() + timedelta(seconds=SESSION_LIFETIME)
    
    # Supprimer les anciennes sessions de cet utilisateur
    db.query(UserSession).filter(UserSession.user_id == user_id).delete()
    
    # Créer la nouvelle session
    session = UserSession(
        id=session_id,
        user_id=user_id,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    db.add(session)
    db.commit()
    
    return session_id

def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Récupère l'utilisateur actuel depuis la session PostgreSQL"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    # Vérifier la session en base
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.expires_at > datetime.now()
    ).first()
    
    if session:
        return session.user
    return None

def require_auth(request: Request, db: Session = Depends(get_db)) -> User:
    """Dépendance pour vérifier l'authentification"""
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Connexion requise")
    return user

def require_admin(request: Request, db: Session = Depends(get_db)) -> User:
    """Dépendance pour vérifier les privilèges admin"""
    user = require_auth(request, db)
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Privilèges administrateur requis")
    return user

# Routes principales
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Page d'accueil"""
    user = get_current_user(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """Page de connexion"""
    user = get_current_user(request, db)
    return templates.TemplateResponse("login.html", {"request": request, "user": user})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Traiter la connexion avec bcrypt"""
    user = db.query(User).filter(User.username == username).first()
    
    if user and verify_password(password, user.password_hash):
        # Mettre à jour la dernière connexion
        user.last_login = datetime.now()
        db.commit()
        
        # Créer une session sécurisée
        session_id = create_session(user.id, request, db)
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_id", value=session_id, httponly=True, secure=False, samesite="lax")
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Nom d'utilisateur ou mot de passe incorrect",
            "user": None
        })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    """Page d'inscription"""
    user = get_current_user(request, db)
    return templates.TemplateResponse("register.html", {"request": request, "user": user})

@app.post("/register")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Traiter l'inscription avec bcrypt"""
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Nom d'utilisateur ou email déjà utilisé",
            "user": None
        })
    
    # Créer le nouvel utilisateur avec bcrypt
    password_hash = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Créer une session et rediriger
    session_id = create_session(new_user.id, request, db)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_id", value=session_id, httponly=True, secure=False, samesite="lax")
    return response

@app.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """Déconnexion sécurisée"""
    session_id = request.cookies.get("session_id")
    if session_id:
        # Supprimer la session de la base de données
        db.query(UserSession).filter(UserSession.id == session_id).delete()
        db.commit()
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="session_id")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(require_auth)):
    """Tableau de bord utilisateur"""
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/python-tutor", response_class=HTMLResponse)
async def python_tutor(request: Request, user: User = Depends(require_auth)):
    """Page DLH Tutor - Visualiseur de code multi-langages"""
    return templates.TemplateResponse("python_tutor.html", {"request": request, "user": user})

@app.post("/api/tutor/run")
async def tutor_run(request: Request, tutor_request: TutorRequest, user: User = Depends(require_auth), db: Session = Depends(get_db)):
    """API intégrée pour le DLH Tutor avec historique"""
    try:
        result = tutor_engine.execute_code(tutor_request.code, tutor_request.language)
        
        # Sauvegarder dans l'historique
        history = TutorHistory(
            user_id=user.id,
            language=tutor_request.language,
            code=tutor_request.code,
            result=str(result),
            execution_time=result.get('execution_time', 'N/A') if isinstance(result, dict) else 'N/A'
        )
        db.add(history)
        db.commit()
        
        return result
    except Exception as e:
        return {"error": str(e), "output": "", "execution_time": "0ms"}

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_home(request: Request, user: User = Depends(require_auth)):
    """Page d'accueil des quiz"""
    return templates.TemplateResponse("quiz_home.html", {
        "request": request, 
        "user": user, 
        "categories": categories
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, user: User = Depends(require_admin)):
    """Page d'administration"""
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "user": user
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user: User = Depends(require_auth)):
    """Page de profil utilisateur"""
    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user
    })

# Route pour nettoyer les sessions expirées (tâche de maintenance)
@app.get("/admin/cleanup-sessions")
async def cleanup_sessions(user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Nettoyer les sessions expirées"""
    deleted = db.query(UserSession).filter(UserSession.expires_at < datetime.now()).delete()
    db.commit()
    return {"message": f"{deleted} sessions expirées supprimées"}

# Route de démonstration du menu utilisateur
@app.get("/demo/menu", response_class=HTMLResponse)
async def demo_menu():
    """Page de démonstration du menu utilisateur avec instructions"""
    with open("demo_menu.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_postgresql:app", 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", "5001")), 
        reload=bool(os.getenv("DEBUG", "true").lower() == "true")
    )

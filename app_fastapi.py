import os
import sqlite3
import hashlib
import random
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from quiz_data import questions, answers, categories
from tutor_engine import TutorEngine

# Initialisation FastAPI
app = FastAPI(
    title="Dev Learning Hub Matrix",
    description="Plateforme d'apprentissage avec thème Matrix",
    version="2.0.0"
)

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialiser le moteur de tuteur
tutor_engine = TutorEngine()

# Configuration de la base de données
DATABASE = 'users.db'

# Models Pydantic
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class TutorRequest(BaseModel):
    code: str
    language: str

class QuizSubmission(BaseModel):
    answers: dict

# Session management (simple in-memory for now)
active_sessions = {}

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_current_user(request: Request) -> Optional[dict]:
    """Récupère l'utilisateur actuel depuis la session"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in active_sessions:
        user_id = active_sessions[session_id]
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            return dict(user)
    return None

def require_auth(request: Request):
    """Dépendance pour vérifier l'authentification"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Connexion requise")
    return user

def create_session(user_id: int) -> str:
    """Crée une nouvelle session"""
    session_id = hashlib.md5(f"{user_id}{datetime.now()}".encode()).hexdigest()
    active_sessions[session_id] = user_id
    return session_id

# Initialisation de la base de données
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            date_taken TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialiser la DB au démarrage
init_db()

# Routes principales
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Page d'accueil"""
    user = get_current_user(request)
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Traiter la connexion"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    
    if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
        session_id = create_session(user['id'])
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Nom d'utilisateur ou mot de passe incorrect"
        })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Page d'inscription"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """Traiter l'inscription"""
    conn = get_db_connection()
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = conn.execute(
        'SELECT id FROM users WHERE username = ? OR email = ?', (username, email)
    ).fetchone()
    
    if existing_user:
        conn.close()
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Nom d'utilisateur ou email déjà utilisé"
        })
    
    # Créer le nouvel utilisateur
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn.execute(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        (username, email, password_hash)
    )
    conn.commit()
    
    # Récupérer l'ID du nouvel utilisateur
    user_id = conn.lastrowid
    conn.close()
    
    # Créer une session et rediriger
    session_id = create_session(user_id)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response

@app.get("/logout")
async def logout(request: Request):
    """Déconnexion"""
    session_id = request.cookies.get("session_id")
    if session_id and session_id in active_sessions:
        del active_sessions[session_id]
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="session_id")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user: dict = Depends(require_auth)):
    """Tableau de bord utilisateur"""
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/python-tutor", response_class=HTMLResponse)
async def python_tutor(request: Request, user: dict = Depends(require_auth)):
    """Page DLH Tutor - Visualiseur de code multi-langages"""
    return templates.TemplateResponse("python_tutor.html", {"request": request, "user": user})

@app.post("/api/tutor/run")
async def tutor_run(request: Request, tutor_request: TutorRequest, user: dict = Depends(require_auth)):
    """API intégrée pour le DLH Tutor"""
    try:
        # Exécuter avec le moteur intégré
        result = tutor_engine.execute_code(tutor_request.code, tutor_request.language)
        
        if result['success']:
            return JSONResponse({
                'trace': result['trace'],
                'output': result.get('final_output', result.get('output', ''))
            })
        else:
            return JSONResponse({'error': result['error']}, status_code=400)
            
    except Exception as e:
        return JSONResponse({'error': f'Erreur interne: {str(e)}'}, status_code=500)

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_home(request: Request, user: dict = Depends(require_auth)):
    """Page d'accueil des quiz"""
    return templates.TemplateResponse("quiz_home.html", {
        "request": request, 
        "user": user, 
        "categories": categories
    })

@app.get("/quiz/{category}", response_class=HTMLResponse)
async def quiz_category(request: Request, category: str, user: dict = Depends(require_auth)):
    """Quiz pour une catégorie donnée"""
    if category not in categories:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    return templates.TemplateResponse("quiz.html", {
        "request": request,
        "user": user,
        "category": category,
        "questions": questions[category]
    })

@app.post("/quiz/{category}/submit")
async def submit_quiz(request: Request, category: str, quiz_submission: QuizSubmission, user: dict = Depends(require_auth)):
    """Soumettre un quiz"""
    if category not in categories:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    score = 0
    total_questions = len(questions[category])
    user_answers = quiz_submission.answers
    
    for i, question in enumerate(questions[category]):
        question_key = f"question_{i}"
        if question_key in user_answers:
            user_answer = int(user_answers[question_key])
            if user_answer == answers[category][i]:
                score += 1
    
    # Sauvegarder le score
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO quiz_scores (user_id, category, score, total_questions) VALUES (?, ?, ?, ?)',
        (user['id'], category, score, total_questions)
    )
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse("quiz_result.html", {
        "request": request,
        "user": user,
        "category": category,
        "score": score,
        "total": total_questions,
        "percentage": round((score / total_questions) * 100, 1)
    })

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, user: dict = Depends(require_auth)):
    """Profil utilisateur"""
    conn = get_db_connection()
    scores = conn.execute(
        'SELECT category, score, total_questions, date_taken FROM quiz_scores WHERE user_id = ? ORDER BY date_taken DESC',
        (user['id'],)
    ).fetchall()
    conn.close()
    
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "quiz_scores": scores
    })

# Point d'entrée pour Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001, reload=True)

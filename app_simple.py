"""
Dev Learning Hub Matrix - Version Simplifiée
FastAPI sans authentification
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Imports locaux
from quiz_data import questions, answers, categories
from tutor_engine import TutorEngine

# Charger les variables d'environnement
load_dotenv()

# Initialisation FastAPI
app = FastAPI(
    title="Dev Learning Hub Matrix - Edition Simplifiée",
    description="Plateforme d'apprentissage sans authentification",
    version="4.0.0"
)

# Configuration des templates et fichiers statiques avec chemin absolu
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Initialiser le moteur de tuteur
tutor_engine = TutorEngine()

# Route d'accueil
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil sans authentification"""
    return templates.TemplateResponse("index.html", {"request": request})

# Route dashboard (accessible sans connexion)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard accessible à tous"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Route Python Tutor
@app.get("/python-tutor", response_class=HTMLResponse)
async def python_tutor(request: Request):
    """DLH Tutor accessible à tous"""
    return templates.TemplateResponse("python_tutor.html", {"request": request})

# Routes Quiz
@app.get("/quiz", response_class=HTMLResponse)
async def quiz_home(request: Request):
    """Page d'accueil des quiz"""
    return templates.TemplateResponse("quiz_home.html", {
        "request": request,
        "categories": categories
    })

# Route pour exécuter du code (Python Tutor)
@app.post("/execute")
async def execute_code(request: Request):
    """Exécuter du code via le tutor engine"""
    try:
        data = await request.json()
        language = data.get("language", "python")
        code = data.get("code", "")
        
        if language == "python":
            result = tutor_engine.execute_python(code)
        elif language == "javascript":
            result = tutor_engine.execute_javascript(code)
        elif language == "c":
            result = tutor_engine.execute_c(code)
        else:
            result = {
                "success": False,
                "error": f"Langage non supporté: {language}",
                "output": "",
                "execution_time": 0
            }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de l'exécution: {str(e)}",
            "output": "",
            "execution_time": 0
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app_simple:app", 
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", "5001")), 
        reload=bool(os.getenv("DEBUG", "true").lower() == "true")
    )

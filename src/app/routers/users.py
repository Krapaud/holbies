from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models import User
from app.schemas import User as UserSchema
from app.auth import get_current_active_user

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

class SyncSessionRequest(BaseModel):
    user_id: int
    username: str

@router.post("/sync-session")
async def sync_session(
    request: Request, 
    sync_data: SyncSessionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Synchronise la session avec les informations de l'utilisateur JWT"""
    try:
        # Vérifier que l'utilisateur JWT correspond aux données envoyées
        if current_user.id != sync_data.user_id or current_user.username != sync_data.username:
            raise HTTPException(status_code=400, detail="Données utilisateur incohérentes")
        
        # Mettre à jour la session
        request.session["user_id"] = current_user.id
        request.session["username"] = current_user.username
        request.session["is_admin"] = current_user.is_admin
        
        return {"status": "success", "message": "Session synchronisée"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la synchronisation: {str(e)}")

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/profile", response_class=HTMLResponse)
async def user_profile(request: Request, current_user: User = Depends(get_current_active_user)):
    """Page de profil utilisateur"""
    context = {
        "request": request,
        "user": current_user
    }
    return templates.TemplateResponse("profile.html", context)

@router.get("/", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def is_admin(user: User, db: Session) -> bool:
    """Vérifie si un utilisateur est administrateur"""
    try:
        result = db.execute(text("SELECT is_admin FROM users WHERE id = :id"), {"id": user.id}).fetchone()
        return result[0] if result else False
    except:
        return False

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """Page d'administration - accessible uniquement aux admins"""
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Accès refusé - Droits administrateur requis")
    
    # Récupérer les statistiques
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    try:
        admin_result = db.execute(text("SELECT COUNT(*) FROM users WHERE is_admin = true")).fetchone()
        admin_count = admin_result[0] if admin_result else 0
    except:
        admin_count = 0
    
    # Récupérer tous les utilisateurs avec leur statut admin
    users = db.query(User).order_by(User.id).all()
    users_with_admin = []
    
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "is_admin": is_admin(user, db)
        }
        users_with_admin.append(user_dict)
    
    # Statistiques des autres tables
    try:
        quiz_sessions = db.execute(text("SELECT COUNT(*) FROM quiz_sessions")).fetchone()[0]
        questions = db.execute(text("SELECT COUNT(*) FROM questions")).fetchone()[0]
        ai_sessions = db.execute(text("SELECT COUNT(*) FROM ai_quiz_sessions")).fetchone()[0]
    except:
        quiz_sessions = questions = ai_sessions = 0
    
    context = {
        "request": request,
        "current_user": current_user,
        "stats": {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "admin_count": admin_count,
            "standard_users": total_users - admin_count,
            "quiz_sessions": quiz_sessions,
            "questions": questions,
            "ai_sessions": ai_sessions
        },
        "users": users_with_admin
    }
    
    return templates.TemplateResponse("admin-dashboard.html", context)

@router.get("/admin/stats")
async def admin_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """API pour récupérer les statistiques admin"""
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    try:
        admin_result = db.execute(text("SELECT COUNT(*) FROM users WHERE is_admin = true")).fetchone()
        admin_count = admin_result[0] if admin_result else 0
    except:
        admin_count = 0
    
    try:
        quiz_sessions = db.execute(text("SELECT COUNT(*) FROM quiz_sessions")).fetchone()[0]
        questions = db.execute(text("SELECT COUNT(*) FROM questions")).fetchone()[0]
        ai_sessions = db.execute(text("SELECT COUNT(*) FROM ai_quiz_sessions")).fetchone()[0]
    except:
        quiz_sessions = questions = ai_sessions = 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "admin_count": admin_count,
        "standard_users": total_users - admin_count,
        "quiz_sessions": quiz_sessions,
        "questions": questions,
        "ai_sessions": ai_sessions
    }

@router.get("/admin/users")
async def admin_users_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """API pour récupérer la liste des utilisateurs avec statut admin"""
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Accès refusé")
    
    users = db.query(User).order_by(User.id).all()
    users_data = []
    
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": is_admin(user, db),
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        users_data.append(user_data)
    
    return {"users": users_data}

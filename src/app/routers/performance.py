"""
Routes pour les statistiques de performance en temps réel
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User
from app.auth import get_current_active_user
from app.performance_service import get_performance_service
from app.routers.users import is_admin

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

@router.get("/stats/performance")
async def get_user_performance_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """API pour récupérer les statistiques de performance de l'utilisateur connecté"""
    performance_service = get_performance_service()
    try:
        stats = performance_service.calculate_user_performance(current_user.id)
        return {"success": True, "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des statistiques: {str(e)}")
    finally:
        performance_service.close()

@router.get("/stats/timeline")
async def get_user_performance_timeline(
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """API pour récupérer l'évolution des performances sur une période"""
    if days > 365:
        days = 365  # Limite maximum
    
    performance_service = get_performance_service()
    try:
        timeline = performance_service.get_user_progress_timeline(current_user.id, days)
        return {"success": True, "data": timeline, "period_days": days}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de la timeline: {str(e)}")
    finally:
        performance_service.close()

@router.get("/stats/system")
async def get_system_performance_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """API pour récupérer les statistiques de performance globales du système (admin only)"""
    if not is_admin(current_user, db):
        raise HTTPException(status_code=403, detail="Accès refusé - Droits administrateur requis")
    
    performance_service = get_performance_service()
    try:
        stats = performance_service.get_system_performance_stats()
        return {"success": True, "data": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul des statistiques système: {str(e)}")
    finally:
        performance_service.close()

@router.get("/analytics", response_class=HTMLResponse)
async def analytics_dashboard(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Page d'analytics avec graphiques de performance"""
    performance_service = get_performance_service()
    try:
        # Récupérer les stats utilisateur
        user_stats = performance_service.calculate_user_performance(current_user.id)
        timeline_30d = performance_service.get_user_progress_timeline(current_user.id, 30)
        
        # Stats système si admin
        system_stats = None
        if is_admin(current_user, db):
            system_stats = performance_service.get_system_performance_stats()
        
        context = {
            "request": request,
            "current_user": current_user,
            "user_stats": user_stats,
            "timeline": timeline_30d,
            "system_stats": system_stats,
            "is_admin": is_admin(current_user, db)
        }
        
        return templates.TemplateResponse("analytics.html", context)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chargement de la page analytics: {str(e)}")
    finally:
        performance_service.close()

@router.post("/stats/activity")
async def log_user_activity(
    activity_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """API pour enregistrer une activité utilisateur"""
    performance_service = get_performance_service()
    try:
        activity_type = activity_data.get("type", "unknown")
        data = activity_data.get("data", {})
        
        performance_service.log_user_activity(current_user.id, activity_type, data)
        return {"success": True, "message": "Activité enregistrée"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'enregistrement de l'activité: {str(e)}")
    finally:
        performance_service.close()

@router.get("/stats/leaderboard")
async def get_leaderboard(
    quiz_type: str = "all",  # "quiz", "ai_quiz", "all"
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """API pour récupérer le classement des utilisateurs"""
    if limit > 50:
        limit = 50  # Limite maximum
    
    performance_service = get_performance_service()
    try:
        system_stats = performance_service.get_system_performance_stats()
        leaderboard = system_stats.get("leaderboard", {})
        
        if quiz_type == "quiz":
            result = leaderboard.get("top_quiz_users", [])[:limit]
        elif quiz_type == "ai_quiz":
            result = leaderboard.get("top_ai_users", [])[:limit]
        else:
            # Combiner les deux classements
            quiz_users = leaderboard.get("top_quiz_users", [])
            ai_users = leaderboard.get("top_ai_users", [])
            
            # Créer un classement combiné (simplifié)
            combined = {}
            for user in quiz_users:
                combined[user["username"]] = {
                    "username": user["username"],
                    "quiz_score": user["avg_score"],
                    "quiz_sessions": user["sessions"],
                    "ai_score": 0,
                    "ai_sessions": 0
                }
            
            for user in ai_users:
                if user["username"] in combined:
                    combined[user["username"]]["ai_score"] = user["avg_score"]
                    combined[user["username"]]["ai_sessions"] = user["sessions"]
                else:
                    combined[user["username"]] = {
                        "username": user["username"],
                        "quiz_score": 0,
                        "quiz_sessions": 0,
                        "ai_score": user["avg_score"],
                        "ai_sessions": user["sessions"]
                    }
            
            # Calculer un score global et trier
            for username in combined:
                user_data = combined[username]
                total_score = user_data["quiz_score"] + user_data["ai_score"]
                total_sessions = user_data["quiz_sessions"] + user_data["ai_sessions"]
                user_data["total_score"] = total_score
                user_data["total_sessions"] = total_sessions
            
            result = sorted(combined.values(), key=lambda x: x["total_score"], reverse=True)[:limit]
        
        return {"success": True, "data": result, "type": quiz_type}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du classement: {str(e)}")
    finally:
        performance_service.close()

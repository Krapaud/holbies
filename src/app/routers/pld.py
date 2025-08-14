"""
Endpoints publics pour le système PLD (Peer Learning Day)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import json

from app.database import get_db
from app.models import PLDCategory, PLDTheme, PLDQuestion, User, AIQuizSession, AIQuizAnswer
from app.schemas import (
    PLDCategory as PLDCategorySchema, 
    PLDTheme as PLDThemeSchema,
    PLDQuestion as PLDQuestionSchema
)
from app.auth import get_current_active_user
from app.ai_feedback import ai_feedback_generator

router = APIRouter(prefix="/pld", tags=["pld"])

# ================================
# ROUTES PUBLIQUES PLD
# ================================

@router.get("/categories")
async def get_public_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupérer toutes les catégories disponibles pour l'utilisateur"""
    categories = db.query(PLDCategory).all()
    
    categories_data = []
    for category in categories:
        # Compter le nombre de questions dans cette catégorie
        question_count = db.query(PLDQuestion).join(PLDTheme).filter(
            PLDTheme.category_id == category.id
        ).count()
        
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'display_name': category.display_name,
            'description': category.description,
            'icon': category.icon,
            'question_count': question_count
        })
    
    return {"categories": categories_data}


@router.get("/categories/{category_name}/themes")
async def get_category_themes(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupérer tous les thèmes d'une catégorie"""
    category = db.query(PLDCategory).filter(PLDCategory.name == category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie '{category_name}' non trouvée"
        )
    
    themes = db.query(PLDTheme).filter(PLDTheme.category_id == category.id).all()
    
    if not themes:
        # Retourner 204 No Content si aucun thème
        from fastapi.responses import Response
        return Response(status_code=204)
    
    themes_data = []
    for theme in themes:
        # Compter les questions de ce thème
        question_count = db.query(PLDQuestion).filter(PLDQuestion.theme_id == theme.id).count()
        
        themes_data.append({
            'id': theme.id,
            'name': theme.name,
            'display_name': theme.display_name,
            'description': theme.description,
            'icon': theme.icon,
            'question_count': question_count
        })
    
    return {"themes": themes_data}


@router.get("/questions/{category_name}")
async def get_category_questions(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupérer toutes les questions d'une catégorie"""
    category = db.query(PLDCategory).filter(PLDCategory.name == category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie '{category_name}' non trouvée"
        )
    
    # Récupérer toutes les questions de cette catégorie
    questions = db.query(PLDQuestion).join(PLDTheme).filter(
        PLDTheme.category_id == category.id
    ).all()
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune question trouvée pour la catégorie '{category_name}'"
        )
    
    questions_data = []
    for question in questions:
        # Parser les termes techniques depuis JSON
        try:
            technical_terms = json.loads(question.technical_terms) if question.technical_terms else []
        except (json.JSONDecodeError, TypeError):
            technical_terms = []
        
        questions_data.append({
            'question_id': question.id,
            'question_text': question.question_text,
            'expected_answer': question.expected_answer,
            'explanation': question.explanation,
            'difficulty': question.difficulty,
            'max_score': question.max_score,
            'technical_terms': technical_terms,
            'theme_name': question.theme.name,
            'theme_display_name': question.theme.display_name
        })
    
    return {"questions": questions_data}


@router.get("/questions/{category_name}/{theme_name}")
async def get_theme_questions(
    category_name: str,
    theme_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupérer toutes les questions d'un thème spécifique"""
    category = db.query(PLDCategory).filter(PLDCategory.name == category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie '{category_name}' non trouvée"
        )
    
    theme = db.query(PLDTheme).filter(
        PLDTheme.name == theme_name,
        PLDTheme.category_id == category.id
    ).first()
    
    if not theme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Thème '{theme_name}' non trouvé dans la catégorie '{category_name}'"
        )
    
    # Récupérer toutes les questions de ce thème
    questions = db.query(PLDQuestion).filter(PLDQuestion.theme_id == theme.id).all()
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aucune question trouvée pour le thème '{theme_name}'"
        )
    
    questions_data = []
    for question in questions:
        # Parser les termes techniques depuis JSON
        try:
            technical_terms = json.loads(question.technical_terms) if question.technical_terms else []
        except (json.JSONDecodeError, TypeError):
            technical_terms = []
        
        questions_data.append({
            'question_id': question.id,
            'question_text': question.question_text,
            'expected_answer': question.expected_answer,
            'explanation': question.explanation,
            'difficulty': question.difficulty,
            'max_score': question.max_score,
            'technical_terms': technical_terms,
            'theme_name': theme.name,
            'theme_display_name': theme.display_name
        })
    
    return {"questions": questions_data}


# ================================
# GESTION DES SESSIONS PLD
# ================================

@router.post("/start")
async def start_pld_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Démarrer une nouvelle session PLD"""
    # Créer une nouvelle session AI Quiz (réutiliser le même système)
    session = AIQuizSession(
        user_id=current_user.id
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "id": session.id,
        "user_id": session.user_id,
        "started_at": session.started_at,
        "completed": session.completed
    }


@router.post("/submit-answer")
async def submit_pld_answer(
    answer_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soumettre une réponse pour évaluation"""
    
    session_id = answer_data.get("session_id")
    question_id = answer_data.get("question_id")
    user_answer = answer_data.get("user_answer")
    
    if not all([session_id, question_id, user_answer]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id, question_id et user_answer sont requis"
        )
    
    # Vérifier que la session appartient à l'utilisateur
    session = db.query(AIQuizSession).filter(
        AIQuizSession.id == session_id,
        AIQuizSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session non trouvée"
        )
    
    # Récupérer la question
    question = db.query(PLDQuestion).filter(PLDQuestion.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question non trouvée"
        )
    
    # Calculer le score (logique simplifiée pour l'instant)
    score = calculate_answer_score(user_answer, question)
    
    # Générer un feedback intelligent avec l'IA
    try:
        # Parser les termes techniques
        technical_terms = json.loads(question.technical_terms) if question.technical_terms else []
    except (json.JSONDecodeError, TypeError):
        technical_terms = []
    
    # Générer le feedback IA
    ai_feedback = ai_feedback_generator.generate_intelligent_feedback(
        user_answer=user_answer,
        question_text=question.question_text,
        expected_answer=question.expected_answer,
        technical_terms=technical_terms,
        score=score,
        max_score=question.max_score or 100
    )
    
    # Formater le feedback pour l'affichage
    formatted_feedback = ai_feedback_generator.format_feedback_for_display(ai_feedback)
    
    # Sauvegarder la réponse
    answer = AIQuizAnswer(
        session_id=session_id,
        question_id=question_id,
        question_text=question.question_text,
        user_answer=user_answer,
        expected_answer=question.expected_answer,
        score=score,
        max_score=question.max_score or 100,
        percentage=(score / (question.max_score or 100)) * 100,
        similarity=0.0,  # Pour l'instant, pas de calcul de similarité
        feedback=ai_feedback.get('feedback_principal', 'Réponse évaluée automatiquement')
    )
    db.add(answer)
    db.commit()
    
    return {
        "score": score,
        "max_score": question.max_score or 100,
        "percentage": (score / (question.max_score or 100)) * 100 if (question.max_score or 100) > 0 else 0,
        "feedback": formatted_feedback,
        "ai_feedback": ai_feedback,  # Feedback structuré pour le frontend
        "expected_answer": question.expected_answer  # On peut garder la réponse attendue pour référence
    }


@router.post("/complete")
async def complete_pld_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marquer une session PLD comme terminée"""
    session = db.query(AIQuizSession).filter(
        AIQuizSession.id == session_id,
        AIQuizSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session non trouvée"
        )
    
    # Marquer comme terminée
    session.completed = True
    db.commit()
    
    return {"message": "Session PLD terminée avec succès"}


# ================================
# FONCTIONS UTILITAIRES
# ================================

def calculate_answer_score(user_answer: str, question: PLDQuestion) -> float:
    """
    Calculer le score d'une réponse utilisateur
    (Logique simplifiée - peut être améliorée)
    """
    if not user_answer or not question.expected_answer:
        return 0.0
    
    user_answer_lower = user_answer.lower().strip()
    expected_answer_lower = question.expected_answer.lower().strip()
    
    # Score basé sur la longueur relative et la présence de mots-clés
    base_score = question.max_score * 0.3  # Score de base pour avoir essayé
    
    # Bonus pour la longueur (encourager les réponses détaillées)
    if len(user_answer) >= 50:
        base_score += question.max_score * 0.2
    
    # Bonus pour les termes techniques
    try:
        technical_terms = json.loads(question.technical_terms) if question.technical_terms else []
        terms_found = sum(1 for term in technical_terms if term.lower() in user_answer_lower)
        if terms_found > 0:
            base_score += (terms_found / len(technical_terms)) * question.max_score * 0.3
    except (json.JSONDecodeError, TypeError):
        pass
    
    # Bonus pour similarité avec la réponse attendue
    common_words = set(user_answer_lower.split()) & set(expected_answer_lower.split())
    if common_words:
        base_score += len(common_words) / len(expected_answer_lower.split()) * question.max_score * 0.2
    
    return min(base_score, question.max_score)

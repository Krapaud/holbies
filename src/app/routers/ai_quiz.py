from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Dict
from pydantic import BaseModel
import difflib
import re
import json
from datetime import datetime

from app.database import get_db
from app.models import User, AIQuizSession, AIQuizAnswer, PLDCategory, PLDTheme, PLDQuestion
from app.schemas import AIQuizSession as AIQuizSessionSchema, AIQuizAnswer as AIQuizAnswerSchema, AIQuizAnswerSubmission, AIQuizResult
from app.auth import get_current_active_user

router = APIRouter()

class AIQuestionResponse(BaseModel):
    question_id: int
    question_text: str
    expected_answer: str
    technical_terms: List[str]
    explanation: str
    difficulty: str
    category: str
    max_score: int = 100

class AIAnswerSubmission(BaseModel):
    question_id: int
    user_answer: str

class AIAnswerResult(BaseModel):
    score: float
    max_score: int
    percentage: float
    similarity: float
    technical_terms_found: List[str]
    technical_bonus: int
    feedback: str
    detailed_explanation: str

class AIQuizCorrector:
    """Correcteur IA pour les réponses textuelles - Version API"""
    
    def __init__(self):
        self.bonus_multiplier = 1.2
        self.similarity_weight = 0.7
        self.technical_weight = 0.3
        
    def normalize_text(self, text: str) -> str:
        """Normalise le texte pour la comparaison"""
        text = re.sub(r'[^\w\s]', '', text.lower())
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def calculate_similarity(self, user_answer: str, expected_answer: str) -> float:
        """Calcule la similarité entre deux textes"""
        user_norm = self.normalize_text(user_answer)
        expected_norm = self.normalize_text(expected_answer)
        
        similarity = difflib.SequenceMatcher(None, user_norm, expected_norm).ratio()
        
        user_words = set(user_norm.split())
        expected_words = set(expected_norm.split())
        word_overlap = len(user_words.intersection(expected_words)) / len(expected_words) if expected_words else 0
        
        return (similarity * 0.6 + word_overlap * 0.4)
    
    def find_technical_terms(self, user_answer: str, technical_terms: List[str]) -> List[str]:
        """Trouve les termes techniques utilisés dans la réponse"""
        user_norm = self.normalize_text(user_answer)
        found_terms = []
        
        for term in technical_terms:
            term_norm = self.normalize_text(term)
            if term_norm in user_norm:
                found_terms.append(term)
        
        return found_terms
    
    def correct_answer(self, question_data: Dict, user_answer: str) -> Dict:
        """Corrige une réponse utilisateur et attribue un score"""
        if not user_answer.strip():
            return {
                'score': 0,
                'max_score': question_data['max_score'],
                'percentage': 0,
                'similarity': 0,
                'technical_terms_found': [],
                'technical_bonus': 0,
                'feedback': "Aucune réponse fournie.",
                'detailed_explanation': question_data['explanation']
            }
        
        similarity = self.calculate_similarity(user_answer, question_data['expected_answer'])
        
        technical_terms_found = self.find_technical_terms(user_answer, question_data['technical_terms'])
        technical_ratio = len(technical_terms_found) / len(question_data['technical_terms']) if question_data['technical_terms'] else 0
        
        base_score = (similarity * self.similarity_weight + technical_ratio * self.technical_weight) * question_data['max_score']
        
        technical_bonus = len(technical_terms_found) * 5
        
        final_score = min(base_score + technical_bonus, question_data['max_score'])
        
        feedback = self.generate_feedback(similarity, technical_terms_found, question_data['technical_terms'], final_score, question_data['max_score'])
        
        return {
            'score': round(final_score, 1),
            'max_score': question_data['max_score'],
            'percentage': round((final_score / question_data['max_score']) * 100, 1),
            'similarity': round(similarity * 100, 1),
            'technical_terms_found': technical_terms_found,
            'technical_bonus': technical_bonus,
            'feedback': feedback,
            'detailed_explanation': question_data['explanation']
        }
    
    def generate_feedback(self, similarity: float, found_terms: List[str], all_terms: List[str], score: float, max_score: float) -> str:
        """Génère un feedback personnalisé"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            feedback = "🏆 Excellente réponse ! "
        elif percentage >= 75:
            feedback = "👍 Très bonne réponse ! "
        elif percentage >= 60:
            feedback = "📚 Bonne réponse, mais peut être améliorée. "
        elif percentage >= 40:
            feedback = "💪 Réponse partiellement correcte. "
        else:
            feedback = "📖 La réponse nécessite des améliorations importantes. "
        
        if found_terms:
            feedback += f"Termes techniques utilisés correctement : {', '.join(found_terms)}. "
        
        missed_terms = [term for term in all_terms if term not in found_terms]
        if missed_terms:
            feedback += f"Termes techniques manqués : {', '.join(missed_terms)}. "
        
        feedback += f"Similarité avec la réponse attendue : {similarity * 100:.1f}%."
        
        return feedback

# Instance du correcteur IA
ai_corrector = AIQuizCorrector()

# ================================
# SERVICES DE BASE DE DONNÉES
# ================================

def get_questions_from_db(db: Session, category: str = None, theme: str = None):
    """Récupérer les questions depuis la base de données"""
    query = db.query(PLDQuestion).join(PLDTheme).join(PLDCategory)
    
    if category:
        query = query.filter(PLDCategory.name == category)
    
    if theme:
        query = query.filter(PLDTheme.name == theme)
    
    questions = query.all()
    
    # Convertir au format attendu par le frontend
    result = []
    for q in questions:
        result.append({
            "question_id": q.id,
            "question_text": q.question_text,
            "expected_answer": q.expected_answer,
            "technical_terms": json.loads(q.technical_terms),
            "explanation": q.explanation,
            "difficulty": q.difficulty,
            "category": q.theme.category.name,
            "theme": q.theme.name,
            "max_score": q.max_score
        })
    
    return result

def get_categories_from_db(db: Session):
    """Récupérer toutes les catégories depuis la base de données"""
    categories = db.query(PLDCategory).all()
    return [
        {
            "name": cat.name,
            "display_name": cat.display_name,
            "description": cat.description,
            "icon": cat.icon,
            "question_count": sum(len(theme.questions) for theme in cat.themes)
        }
        for cat in categories
    ]

def get_themes_from_db(db: Session, category: str):
    """Récupérer les thèmes d'une catégorie depuis la base de données"""
    category_obj = db.query(PLDCategory).filter(PLDCategory.name == category).first()
    if not category_obj:
        return []
    
    return [
        {
            "name": theme.name,
            "display_name": theme.display_name,
            "description": theme.description,
            "icon": theme.icon,
            "question_count": len(theme.questions)
        }
        for theme in category_obj.themes
    ]

def find_question_by_id_db(db: Session, question_id: int):
    """Trouver une question par ID dans la base de données"""
    question = db.query(PLDQuestion).filter(PLDQuestion.id == question_id).first()
    if not question:
        return None
    
    return {
        "question_id": question.id,
        "question_text": question.question_text,
        "expected_answer": question.expected_answer,
        "technical_terms": json.loads(question.technical_terms),
        "explanation": question.explanation,
        "difficulty": question.difficulty,
        "category": question.theme.category.name,
        "theme": question.theme.name,
        "max_score": question.max_score
    }

def count_total_questions_db(db: Session):
    """Compter le nombre total de questions dans la base de données"""
    return db.query(PLDQuestion).count()

# AI Quiz Session Management Endpoints

# AI Quiz Session Management Endpoints
@router.get("/sessions", response_model=List[AIQuizSessionSchema])
async def get_user_ai_quiz_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère toutes les sessions AI Quiz de l'utilisateur"""
    sessions = db.query(AIQuizSession).filter(
        AIQuizSession.user_id == current_user.id
    ).order_by(AIQuizSession.started_at.desc()).all()
    return sessions

@router.get("/sessions/active", response_model=AIQuizSessionSchema)
async def get_active_ai_quiz_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la session AI Quiz active de l'utilisateur"""
    active_session = db.query(AIQuizSession).filter(
        AIQuizSession.user_id == current_user.id,
        AIQuizSession.completed == False
    ).first()
    
    if not active_session:
        raise HTTPException(
            status_code=404,
            detail="No active AI quiz session found"
        )
    
    return active_session

@router.post("/start", response_model=AIQuizSessionSchema)
async def start_ai_quiz_session(
    force_new: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Démarre une nouvelle session AI Quiz"""
    # Vérifier s'il y a une session active
    active_session = db.query(AIQuizSession).filter(
        AIQuizSession.user_id == current_user.id,
        AIQuizSession.completed == False
    ).first()
    
    if active_session and not force_new:
        # Retourner la session existante
        return active_session
    elif active_session and force_new:
        # Marquer l'ancienne session comme complétée
        active_session.completed = True
        db.commit()
    
    # Créer une nouvelle session
    ai_quiz_session = AIQuizSession(
        user_id=current_user.id,
        total_questions=count_total_questions_db(db)
    )
    db.add(ai_quiz_session)
    db.commit()
    db.refresh(ai_quiz_session)
    return ai_quiz_session

@router.get("/ai-questions", response_model=List[AIQuestionResponse])
async def get_ai_questions(
    category: str = None,
    theme: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la liste des questions pour le quiz IA par catégorie et/ou thème depuis la DB"""
    try:
        questions_data = get_questions_from_db(db, category, theme)
        
        if not questions_data:
            detail = "No questions found"
            if category and theme:
                detail = f"No questions found for category '{category}' and theme '{theme}'"
            elif category:
                detail = f"No questions found for category '{category}'"
            raise HTTPException(status_code=404, detail=detail)
        
        questions = []
        for question_data in questions_data:
            questions.append(AIQuestionResponse(**question_data))
        
        return questions
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving questions: {str(e)}"
        )

@router.get("/ai-questions/{question_id}", response_model=AIQuestionResponse)
async def get_ai_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère une question spécifique pour le quiz IA depuis la DB"""
    question_data = find_question_by_id_db(db, question_id)
    if not question_data:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    return AIQuestionResponse(**question_data)

@router.post("/submit-answer", response_model=AIAnswerResult)
async def submit_ai_answer(
    submission: AIQuizAnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soumet une réponse textuelle pour correction par IA et sauvegarde dans une session"""
    # Vérifier que la question existe dans la base de données
    question_data = find_question_by_id_db(db, submission.question_id)
    if not question_data:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    # Vérifier que la session existe et appartient à l'utilisateur
    session = db.query(AIQuizSession).filter(
        AIQuizSession.id == submission.session_id,
        AIQuizSession.user_id == current_user.id,
        AIQuizSession.completed == False
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Active AI quiz session not found"
        )
    
    # Correction par IA
    result = ai_corrector.correct_answer(question_data, submission.user_answer)
    
    # Sauvegarder la réponse dans la base de données
    ai_answer = AIQuizAnswer(
        session_id=session.id,
        question_id=submission.question_id,
        question_text=question_data["question_text"],
        user_answer=submission.user_answer,
        expected_answer=question_data["expected_answer"],
        score=result["score"],
        max_score=result["max_score"],
        percentage=result["percentage"],
        similarity=result["similarity"],
        technical_terms_found=json.dumps(result["technical_terms_found"]),
        technical_bonus=result["technical_bonus"],
        feedback=result["feedback"]
    )
    
    db.add(ai_answer)
    
    # Mettre à jour le score total de la session
    session.total_score += result["score"]
    
    db.commit()
    db.refresh(ai_answer)
    
    return AIAnswerResult(**result)

@router.post("/complete", response_model=AIQuizResult)
async def complete_ai_quiz_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Marque une session AI Quiz comme complétée et retourne les résultats"""
    session = db.query(AIQuizSession).filter(
        AIQuizSession.id == session_id,
        AIQuizSession.user_id == current_user.id,
        AIQuizSession.completed == False
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Active AI quiz session not found"
        )
    
    # Marquer comme complétée
    session.completed = True
    session.completed_at = datetime.utcnow()
    
    # Calculer le nombre de questions répondues
    answered_questions = db.query(AIQuizAnswer).filter(
        AIQuizAnswer.session_id == session.id
    ).count()
    
    session.total_questions = answered_questions
    
    db.commit()
    
    # Récupérer toutes les réponses pour les résultats
    answers = db.query(AIQuizAnswer).filter(
        AIQuizAnswer.session_id == session.id
    ).all()
    
    # Calculer le pourcentage moyen
    average_percentage = (session.total_score / (answered_questions * 100)) * 100 if answered_questions > 0 else 0
    
    return AIQuizResult(
        session_id=session.id,
        total_score=session.total_score,
        total_questions=session.total_questions,
        average_percentage=average_percentage,
        answers=answers
    )

# Ancien endpoint maintenu pour compatibilité (sans session)
@router.post("/ai-submit", response_model=AIAnswerResult)
async def submit_ai_answer_legacy(
    submission: AIAnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soumet une réponse textuelle pour correction par IA (legacy - sans session)"""
    question_data = find_question_by_id_db(db, submission.question_id)
    if not question_data:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    # Correction par IA
    result = ai_corrector.correct_answer(question_data, submission.user_answer)
    
    return AIAnswerResult(**result)

@router.get("/ai-quiz/demo")
async def get_demo_info(db: Session = Depends(get_db)):
    """Informations sur le quiz IA (accessible sans authentification pour démo)"""
    return {
        "title": "Quiz IA avec Correction Automatique",
        "description": "Système de quiz avancé avec réponses textuelles corrigées par IA",
        "features": [
            "Réponses textuelles libres",
            "Correction automatique par IA",
            "Scoring basé sur la précision et l'usage de termes techniques",
            "Feedback détaillé personnalisé",
            "Bonus pour les termes techniques"
        ],
        "scoring": {
            "similarity_weight": "70% - Similarité avec la réponse attendue",
            "technical_weight": "30% - Usage des termes techniques",
            "technical_bonus": "5 points par terme technique utilisé",
            "max_score_per_question": 100
        },
        "total_questions": count_total_questions_db(db)
    }

@router.get("/categories/{category}/themes")
async def get_category_themes(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la liste des thèmes disponibles pour une catégorie depuis la DB"""
    themes_data = get_themes_from_db(db, category)
    
    if not themes_data:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found or has no themes"
        )
    
    return {"themes": themes_data}

@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la liste des catégories disponibles depuis la DB"""
    categories_data = get_categories_from_db(db)
    return {"categories": categories_data}

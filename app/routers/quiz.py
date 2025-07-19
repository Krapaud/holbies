from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import random
from datetime import datetime

from app.database import get_db
from app.models import User, Question, QuizSession, QuizAnswer
from app.schemas import (
    Question as QuestionSchema, 
    QuestionCreate, 
    QuizAnswer as QuizAnswerSchema,
    QuizSession as QuizSessionSchema,
    QuizResult,
    QuizAnswerSubmission
)
from app.auth import get_current_active_user

router = APIRouter()

@router.get("/questions", response_model=List[QuestionSchema])
async def get_quiz_questions(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère un ensemble aléatoire de questions pour le quiz"""
    total_questions = db.query(Question).count()
    if total_questions < limit:
        limit = total_questions
    
    # Sélectionner des questions aléatoires
    questions = db.query(Question).order_by(func.random()).limit(limit).all()
    return questions

@router.get("/sessions", response_model=List[QuizSessionSchema])
async def get_user_quiz_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère toutes les sessions de quiz de l'utilisateur"""
    sessions = db.query(QuizSession).filter(
        QuizSession.user_id == current_user.id
    ).order_by(QuizSession.created_at.desc()).all()
    return sessions

@router.get("/sessions/active", response_model=QuizSessionSchema)
async def get_active_quiz_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la session de quiz active de l'utilisateur"""
    active_session = db.query(QuizSession).filter(
        QuizSession.user_id == current_user.id,
        QuizSession.completed == False
    ).first()
    
    if not active_session:
        raise HTTPException(
            status_code=404,
            detail="No active quiz session found"
        )
    
    return active_session

@router.post("/start", response_model=QuizSessionSchema)
async def start_quiz_session(
    force_new: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Démarre une nouvelle session de quiz"""
    # Vérifier s'il y a une session active
    active_session = db.query(QuizSession).filter(
        QuizSession.user_id == current_user.id,
        QuizSession.completed == False
    ).first()
    
    if active_session and not force_new:
        # Retourner la session existante
        return active_session
    elif active_session and force_new:
        # Marquer l'ancienne session comme complétée
        active_session.completed = True
        db.commit()
    
    # Créer une nouvelle session
    quiz_session = QuizSession(
        user_id=current_user.id,
        total_questions=10  # Par défaut 10 questions
    )
    db.add(quiz_session)
    db.commit()
    db.refresh(quiz_session)
    return quiz_session

@router.post("/submit-answer")
async def submit_answer(
    answer_data: QuizAnswerSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Soumet une réponse pour une question"""
    # Vérifier que la session appartient à l'utilisateur
    session = db.query(QuizSession).filter(
        QuizSession.id == answer_data.session_id,
        QuizSession.user_id == current_user.id,
        QuizSession.completed == False
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Quiz session not found or already completed"
        )
    
    # Récupérer la question
    question = db.query(Question).filter(Question.id == answer_data.question_id).first()
    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    # Vérifier si la réponse existe déjà
    existing_answer = db.query(QuizAnswer).filter(
        QuizAnswer.session_id == answer_data.session_id,
        QuizAnswer.question_id == answer_data.question_id
    ).first()
    
    if existing_answer:
        raise HTTPException(
            status_code=400,
            detail="Answer already submitted for this question"
        )
    
    # Vérifier si la réponse est correcte
    is_correct = answer_data.user_answer.lower() == question.correct_answer.lower()
    
    # Enregistrer la réponse
    quiz_answer = QuizAnswer(
        session_id=answer_data.session_id,
        question_id=answer_data.question_id,
        user_answer=answer_data.user_answer,
        is_correct=is_correct
    )
    db.add(quiz_answer)
    
    # Mettre à jour le score si correct
    if is_correct:
        session.score += 1
    
    db.commit()
    
    return {
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation
    }

@router.post("/complete/{session_id}", response_model=QuizResult)
async def complete_quiz(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Finalise une session de quiz"""
    session = db.query(QuizSession).filter(
        QuizSession.id == session_id,
        QuizSession.user_id == current_user.id,
        QuizSession.completed == False
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Quiz session not found or already completed"
        )
    
    # Marquer la session comme terminée
    session.completed = True
    session.completed_at = datetime.utcnow()
    
    # Récupérer toutes les réponses
    answers = db.query(QuizAnswer).filter(QuizAnswer.session_id == session_id).all()
    session.total_questions = len(answers)
    
    db.commit()
    
    # Calculer les résultats
    correct_answers = [a.question_id for a in answers if a.is_correct]
    incorrect_answers = [a.question_id for a in answers if not a.is_correct]
    percentage = (session.score / session.total_questions * 100) if session.total_questions > 0 else 0
    
    return QuizResult(
        session_id=session.id,
        score=session.score,
        total_questions=session.total_questions,
        percentage=percentage,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers
    )

@router.get("/sessions", response_model=List[QuizSessionSchema])
async def get_user_quiz_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère l'historique des sessions de quiz de l'utilisateur"""
    sessions = db.query(QuizSession).filter(
        QuizSession.user_id == current_user.id
    ).order_by(QuizSession.started_at.desc()).all()
    return sessions

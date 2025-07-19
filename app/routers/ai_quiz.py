from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel
import difflib
import re

from app.database import get_db
from app.models import User
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

# Base de données des questions textuelles
AI_QUESTIONS_DB = {
    1: {
        "question_id": 1,
        "question_text": "Expliquez ce qu'est un pointeur en C et comment il fonctionne.",
        "expected_answer": "Un pointeur est une variable qui stocke l'adresse mémoire d'une autre variable. Il permet d'accéder indirectement aux données en mémoire en utilisant l'opérateur de déréférencement *.",
        "technical_terms": ["pointeur", "adresse mémoire", "variable", "déréférencement", "opérateur *", "indirection"],
        "explanation": "Un pointeur en C est fondamental pour la gestion de la mémoire dynamique et l'efficacité du code. L'opérateur & récupère l'adresse d'une variable, tandis que * déréférence un pointeur pour accéder à la valeur.",
        "difficulty": "medium",
        "category": "c-programming",
        "max_score": 100
    },
    2: {
        "question_id": 2,
        "question_text": "Décrivez la différence entre malloc() et calloc() en C.",
        "expected_answer": "malloc() alloue un bloc de mémoire de taille spécifiée sans l'initialiser, tandis que calloc() alloue de la mémoire pour un tableau d'éléments et initialise tous les octets à zéro.",
        "technical_terms": ["malloc", "calloc", "allocation dynamique", "mémoire", "initialisation", "zéro", "heap", "octets"],
        "explanation": "malloc() est plus rapide car elle n'initialise pas la mémoire, mais calloc() garantit une mémoire propre initialisée à zéro, ce qui peut éviter des bugs liés aux valeurs non initialisées.",
        "difficulty": "medium",
        "category": "c-programming",
        "max_score": 100
    },
    3: {
        "question_id": 3,
        "question_text": "Qu'est-ce que la segmentation fault et pourquoi se produit-elle ?",
        "expected_answer": "Une segmentation fault est une erreur qui se produit quand un programme tente d'accéder à une zone mémoire qui ne lui appartient pas ou qui n'est pas autorisée, souvent causée par un déréférencement de pointeur invalide.",
        "technical_terms": ["segmentation fault", "SIGSEGV", "mémoire", "pointeur invalide", "déréférencement", "accès mémoire", "protection mémoire"],
        "explanation": "Les segmentation faults sont un mécanisme de protection du système d'exploitation pour empêcher les programmes d'écraser la mémoire d'autres processus ou du système.",
        "difficulty": "medium",
        "category": "c-programming",
        "max_score": 100
    },
    4: {
        "question_id": 4,
        "question_text": "Expliquez le concept de gestion automatique de la mémoire vs manuelle en C.",
        "expected_answer": "En C, la gestion mémoire est manuelle : le programmeur doit explicitement allouer avec malloc/calloc et libérer avec free. Contrairement aux langages avec garbage collector, C donne le contrôle total mais exige une discipline stricte.",
        "technical_terms": ["gestion mémoire", "malloc", "free", "garbage collector", "allocation manuelle", "libération", "fuites mémoire", "stack", "heap"],
        "explanation": "La gestion manuelle offre performance et contrôle précis, mais augmente le risque de fuites mémoire et d'erreurs. Les langages modernes automatisent souvent cette gestion.",
        "difficulty": "hard",
        "category": "c-programming",
        "max_score": 100
    },
    5: {
        "question_id": 5,
        "question_text": "Décrivez ce qui se passe lors de la compilation d'un programme C.",
        "expected_answer": "La compilation C se fait en plusieurs étapes : préprocesseur (macros, includes), compilateur (code source vers assembleur), assembleur (assembleur vers code objet), et éditeur de liens (liaison des modules pour créer l'exécutable).",
        "technical_terms": ["préprocesseur", "compilateur", "assembleur", "éditeur de liens", "linker", "code objet", "exécutable", "macros", "bibliothèques"],
        "explanation": "Chaque étape a un rôle spécifique : le préprocesseur traite les directives, le compilateur optimise et génère du code machine, l'éditeur de liens résout les symboles externes.",
        "difficulty": "hard",
        "category": "c-programming",
        "max_score": 100
    }
}

@router.get("/ai-questions", response_model=List[AIQuestionResponse])
async def get_ai_questions(
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la liste des questions pour le quiz IA"""
    questions = []
    for question_data in AI_QUESTIONS_DB.values():
        questions.append(AIQuestionResponse(**question_data))
    return questions

@router.get("/ai-questions/{question_id}", response_model=AIQuestionResponse)
async def get_ai_question(
    question_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère une question spécifique pour le quiz IA"""
    if question_id not in AI_QUESTIONS_DB:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    question_data = AI_QUESTIONS_DB[question_id]
    return AIQuestionResponse(**question_data)

@router.post("/ai-submit", response_model=AIAnswerResult)
async def submit_ai_answer(
    submission: AIAnswerSubmission,
    current_user: User = Depends(get_current_active_user)
):
    """Soumet une réponse textuelle pour correction par IA"""
    if submission.question_id not in AI_QUESTIONS_DB:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    
    question_data = AI_QUESTIONS_DB[submission.question_id]
    
    # Correction par IA
    result = ai_corrector.correct_answer(question_data, submission.user_answer)
    
    return AIAnswerResult(**result)

@router.get("/ai-quiz/demo")
async def get_demo_info():
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
        "total_questions": len(AI_QUESTIONS_DB)
    }

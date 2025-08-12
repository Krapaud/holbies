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

# Base de données des questions textuelles (LEGACY - à supprimer après migration)
# Base de données des questions avec structure hiérarchique : catégorie -> thème -> questions
AI_QUESTIONS_DB = {
    "shell": {
        "permission": {
            1: {
                "question_id": 1,
                "question_text": "Expliquez la différence entre chmod 755 et chmod 644 sur un fichier.",
                "expected_answer": "chmod 755 donne les permissions rwx pour le propriétaire et rx pour le groupe et les autres, tandis que chmod 644 donne rw pour le propriétaire et r pour le groupe et les autres. 755 est typique pour les exécutables, 644 pour les fichiers de données.",
                "technical_terms": ["chmod", "permissions", "rwx", "propriétaire", "groupe", "autres", "octal", "755", "644"],
                "explanation": "Les permissions Unix utilisent 3 bits par catégorie : r(4) + w(2) + x(1). 755 = rwxr-xr-x, 644 = rw-r--r--",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            2: {
                "question_id": 2,
                "question_text": "Comment changer le propriétaire d'un fichier et pourquoi utiliser sudo ?",
                "expected_answer": "On utilise chown pour changer le propriétaire : chown utilisateur:groupe fichier. Sudo est nécessaire car seul le root ou le propriétaire actuel peut changer la propriété d'un fichier.",
                "technical_terms": ["chown", "propriétaire", "groupe", "sudo", "root", "permissions", "utilisateur"],
                "explanation": "chown modifie les métadonnées du système de fichiers. Sudo élève temporairement les privilèges pour les opérations administratives.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            3: {
                "question_id": 3,
                "question_text": "Que fait umask et comment calculer les permissions résultantes ?",
                "expected_answer": "umask définit les permissions par défaut en soustrayant ses valeurs des permissions maximales. Pour les fichiers (666), umask 022 donne 644. Pour les dossiers (777), umask 022 donne 755.",
                "technical_terms": ["umask", "permissions par défaut", "masque", "666", "777", "022", "soustraction"],
                "explanation": "umask agit comme un masque inversé : il retire des permissions. Plus umask est élevé, moins il y a de permissions accordées par défaut.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            4: {
                "question_id": 4,
                "question_text": "Expliquez les permissions spéciales : sticky bit, SUID et SGID.",
                "expected_answer": "SUID (4000) permet d'exécuter avec les droits du propriétaire, SGID (2000) avec ceux du groupe, sticky bit (1000) empêche la suppression par d'autres utilisateurs dans un répertoire partagé.",
                "technical_terms": ["sticky bit", "SUID", "SGID", "permissions spéciales", "4000", "2000", "1000", "exécution"],
                "explanation": "Ces permissions spéciales modifient le comportement d'exécution et d'accès au-delà des permissions standards rwx.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            5: {
                "question_id": 5,
                "question_text": "Comment voir les permissions détaillées d'un fichier ?",
                "expected_answer": "ls -l affiche les permissions sous forme de chaîne (rwxrwxrwx), ls -la inclut les fichiers cachés, stat donne des informations détaillées incluant les permissions en octal.",
                "technical_terms": ["ls -l", "ls -la", "stat", "permissions", "octal", "fichiers cachés", "métadonnées"],
                "explanation": "Plusieurs commandes permettent de voir les permissions avec différents niveaux de détail selon les besoins.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            6: {
                "question_id": 6,
                "question_text": "Quelle est la différence entre su et sudo ?",
                "expected_answer": "su change d'utilisateur complètement et nécessite le mot de passe de l'utilisateur cible, sudo exécute une commande avec des privilèges élevés en utilisant votre propre mot de passe et selon la configuration sudoers.",
                "technical_terms": ["su", "sudo", "utilisateur", "mot de passe", "privilèges", "sudoers", "switch user"],
                "explanation": "su est un changement complet d'identité, sudo est une élévation temporaire et contrôlée de privilèges.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            7: {
                "question_id": 7,
                "question_text": "Comment donner temporairement les permissions d'exécution à un script ?",
                "expected_answer": "chmod +x script.sh ajoute les permissions d'exécution pour tous, ou chmod u+x pour le propriétaire seulement. On peut aussi utiliser sh script.sh sans changer les permissions.",
                "technical_terms": ["chmod +x", "chmod u+x", "permissions d'exécution", "script", "sh", "propriétaire"],
                "explanation": "Les permissions d'exécution sont nécessaires pour lancer un script directement. Alternativement, passer par l'interpréteur contourne cette exigence.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            }
        },
        "io": {
            8: {
                "question_id": 8,
                "question_text": "Expliquez la différence entre >, >> et < dans le shell.",
                "expected_answer": "> redirige la sortie en écrasant le fichier, >> ajoute à la fin du fichier, < redirige l'entrée depuis un fichier. > et >> concernent la sortie (stdout), < concerne l'entrée (stdin).",
                "technical_terms": ["redirection", "stdout", "stdin", ">", ">>", "<", "écrasement", "ajout", "entrée", "sortie"],
                "explanation": "Les redirections permettent de manipuler les flux d'entrée et sortie standard des commandes Unix.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            9: {
                "question_id": 9,
                "question_text": "Comment fonctionne le pipe | et donnez un exemple d'utilisation ?",
                "expected_answer": "Le pipe | connecte la sortie d'une commande à l'entrée de la suivante. Exemple : ls -l | grep '.txt' filtre les fichiers .txt dans la liste. C'est un mécanisme de communication inter-processus.",
                "technical_terms": ["pipe", "|", "sortie", "entrée", "grep", "ls", "filtre", "inter-processus", "chaînage"],
                "explanation": "Les pipes permettent de chaîner des commandes pour créer des workflows complexes de traitement de données.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            10: {
                "question_id": 10,
                "question_text": "Quelle est la différence entre 2> et 2>&1 ?",
                "expected_answer": "2> redirige stderr (erreurs) vers un fichier, 2>&1 redirige stderr vers stdout. Cela permet de capturer les erreurs avec la sortie normale ou de les traiter séparément.",
                "technical_terms": ["stderr", "stdout", "2>", "2>&1", "redirection", "erreurs", "descripteur de fichier"],
                "explanation": "La gestion séparée des flux d'erreur et de sortie normale permet un meilleur contrôle du traitement des résultats.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            11: {
                "question_id": 11,
                "question_text": "Comment rechercher un mot dans des fichiers avec grep ?",
                "expected_answer": "grep 'mot' fichier recherche dans un fichier, grep -r 'mot' dossier/ recherche récursivement, grep -i pour ignorer la casse, grep -n pour afficher les numéros de lignes.",
                "technical_terms": ["grep", "recherche", "récursif", "-r", "-i", "-n", "casse", "numéros de lignes", "pattern"],
                "explanation": "grep est un outil puissant de recherche textuelle avec de nombreuses options pour affiner les résultats.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            12: {
                "question_id": 12,
                "question_text": "Comment utiliser find pour localiser des fichiers ?",
                "expected_answer": "find /chemin -name 'pattern' trouve par nom, find . -type f pour les fichiers seulement, find . -size +1M pour les fichiers > 1MB, find . -mtime -7 pour les fichiers modifiés dans les 7 derniers jours.",
                "technical_terms": ["find", "-name", "-type", "-size", "-mtime", "pattern", "fichiers", "répertoires", "critères"],
                "explanation": "find permet des recherches complexes basées sur divers critères : nom, type, taille, date de modification, permissions...",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            13: {
                "question_id": 13,
                "question_text": "Expliquez l'utilisation de head, tail et less.",
                "expected_answer": "head affiche les premières lignes d'un fichier (défaut 10), tail les dernières lignes, less permet de naviguer dans un fichier page par page. tail -f suit un fichier en temps réel.",
                "technical_terms": ["head", "tail", "less", "premières lignes", "dernières lignes", "navigation", "tail -f", "temps réel"],
                "explanation": "Ces outils permettent d'examiner des fichiers de différentes manières selon les besoins : aperçu, fin de logs, lecture complète.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            14: {
                "question_id": 14,
                "question_text": "Comment combiner plusieurs commandes avec && et || ?",
                "expected_answer": "&& exécute la commande suivante seulement si la précédente réussit (code de retour 0), || exécute si la précédente échoue. Exemple : make && make install || echo 'Échec'",
                "technical_terms": ["&&", "||", "code de retour", "succès", "échec", "enchaînement conditionnel", "make"],
                "explanation": "Ces opérateurs permettent un contrôle de flux conditionnel basé sur le succès ou l'échec des commandes précédentes.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            }
        }
    }
}

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

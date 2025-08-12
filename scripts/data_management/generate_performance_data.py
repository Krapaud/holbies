#!/usr/bin/env python3
"""
Script pour générer des données de test de performance réalistes
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User, QuizSession, AIQuizSession, Question, UserActivity
from app.performance_service import get_performance_service

def create_sample_questions():
    """Crée quelques questions d'exemple"""
    db = SessionLocal()
    try:
        # Vérifier s'il y a déjà des questions
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print(f"✅ {existing_questions} questions déjà présentes")
            return
        
        print("📝 Création de questions d'exemple...")
        
        sample_questions = [
            {
                "question_text": "Qu'est-ce que Python ?",
                "option_a": "Un serpent",
                "option_b": "Un langage de programmation",
                "option_c": "Un framework web",
                "option_d": "Une base de données",
                "correct_answer": "b",
                "explanation": "Python est un langage de programmation interprété et orienté objet.",
                "difficulty": "easy",
                "category": "programming"
            },
            {
                "question_text": "Que signifie HTML ?",
                "option_a": "HyperText Markup Language",
                "option_b": "High Tech Modern Language",
                "option_c": "Home Tool Markup Language",
                "option_d": "Hyperlink and Text Markup Language",
                "correct_answer": "a",
                "explanation": "HTML signifie HyperText Markup Language.",
                "difficulty": "easy",
                "category": "web"
            },
            {
                "question_text": "Quelle est la complexité temporelle d'une recherche dans un arbre binaire de recherche équilibré ?",
                "option_a": "O(1)",
                "option_b": "O(log n)",
                "option_c": "O(n)",
                "option_d": "O(n²)",
                "correct_answer": "b",
                "explanation": "Dans un arbre binaire de recherche équilibré, la recherche s'effectue en O(log n).",
                "difficulty": "medium",
                "category": "algorithms"
            },
            {
                "question_text": "Quel pattern de design garantit qu'une classe n'a qu'une seule instance ?",
                "option_a": "Factory",
                "option_b": "Observer",
                "option_c": "Singleton",
                "option_d": "Strategy",
                "correct_answer": "c",
                "explanation": "Le pattern Singleton garantit qu'une classe n'a qu'une seule instance.",
                "difficulty": "medium",
                "category": "design_patterns"
            },
            {
                "question_text": "Qu'est-ce que la programmation fonctionnelle ?",
                "option_a": "Programmer des fonctions uniquement",
                "option_b": "Un paradigme basé sur l'évaluation de fonctions mathématiques",
                "option_c": "Programmer sans classes",
                "option_d": "Utiliser seulement des fonctions natives",
                "correct_answer": "b",
                "explanation": "La programmation fonctionnelle est un paradigme basé sur l'évaluation de fonctions mathématiques et évite les changements d'état.",
                "difficulty": "hard",
                "category": "programming"
            }
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"✅ {len(sample_questions)} questions créées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des questions: {e}")
        db.rollback()
    finally:
        db.close()

def generate_sample_quiz_sessions():
    """Génère des sessions de quiz avec des données réalistes"""
    db = SessionLocal()
    performance_service = get_performance_service()
    
    try:
        print("🎯 Génération de sessions de quiz...")
        
        # Récupérer tous les utilisateurs
        users = db.query(User).all()
        questions = db.query(Question).all()
        
        if not users:
            print("❌ Aucun utilisateur trouvé")
            return
        
        if not questions:
            print("❌ Aucune question trouvée")
            return
        
        sessions_created = 0
        
        for user in users:
            # Générer entre 3 et 15 sessions par utilisateur
            num_sessions = random.randint(3, 15)
            
            for i in range(num_sessions):
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                session_date = datetime.now() - timedelta(days=days_ago)
                
                # Nombre de questions par session (5 à 10)
                num_questions = random.randint(5, min(10, len(questions)))
                selected_questions = random.sample(questions, num_questions)
                
                # Calculer un score basé sur la difficulté et un facteur de réussite simulé
                user_skill_level = random.uniform(0.3, 0.9)  # Niveau de compétence simulé
                correct_answers = 0
                
                for question in selected_questions:
                    # Probabilité de réussite basée sur la difficulté et le niveau de l'utilisateur
                    if question.difficulty == "easy":
                        success_rate = user_skill_level * 0.9
                    elif question.difficulty == "medium":
                        success_rate = user_skill_level * 0.7
                    else:  # hard
                        success_rate = user_skill_level * 0.5
                    
                    if random.random() < success_rate:
                        correct_answers += 1
                
                # Créer la session
                quiz_session = QuizSession(
                    user_id=user.id,
                    score=correct_answers,
                    total_questions=num_questions,
                    completed=True,
                    started_at=session_date,
                    completed_at=session_date + timedelta(minutes=random.randint(5, 30))
                )
                
                db.add(quiz_session)
                sessions_created += 1
                
                # Log d'activité
                performance_service.log_user_activity(
                    user.id,
                    "quiz_completed",
                    {
                        "score": correct_answers,
                        "total_questions": num_questions,
                        "percentage": (correct_answers / num_questions) * 100
                    }
                )
        
        db.commit()
        print(f"✅ {sessions_created} sessions de quiz créées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des sessions: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        performance_service.close()

def generate_sample_ai_quiz_sessions():
    """Génère des sessions d'AI quiz avec des données réalistes"""
    db = SessionLocal()
    performance_service = get_performance_service()
    
    try:
        print("🤖 Génération de sessions d'AI quiz...")
        
        users = db.query(User).all()
        
        if not users:
            print("❌ Aucun utilisateur trouvé")
            return
        
        sessions_created = 0
        
        for user in users:
            # Générer entre 2 et 8 sessions AI par utilisateur
            num_sessions = random.randint(2, 8)
            
            for i in range(num_sessions):
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                session_date = datetime.now() - timedelta(days=days_ago)
                
                # Nombre de questions par session (3 à 7)
                num_questions = random.randint(3, 7)
                
                # Score total simulé (plus variable que les quiz classiques)
                user_ai_skill = random.uniform(0.2, 0.8)
                total_score = 0
                
                for q in range(num_questions):
                    # Score par question (0 à 100)
                    question_score = random.gauss(user_ai_skill * 100, 20)
                    question_score = max(0, min(100, question_score))  # Limiter entre 0 et 100
                    total_score += question_score
                
                # Créer la session AI
                ai_session = AIQuizSession(
                    user_id=user.id,
                    total_score=total_score,
                    total_questions=num_questions,
                    completed=True,
                    started_at=session_date,
                    completed_at=session_date + timedelta(minutes=random.randint(10, 45))
                )
                
                db.add(ai_session)
                sessions_created += 1
                
                # Log d'activité
                performance_service.log_user_activity(
                    user.id,
                    "ai_quiz_completed",
                    {
                        "total_score": total_score,
                        "total_questions": num_questions,
                        "average_score": total_score / num_questions
                    }
                )
        
        db.commit()
        print(f"✅ {sessions_created} sessions d'AI quiz créées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des sessions AI: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        performance_service.close()

def generate_user_activities():
    """Génère des activités utilisateur diverses"""
    db = SessionLocal()
    performance_service = get_performance_service()
    
    try:
        print("📱 Génération d'activités utilisateur...")
        
        users = db.query(User).all()
        
        if not users:
            print("❌ Aucun utilisateur trouvé")
            return
        
        activities_created = 0
        activity_types = ["login", "page_view", "quiz_start", "ai_quiz_start", "logout"]
        
        for user in users:
            # Générer des activités pour les 30 derniers jours
            for day in range(30):
                # Probabilité d'activité par jour
                if random.random() < 0.6:  # 60% de chance d'activité par jour
                    date = datetime.now() - timedelta(days=day)
                    
                    # Nombre d'activités dans la journée
                    daily_activities = random.randint(1, 8)
                    
                    for _ in range(daily_activities):
                        activity_time = date.replace(
                            hour=random.randint(8, 22),
                            minute=random.randint(0, 59),
                            second=random.randint(0, 59)
                        )
                        
                        activity_type = random.choice(activity_types)
                        
                        performance_service.log_user_activity(
                            user.id,
                            activity_type,
                            {"timestamp": activity_time.isoformat()}
                        )
                        activities_created += 1
        
        print(f"✅ {activities_created} activités générées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des activités: {e}")
        import traceback
        traceback.print_exc()
    finally:
        performance_service.close()

def main():
    """Fonction principale pour générer toutes les données de test"""
    print("🚀 GÉNÉRATION DE DONNÉES DE PERFORMANCE")
    print("=" * 50)
    
    # 1. Créer les questions d'exemple
    create_sample_questions()
    
    # 2. Générer les sessions de quiz
    generate_sample_quiz_sessions()
    
    # 3. Générer les sessions d'AI quiz
    generate_sample_ai_quiz_sessions()
    
    # 4. Générer les activités utilisateur
    generate_user_activities()
    
    print("\n🎯 GÉNÉRATION TERMINÉE")
    print("=" * 30)
    
    # Afficher un résumé
    db = SessionLocal()
    try:
        quiz_sessions = db.query(QuizSession).count()
        ai_sessions = db.query(AIQuizSession).count()
        activities = db.query(UserActivity).count()
        questions = db.query(Question).count()
        
        print(f"📊 Questions: {questions}")
        print(f"🎯 Sessions Quiz: {quiz_sessions}")
        print(f"🤖 Sessions AI Quiz: {ai_sessions}")
        print(f"📱 Activités: {activities}")
        print(f"\n✅ Données de performance générées avec succès!")
        print(f"🌐 Testez les analytics: http://localhost:8000/api/performance/analytics")
        
    except Exception as e:
        print(f"❌ Erreur lors du résumé: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

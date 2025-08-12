#!/usr/bin/env python3
"""
Script pour supprimer toutes les données PLD (AI Quiz) existantes
Supprime les sessions et réponses AI Quiz de tous les utilisateurs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import DATABASE_URL, Base
from app.models import AIQuizSession, AIQuizAnswer, UserPerformanceStats

def clear_pld_data():
    """Supprime toutes les données PLD de la base de données"""
    
    # Créer la connexion à la base de données
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🗑️  Suppression des données PLD en cours...")
        
        # Compter les données avant suppression
        ai_answers_count = db.query(AIQuizAnswer).count()
        ai_sessions_count = db.query(AIQuizSession).count()
        
        print(f"📊 Données trouvées:")
        print(f"   - Sessions AI Quiz: {ai_sessions_count}")
        print(f"   - Réponses AI Quiz: {ai_answers_count}")
        
        if ai_answers_count == 0 and ai_sessions_count == 0:
            print("✅ Aucune donnée PLD à supprimer.")
            return
        
        # Supprimer les réponses AI Quiz en premier (contraintes de clés étrangères)
        if ai_answers_count > 0:
            db.query(AIQuizAnswer).delete()
            print(f"🗑️  {ai_answers_count} réponses AI Quiz supprimées")
        
        # Supprimer les sessions AI Quiz
        if ai_sessions_count > 0:
            db.query(AIQuizSession).delete()
            print(f"🗑️  {ai_sessions_count} sessions AI Quiz supprimées")
        
        # Réinitialiser les statistiques AI Quiz dans UserPerformanceStats
        stats_updated = db.query(UserPerformanceStats).filter(
            (UserPerformanceStats.ai_quiz_sessions_completed > 0) |
            (UserPerformanceStats.ai_quiz_total_score > 0) |
            (UserPerformanceStats.ai_quiz_total_questions > 0)
        ).update({
            UserPerformanceStats.ai_quiz_sessions_completed: 0,
            UserPerformanceStats.ai_quiz_total_score: 0.0,
            UserPerformanceStats.ai_quiz_total_questions: 0,
            UserPerformanceStats.ai_quiz_average_score: 0.0,
            UserPerformanceStats.ai_quiz_best_score: 0.0,
            UserPerformanceStats.ai_quiz_time_spent_minutes: 0
        })
        
        if stats_updated > 0:
            print(f"📊 Statistiques PLD réinitialisées pour {stats_updated} utilisateur(s)")
        
        # Valider les changements
        db.commit()
        
        print("✅ Suppression des données PLD terminée avec succès!")
        print("📝 Les nouvelles questions par catégories peuvent maintenant être ajoutées.")
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Script de suppression des données PLD")
    print("=" * 50)
    
    response = input("⚠️  Êtes-vous sûr de vouloir supprimer TOUTES les données PLD ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'oui']:
        clear_pld_data()
    else:
        print("❌ Suppression annulée.")

#!/usr/bin/env python3
"""
Script pour réinitialiser complètement la base de données
"""

from app.database import engine, Base
from app.models import User, Question, QuizSession, QuizAnswer

def reset_database():
    """Supprime et recrée toutes les tables"""
    print("🔄 Réinitialisation complète de la base de données...")
    try:
        # Supprime toutes les tables
        print("  📋 Suppression des tables existantes...")
        Base.metadata.drop_all(bind=engine)
        print("  ✅ Tables supprimées")
        
        # Recrée toutes les tables
        print("  🔨 Création des nouvelles tables...")
        Base.metadata.create_all(bind=engine)
        print("  ✅ Tables créées")
        
        print("\n✅ Base de données réinitialisée avec succès!")
        print("\nTables disponibles:")
        print("  - users (utilisateurs)")
        print("  - questions (questions de quiz)")
        print("  - quiz_sessions (sessions de quiz)")
        print("  - quiz_answers (réponses de quiz)")
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        raise

if __name__ == "__main__":
    reset_database()

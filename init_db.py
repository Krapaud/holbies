#!/usr/bin/env python3
"""
Script pour initialiser la base de données avec les tables nécessaires
"""

from app.database import engine, Base
from app.models import User, Question, QuizSession, QuizAnswer

def init_database():
    """Crée toutes les tables dans la base de données"""
    print("🔄 Création des tables de base de données...")
    try:
        # Crée toutes les tables définies dans les modèles
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès!")
        print("\nTables disponibles:")
        print("  - users (utilisateurs)")
        print("  - questions (questions de quiz)")
        print("  - quiz_sessions (sessions de quiz)")
        print("  - quiz_answers (réponses de quiz)")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        raise

if __name__ == "__main__":
    init_database()

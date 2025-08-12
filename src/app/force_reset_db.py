#!/usr/bin/env python3
"""
Script pour supprimer toutes les tables PostgreSQL avec CASCADE
"""

import psycopg2
from sqlalchemy import text
from app.database import engine, Base
from app.models import User, Question, QuizSession, QuizAnswer

def force_reset_database():
    """Force la suppression de toutes les tables avec CASCADE"""
    print("🔄 Nettoyage forcé de la base de données...")
    
    try:
        # Connexion directe pour supprimer toutes les tables
        with engine.connect() as connection:
            print("  🗑️  Suppression forcée de toutes les tables...")
            
            # Récupère toutes les tables existantes
            result = connection.execute(text("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public';
            """))
            
            tables = [row[0] for row in result]
            print(f"  📋 Tables trouvées: {tables}")
            
            # Supprime chaque table avec CASCADE
            for table in tables:
                try:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
                    print(f"    ✅ {table} supprimée")
                except Exception as e:
                    print(f"    ⚠️  Erreur avec {table}: {e}")
            
            connection.commit()
            print("  ✅ Toutes les tables supprimées")
        
        # Recrée les tables avec le bon schéma
        print("  🔨 Création des nouvelles tables...")
        Base.metadata.create_all(bind=engine)
        print("  ✅ Nouvelles tables créées")
        
        print("\n🎉 Base de données complètement réinitialisée!")
        print("\nTables disponibles:")
        print("  - users (utilisateurs)")
        print("  - questions (questions de quiz)")
        print("  - quiz_sessions (sessions de quiz)")
        print("  - quiz_answers (réponses de quiz)")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage forcé: {e}")
        raise

if __name__ == "__main__":
    force_reset_database()

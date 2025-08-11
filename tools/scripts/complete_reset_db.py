import psycopg2
from sqlalchemy import create_engine, text
from app.database import DATABASE_URL, Base
from app.models import User, Question, QuizSession, QuizAnswer

def complete_reset_database():
    """Réinitialisation complète de la base de données"""
    try:
        # Connexion directe avec psycopg2 pour supprimer toutes les tables
        conn = psycopg2.connect(
            host="localhost",
            database="holbies_db",
            user="username", 
            password="password"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Suppression de toutes les tables...")
        # Supprimer toutes les tables publiques
        cur.execute("""
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
            GRANT ALL ON SCHEMA public TO postgres;
            GRANT ALL ON SCHEMA public TO public;
        """)
        
        cur.close()
        conn.close()
        print("✅ Schéma public complètement réinitialisé")
        
        # Recréer toutes les tables avec SQLAlchemy
        print("Création des nouvelles tables...")
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
        
        # Vérifier la structure de la table users
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name='users' 
                ORDER BY ordinal_position
            """))
            
            print("\n📋 Structure de la table users:")
            for row in result:
                print(f"  - {row[0]}: {row[1]}")
        
        engine.dispose()
        print("\n🎉 Base de données complètement réinitialisée !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    complete_reset_database()

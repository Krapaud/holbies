from sqlalchemy import create_engine, text
from app.database import DATABASE_URL, Base
from app.models import User, Question, QuizSession, QuizAnswer

def reset_with_sqlalchemy():
    """Réinitialisation de la base de données avec SQLAlchemy uniquement"""
    try:
        print(f"Connexion à la base: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        
        # Supprimer toutes les tables existantes
        print("Suppression des tables existantes...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables supprimées")
        
        # Recréer toutes les tables
        print("Création des nouvelles tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées")
        
        # Vérifier la structure de la table users
        with engine.connect() as connection:
            try:
                result = connection.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name='users' 
                    ORDER BY ordinal_position
                """))
                
                print("\n📋 Structure de la table users:")
                for row in result:
                    print(f"  - {row[0]}: {row[1]}")
                    
            except Exception as e:
                print(f"Erreur lors de la vérification: {e}")
        
        engine.dispose()
        print("\n🎉 Base de données réinitialisée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_with_sqlalchemy()

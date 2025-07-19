"""
Script de migration SQLite vers PostgreSQL
Transfère toutes les données existantes vers la nouvelle base PostgreSQL
"""

import sqlite3
import bcrypt
from sqlalchemy.orm import Session
from database import engine, User, QuizScore, create_tables
from datetime import datetime

def migrate_data():
    """Migrer les données de SQLite vers PostgreSQL"""
    print("🚀 Début de la migration SQLite → PostgreSQL")
    
    # Créer les tables PostgreSQL
    create_tables()
    
    # Connexion SQLite
    sqlite_conn = sqlite3.connect('users.db')
    sqlite_conn.row_factory = sqlite3.Row
    
    # Session PostgreSQL
    with Session(engine) as pg_session:
        try:
            # Migrer les utilisateurs
            print("👥 Migration des utilisateurs...")
            sqlite_users = sqlite_conn.execute('SELECT * FROM users').fetchall()
            
            for sqlite_user in sqlite_users:
                # Convertir le hash SHA-256 en bcrypt (plus sécurisé)
                # Note: Impossible de récupérer le mot de passe original
                # Les utilisateurs devront utiliser un mot de passe temporaire
                temp_password = "matrix2025"  # Mot de passe temporaire
                password_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Gérer les colonnes qui peuvent ne pas exister
                try:
                    is_admin = bool(sqlite_user['is_admin'])
                except (KeyError, IndexError):
                    is_admin = False
                
                try:
                    created_at = datetime.fromisoformat(sqlite_user['created_at'])
                except (KeyError, IndexError, ValueError):
                    created_at = datetime.now()
                
                pg_user = User(
                    username=sqlite_user['username'],
                    email=sqlite_user['email'],
                    password_hash=password_hash,
                    is_admin=is_admin,
                    created_at=created_at
                )
                pg_session.add(pg_user)
            
            # Commit des utilisateurs d'abord pour avoir les IDs
            pg_session.commit()
            print(f"✅ {len(sqlite_users)} utilisateurs migrés")
            
            # Migrer les scores de quiz s'ils existent
            try:
                sqlite_scores = sqlite_conn.execute('SELECT * FROM quiz_scores').fetchall()
                print("🧠 Migration des scores de quiz...")
                
                for sqlite_score in sqlite_scores:
                    # Trouver l'utilisateur correspondant dans PostgreSQL
                    pg_user = pg_session.query(User).filter(User.id == sqlite_score['user_id']).first()
                    if pg_user:
                        try:
                            date_taken = datetime.fromisoformat(sqlite_score['date_taken'])
                        except (KeyError, IndexError, ValueError):
                            date_taken = datetime.now()
                            
                        pg_score = QuizScore(
                            user_id=pg_user.id,
                            category=sqlite_score['category'],
                            score=sqlite_score['score'],
                            total_questions=sqlite_score['total_questions'],
                            date_taken=date_taken
                        )
                        pg_session.add(pg_score)
                
                pg_session.commit()
                print(f"✅ {len(sqlite_scores)} scores de quiz migrés")
                
            except sqlite3.OperationalError:
                print("ℹ️ Aucune table quiz_scores trouvée dans SQLite")
            
            print("🎉 Migration terminée avec succès!")
            print("\n⚠️  IMPORTANT: Tous les utilisateurs ont maintenant le mot de passe temporaire: 'matrix2025'")
            print("   Ils devront se connecter avec ce mot de passe et le changer.")
            
        except Exception as e:
            pg_session.rollback()
            print(f"❌ Erreur lors de la migration: {e}")
            raise
        
    sqlite_conn.close()

def create_admin_user():
    """Créer un utilisateur admin par défaut"""
    with Session(engine) as session:
        # Vérifier si un admin existe déjà
        admin_exists = session.query(User).filter(User.is_admin == True).first()
        
        if not admin_exists:
            admin_password = "admin_matrix_2025"
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            admin_user = User(
                username="admin",
                email="admin@devhub.matrix",
                password_hash=password_hash,
                is_admin=True,
                created_at=datetime.now()
            )
            session.add(admin_user)
            session.commit()
            
            print(f"👑 Utilisateur admin créé:")
            print(f"   Username: admin")
            print(f"   Password: {admin_password}")
            print(f"   Email: admin@devhub.matrix")

if __name__ == "__main__":
    migrate_data()
    create_admin_user()

"""
Script de diagnostic pour tester l'authentification PostgreSQL
"""

import bcrypt
from database import SessionLocal, User

def test_auth():
    with SessionLocal() as db:
        print("=== Test authentification PostgreSQL ===")
        
        # Lister tous les utilisateurs
        users = db.query(User).all()
        print(f"\nUtilisateurs en base: {len(users)}")
        for user in users:
            print(f"- {user.username} | {user.email} | Admin: {user.is_admin}")
        
        # Test avec admin
        admin = db.query(User).filter(User.username == 'admin').first()
        if admin:
            print(f"\nAdmin trouvé: {admin.username}")
            print(f"Hash stocké: {admin.password_hash[:50]}...")
            
            # Tests de mots de passe
            passwords_to_test = ['matrix2025', 'admin_matrix_2025', 'admin']
            for pwd in passwords_to_test:
                try:
                    is_valid = bcrypt.checkpw(pwd.encode('utf-8'), admin.password_hash.encode('utf-8'))
                    print(f"Mot de passe '{pwd}': {'✅ VALIDE' if is_valid else '❌ INVALIDE'}")
                except Exception as e:
                    print(f"Erreur avec '{pwd}': {e}")
        
        # Créer un nouvel admin avec mot de passe connu
        test_admin = db.query(User).filter(User.username == 'testadmin').first()
        if not test_admin:
            password = 'test123'
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            test_admin = User(
                username='testadmin',
                email='testadmin@test.com',
                password_hash=password_hash,
                is_admin=True
            )
            db.add(test_admin)
            db.commit()
            print(f"\n✅ Utilisateur de test créé: testadmin / {password}")

if __name__ == "__main__":
    test_auth()

#!/usr/bin/env python3
"""
Script pour créer automatiquement des données de test avec des utilisateurs admin et standard
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

# Configuration du hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash un mot de passe"""
    return pwd_context.hash(password)

def create_admin_and_users():
    """Crée un admin et plusieurs utilisateurs de test"""
    db = SessionLocal()
    
    try:
        print("🧪 CRÉATION DES UTILISATEURS DE TEST")
        print("=" * 40)
        
        # Données de test avec admins et utilisateurs
        test_users = [
            ("admin", "admin@holbies.dev", "admin123", True, "👑 Administrateur principal"),
            ("teacher", "teacher@holbies.dev", "teacher123", True, "👑 Enseignant admin"),
            ("student1", "student1@holbies.dev", "student123", False, "👤 Étudiant 1"),
            ("student2", "student2@holbies.dev", "student123", False, "👤 Étudiant 2"),
            ("student3", "student3@holbies.dev", "student123", False, "👤 Étudiant 3"),
            ("demo_user", "demo@holbies.dev", "demo123", False, "👤 Utilisateur démo"),
            ("test_user", "test@holbies.dev", "test123", False, "👤 Utilisateur test"),
            ("guest", "guest@holbies.dev", "guest123", False, "👤 Invité"),
        ]
        
        created_count = 0
        for username, email, password, is_admin, description in test_users:
            # Vérifier si l'utilisateur existe déjà
            existing = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing:
                print(f"⏭️  {username} existe déjà, ignoré")
                continue
            
            # Créer l'utilisateur
            hashed_pwd = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                hashed_password=hashed_pwd,
                is_active=True
            )
            
            db.add(new_user)
            db.flush()  # Pour obtenir l'ID
            
            # Ajouter le statut admin via SQL direct
            try:
                db.execute(text("UPDATE users SET is_admin = :is_admin WHERE id = :id"), 
                          {"is_admin": is_admin, "id": new_user.id})
            except Exception as e:
                print(f"⚠️  Erreur lors de la mise à jour admin pour {username}: {e}")
            
            created_count += 1
            print(f"✅ {username:12s} | {description}")
        
        db.commit()
        
        print(f"\n🎯 RÉSUMÉ:")
        print(f"   ✨ {created_count} utilisateur(s) créé(s)")
        
        # Afficher les statistiques finales
        total_users = db.query(User).count()
        try:
            admin_result = db.execute(text("SELECT COUNT(*) FROM users WHERE is_admin = true")).fetchone()
            admin_count = admin_result[0] if admin_result else 0
        except:
            admin_count = 0
        
        print(f"   👥 Total utilisateurs: {total_users}")
        print(f"   👑 Administrateurs: {admin_count}")
        print(f"   👤 Utilisateurs standard: {total_users - admin_count}")
        
        print(f"\n🔑 IDENTIFIANTS DE CONNEXION:")
        print("   👑 admin / admin123 (Administrateur)")
        print("   👑 teacher / teacher123 (Enseignant admin)")
        print("   👤 student1 / student123 (Étudiant)")
        print("   👤 demo_user / demo123 (Démo)")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_and_users()

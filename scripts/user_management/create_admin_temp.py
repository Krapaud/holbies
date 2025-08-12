#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur
"""

import sys
import os
import getpass

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash, get_user_by_username, get_user_by_email

def create_admin_user():
    """Crée un utilisateur administrateur"""
    db = SessionLocal()
    
    try:
        print("🔧 Création d'un utilisateur administrateur")
        print("=" * 50)
        
        # Créer un admin par défaut
        username = "admin"
        email = "admin@holbies.dev"
        password = "admin123"
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"✅ Un utilisateur admin existe déjà: {existing_user.username} ({existing_user.email})")
            return
            
        existing_email = get_user_by_email(db, email)
        if existing_email:
            print(f"✅ Un utilisateur avec cet email existe déjà: {existing_email.username} ({existing_email.email})")
            return
        
        # Créer l'utilisateur
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Utilisateur administrateur '{username}' créé avec succès!")
        print(f"📧 Email: {email}")
        print(f"🔑 Mot de passe: {password}")
        print(f"🆔 ID: {admin_user.id}")
        print("\n🎉 Vous pouvez maintenant vous connecter avec ces identifiants!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

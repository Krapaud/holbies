#!/usr/bin/env python3
"""
Script pour créer un utilisateur administrateur
"""

import sys
import os
import getpass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        
        # Demander les informations
        username = input("Nom d'utilisateur: ").strip()
        if not username:
            print("❌ Le nom d'utilisateur ne peut pas être vide!")
            return
            
        email = input("Email: ").strip()
        if not email:
            print("❌ L'email ne peut pas être vide!")
            return
            
        password = getpass.getpass("Mot de passe: ")
        if len(password) < 6:
            print("❌ Le mot de passe doit faire au moins 6 caractères!")
            return
            
        confirm_password = getpass.getpass("Confirmer le mot de passe: ")
        if password != confirm_password:
            print("❌ Les mots de passe ne correspondent pas!")
            return
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"❌ Un utilisateur avec le nom '{username}' existe déjà!")
            return
            
        existing_email = get_user_by_email(db, email)
        if existing_email:
            print(f"❌ Un utilisateur avec l'email '{email}' existe déjà!")
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
        print(f"🆔 ID: {admin_user.id}")
        print("\n🎉 Vous pouvez maintenant vous connecter avec ces identifiants!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

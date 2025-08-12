#!/usr/bin/env python3
"""
Script pour créer des utilisateurs de test
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash, get_user_by_username, get_user_by_email

def create_test_users():
    """Crée des utilisateurs de test"""
    db = SessionLocal()
    
    test_users = [
        {"username": "student1", "email": "student1@holbies.dev", "password": "student123"},
        {"username": "student2", "email": "student2@holbies.dev", "password": "student123"},
        {"username": "john_doe", "email": "john.doe@example.com", "password": "john123"},
        {"username": "alice_smith", "email": "alice.smith@example.com", "password": "alice123"},
        {"username": "bob_wilson", "email": "bob.wilson@example.com", "password": "bob123"},
        {"username": "marie_dupont", "email": "marie.dupont@example.com", "password": "marie123"},
        {"username": "dev_test", "email": "dev@test.com", "password": "dev123"}
    ]
    
    try:
        print("🔧 Création d'utilisateurs de test")
        print("=" * 50)
        
        created_count = 0
        for user_data in test_users:
            username = user_data["username"]
            email = user_data["email"]
            password = user_data["password"]
            
            # Vérifier si l'utilisateur existe déjà
            existing_user = get_user_by_username(db, username)
            if existing_user:
                print(f"⚠️  L'utilisateur '{username}' existe déjà")
                continue
                
            existing_email = get_user_by_email(db, email)
            if existing_email:
                print(f"⚠️  L'email '{email}' est déjà utilisé")
                continue
            
            # Créer l'utilisateur
            hashed_password = get_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print(f"✅ Utilisateur '{username}' créé (ID: {new_user.id})")
            created_count += 1
        
        print(f"\n🎉 {created_count} utilisateurs de test créés avec succès!")
        print("\n📋 Identifiants de connexion:")
        print("  - Username: [nom_utilisateur] | Password: [password correspondant]")
        print("  - Exemple: student1 / student123")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()

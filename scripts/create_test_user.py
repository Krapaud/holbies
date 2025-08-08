#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test pour le Quiz IA
"""

import sys
import os
from sqlalchemy.orm import Session

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db, engine
from app.models import User
from app.auth import get_password_hash

def create_test_user():
    """Créer un utilisateur de test"""
    
    # Créer une session de base de données
    db = Session(engine)
    
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("✅ L'utilisateur de test existe déjà !")
            print(f"   Username: testuser")
            print(f"   Email: {existing_user.email}")
            print(f"   Mot de passe: test123")
            return
        
        # Créer l'utilisateur de test
        hashed_password = get_password_hash("test123")
        test_user = User(
            username="testuser",
            email="test@holbies.com",
            first_name="Test",
            last_name="User", 
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("🎉 Utilisateur de test créé avec succès !")
        print(f"   Username: testuser")
        print(f"   Email: test@holbies.com")
        print(f"   Mot de passe: test123")
        print(f"   ID: {test_user.id}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()

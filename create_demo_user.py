#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test rapidement
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import get_db, User
import bcrypt

def create_test_user():
    db = next(get_db())
    
    # Vérifier si l'utilisateur existe déjà
    existing = db.query(User).filter(User.username == 'demo').first()
    if existing:
        print("Utilisateur 'demo' existe déjà")
        print(f"Email: {existing.email}")
        print(f"Admin: {'Oui' if existing.is_admin else 'Non'}")
        return
    
    # Créer un nouvel utilisateur
    password = 'demo123'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = User(
        username='demo',
        email='demo@matrix.com',
        password_hash=hashed.decode('utf-8'),
        is_admin=True
    )
    
    db.add(user)
    db.commit()
    
    print("✅ Utilisateur de démonstration créé !")
    print("Username: demo")
    print("Password: demo123")
    print("Admin: Oui")

if __name__ == "__main__":
    create_test_user()

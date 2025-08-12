#!/usr/bin/env python3
"""
Script pour lister tous les utilisateurs
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def list_users():
    """Liste tous les utilisateurs"""
    db = SessionLocal()
    
    try:
        users = db.query(User).order_by(User.id).all()
        
        print("👥 LISTE DES UTILISATEURS")
        print("=" * 80)
        print(f"📊 Total: {len(users)} utilisateur(s)")
        print()
        
        if not users:
            print("Aucun utilisateur trouvé.")
            return
        
        for user in users:
            status = "✅ Actif" if user.is_active else "❌ Inactif"
            created = user.created_at.strftime("%d/%m/%Y %H:%M") if user.created_at else "N/A"
            
            print(f"👤 ID: {user.id}")
            print(f"   📝 Username: {user.username}")
            print(f"   📧 Email: {user.email}")
            print(f"   {status}")
            print(f"   📅 Créé le: {created}")
            print("-" * 50)
        
        print(f"\n🎯 Résumé:")
        active_users = len([u for u in users if u.is_active])
        inactive_users = len(users) - active_users
        print(f"   ✅ Utilisateurs actifs: {active_users}")
        print(f"   ❌ Utilisateurs inactifs: {inactive_users}")
        
        # Afficher les identifiants de connexion pour les tests
        print(f"\n🔑 Identifiants de test disponibles:")
        test_accounts = [
            ("admin", "admin123", "Administrateur"),
            ("student1", "student123", "Étudiant"),
            ("student2", "student123", "Étudiant"),
            ("john_doe", "john123", "Utilisateur test"),
            ("alice_smith", "alice123", "Utilisateur test"),
            ("bob_wilson", "bob123", "Utilisateur test"),
            ("marie_dupont", "marie123", "Utilisateur test"),
            ("dev_test", "dev123", "Développeur test")
        ]
        
        for username, password, role in test_accounts:
            user_exists = any(u.username == username for u in users)
            if user_exists:
                print(f"   👤 {username:<15} | 🔑 {password:<12} | 📋 {role}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des utilisateurs: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    list_users()

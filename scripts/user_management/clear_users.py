#!/usr/bin/env python3
"""
Script pour vider tous les utilisateurs de la base de données
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User

def clear_all_users():
    """Vide tous les utilisateurs de la base de données"""
    db = SessionLocal()
    
    try:
        # Compter les utilisateurs avant suppression
        user_count = db.query(User).count()
        
        if user_count == 0:
            print("📭 Aucun utilisateur à supprimer.")
            return
        
        print(f"⚠️  ATTENTION: Vous allez supprimer {user_count} utilisateur(s)")
        print("🗑️  Suppression en cours...")
        
        # Supprimer tous les utilisateurs
        deleted_count = db.query(User).delete()
        db.commit()
        
        print(f"✅ {deleted_count} utilisateur(s) supprimé(s) avec succès")
        print("🎯 La base de données des utilisateurs est maintenant vide")
        
        # Vérification
        remaining_users = db.query(User).count()
        if remaining_users == 0:
            print("✅ Vérification: Aucun utilisateur restant")
        else:
            print(f"⚠️  Attention: {remaining_users} utilisateur(s) restant(s)")
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des utilisateurs: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def confirm_deletion():
    """Demande confirmation avant suppression (pour usage interactif)"""
    print("⚠️  ATTENTION: Cette action va supprimer TOUS les utilisateurs!")
    print("Cette action est IRRÉVERSIBLE!")
    
    # En mode script Docker, on confirme automatiquement
    # Pour éviter les problèmes d'input dans le conteneur
    print("🔄 Confirmation automatique en mode conteneur...")
    return True

if __name__ == "__main__":
    print("🗑️  SUPPRESSION DE TOUS LES UTILISATEURS")
    print("=" * 50)
    
    if confirm_deletion():
        clear_all_users()
    else:
        print("❌ Suppression annulée")

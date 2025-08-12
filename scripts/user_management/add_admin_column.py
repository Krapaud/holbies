#!/usr/bin/env python3
"""
Script pour ajouter le champ is_admin aux utilisateurs existants
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy import text
from app.database import SessionLocal

def add_admin_column():
    """Ajoute la colonne is_admin à la table users"""
    db = SessionLocal()
    
    try:
        print("🔧 Ajout de la colonne is_admin...")
        
        # Vérifier si la colonne existe déjà
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='is_admin'
        """)).fetchone()
        
        if result:
            print("✅ La colonne is_admin existe déjà")
            return
        
        # Ajouter la colonne is_admin
        db.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE"))
        db.commit()
        
        print("✅ Colonne is_admin ajoutée avec succès")
        
        # Vérifier que la colonne a été ajoutée
        result = db.execute(text("SELECT COUNT(*) FROM users")).fetchone()
        user_count = result[0] if result else 0
        print(f"📊 {user_count} utilisateur(s) dans la base")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la colonne: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 MIGRATION: Ajout du champ is_admin")
    print("=" * 40)
    add_admin_column()

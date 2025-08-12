#!/usr/bin/env python3
"""
Migration pour créer les tables de statistiques de performance
"""

import sys
import os

# Ajouter le répertoire src au PATH
sys.path.insert(0, '/app/src')

from sqlalchemy import text
from app.database import SessionLocal, engine
from app.models import Base

def create_performance_tables():
    """Crée les tables pour les statistiques de performance"""
    db = SessionLocal()
    
    try:
        print("🔧 MIGRATION: Création des tables de performance")
        print("=" * 50)
        
        # Créer toutes les tables définies dans les modèles
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
        
        # Vérifier les tables créées
        tables_check = [
            "user_performance_stats",
            "daily_system_stats", 
            "user_activities"
        ]
        
        for table in tables_check:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
                print(f"✅ Table {table}: OK ({result[0]} enregistrements)")
            except Exception as e:
                print(f"⚠️  Table {table}: {e}")
        
        print("\n🎯 Migration terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_performance_tables()

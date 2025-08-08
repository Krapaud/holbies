#!/usr/bin/env python3
"""
Script pour créer les tables PostgreSQL
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app.models import Base

def create_tables():
    """Create all database tables"""
    try:
        print(f"Database URL: {engine.url}")
        print("Création des tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables créées avec succès!")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables créées: {tables}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    create_tables()

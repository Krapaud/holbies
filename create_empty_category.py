#!/usr/bin/env python3
"""Créer une catégorie vide pour test"""

import psycopg2
import os

def create_empty_category():
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="holbies",
            user="holbies",
            password="password123"
        )
        cursor = conn.cursor()
        
        # Créer une catégorie vide pour test
        cursor.execute("""
            INSERT INTO pld_categories (name, description) 
            VALUES ('test_empty', 'Catégorie de test vide')
            ON CONFLICT (name) DO NOTHING
        """)
        
        conn.commit()
        print("✅ Catégorie 'test_empty' créée")
        
        # Vérifier qu'elle n'a pas de thèmes
        cursor.execute("""
            SELECT COUNT(*) FROM pld_themes WHERE category_id = (
                SELECT id FROM pld_categories WHERE name = 'test_empty'
            )
        """)
        
        count = cursor.fetchone()[0]
        print(f"📊 Nombre de thèmes dans test_empty: {count}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_empty_category()

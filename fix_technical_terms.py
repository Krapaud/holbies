#!/usr/bin/env python3
"""
Script pour corriger le format JSON des technical_terms
"""
import sys
import json
sys.path.append('/app/src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import PLDQuestion
from app.database import DATABASE_URL

def main():
    # Connexion à la base de données
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔄 Correction du format JSON des technical_terms...")
        
        # Récupérer toutes les questions
        questions = db.query(PLDQuestion).all()
        
        for question in questions:
            print(f"Traitement de la question {question.id}: {question.question_text[:50]}...")
            
            # Vérifier si technical_terms est déjà du JSON valide
            try:
                json.loads(question.technical_terms)
                print(f"  ✅ Déjà en format JSON correct")
                continue
            except json.JSONDecodeError:
                pass
            
            # Si c'est un format PostgreSQL array {item1,item2,item3}
            if question.technical_terms.startswith('{') and question.technical_terms.endswith('}'):
                # Retirer les accolades et diviser par les virgules
                content = question.technical_terms[1:-1]  # Enlever { et }
                if content:
                    terms_list = [term.strip() for term in content.split(',')]
                    # Convertir en JSON
                    question.technical_terms = json.dumps(terms_list)
                    print(f"  ✅ Converti de PostgreSQL array vers JSON: {len(terms_list)} termes")
                else:
                    # Array vide
                    question.technical_terms = json.dumps([])
                    print(f"  ✅ Array vide converti vers JSON")
            else:
                print(f"  ❌ Format non reconnu: {question.technical_terms[:50]}...")
        
        db.commit()
        print("✅ Correction terminée !")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la correction: {e}")
        return 1
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

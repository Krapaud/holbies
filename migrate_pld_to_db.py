#!/usr/bin/env python3
"""
Script pour migrer les questions PLD vers la base de données
"""
import sys
import os
sys.path.append('/home/krapaud/project-holbies/src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import PLDCategory, PLDTheme, PLDQuestion
from app.database import DATABASE_URL

# Questions PLD à insérer
PLD_QUESTIONS = {
    "shell": {
        "permission": [
            {
                "question_text": "Expliquez la différence entre chmod 755 et chmod 644 sur un fichier.",
                "expected_answer": "chmod 755 donne les permissions rwx pour le propriétaire et rx pour le groupe et les autres, tandis que chmod 644 donne rw pour le propriétaire et r pour le groupe et les autres. 755 est typique pour les exécutables, 644 pour les fichiers de données.",
                "technical_terms": ["chmod", "permissions", "rwx", "propriétaire", "groupe", "autres", "octal", "755", "644"],
                "explanation": "Les permissions Unix utilisent 3 bits par catégorie : r(4) + w(2) + x(1). 755 = rwxr-xr-x, 644 = rw-r--r--",
                "difficulty": "medium",
                "max_score": 100
            },
            {
                "question_text": "Comment utiliser sudo et su de manière sécurisée ?",
                "expected_answer": "sudo permet d'exécuter des commandes avec les privilèges d'un autre utilisateur (root par défaut) sans connaître son mot de passe. su change d'utilisateur. Utiliser sudo est plus sécurisé car il garde une trace des actions et permet un contrôle granulaire via /etc/sudoers.",
                "technical_terms": ["sudo", "su", "privilèges", "root", "sudoers", "sécurité", "authentification", "logs"],
                "explanation": "sudo est préférable à su car il offre un meilleur contrôle d'accès et une meilleure traçabilité des actions administratives.",
                "difficulty": "medium",
                "max_score": 100
            },
            {
                "question_text": "Expliquez les permissions spéciales : setuid, setgid et sticky bit.",
                "expected_answer": "setuid (4000) permet à un fichier de s'exécuter avec les privilèges du propriétaire. setgid (2000) avec ceux du groupe. sticky bit (1000) sur un répertoire empêche la suppression de fichiers par d'autres utilisateurs que le propriétaire.",
                "technical_terms": ["setuid", "setgid", "sticky bit", "4000", "2000", "1000", "privilèges", "sécurité", "répertoire"],
                "explanation": "Ces permissions spéciales modifient le comportement standard et ont des implications importantes en sécurité.",
                "difficulty": "hard",
                "max_score": 100
            }
        ],
        "io": [
            {
                "question_text": "Comment rediriger les sorties standard et d'erreur ?",
                "expected_answer": "< redirige l'entrée, > redirige la sortie (écrase), >> ajoute à la fin. 2> redirige stderr, &> redirige stdout et stderr ensemble. | pipe la sortie vers une autre commande.",
                "technical_terms": ["redirection", "stdout", "stderr", "stdin", ">", ">>", "2>", "&>", "|", "pipe"],
                "explanation": "La redirection permet de contrôler les flux d'entrée/sortie et de chaîner les commandes efficacement.",
                "difficulty": "medium",
                "max_score": 100
            },
            {
                "question_text": "Décrivez l'utilisation de grep pour rechercher dans les fichiers.",
                "expected_answer": "grep recherche des patterns dans les fichiers. Options utiles : -r (récursif), -i (ignore la casse), -n (numéros de lignes), -v (inverse), -E (regex étendues). Exemple : grep -rn 'error' /var/log/",
                "technical_terms": ["grep", "recherche", "récursif", "-r", "-i", "-n", "casse", "numéros de lignes", "pattern"],
                "explanation": "grep est un outil puissant de recherche textuelle avec de nombreuses options pour affiner les résultats.",
                "difficulty": "easy",
                "max_score": 100
            }
        ]
    }
}

def main():
    # Connexion à la base de données
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔄 Migration des questions PLD vers la base de données...")
        
        # Supprimer les anciennes données
        db.query(PLDQuestion).delete()
        db.query(PLDTheme).delete()
        db.query(PLDCategory).delete()
        db.commit()
        print("✅ Anciennes données supprimées")
        
        total_questions = 0
        
        # Créer les catégories, thèmes et questions
        for category_name, themes_data in PLD_QUESTIONS.items():
            # Créer la catégorie
            category = PLDCategory(
                name=category_name,
                display_name=category_name.capitalize(),
                description=f"Questions de la catégorie {category_name}"
            )
            db.add(category)
            db.flush()  # Pour obtenir l'ID
            print(f"📁 Catégorie créée: {category_name}")
            
            for theme_name, questions in themes_data.items():
                # Créer le thème
                theme = PLDTheme(
                    name=theme_name,
                    display_name=theme_name.capitalize(),
                    description=f"Questions du thème {theme_name}",
                    category_id=category.id
                )
                db.add(theme)
                db.flush()  # Pour obtenir l'ID
                print(f"  📂 Thème créé: {theme_name}")
                
                for question_data in questions:
                    # Créer la question
                    question = PLDQuestion(
                        question_text=question_data["question_text"],
                        expected_answer=question_data["expected_answer"],
                        technical_terms=question_data["technical_terms"],
                        explanation=question_data["explanation"],
                        difficulty=question_data["difficulty"],
                        max_score=question_data["max_score"],
                        theme_id=theme.id
                    )
                    db.add(question)
                    total_questions += 1
                    print(f"    ❓ Question créée: {question_data['question_text'][:50]}...")
        
        db.commit()
        print(f"✅ Migration terminée ! {total_questions} questions ajoutées.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la migration: {e}")
        return 1
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

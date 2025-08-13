#!/usr/bin/env python3
"""
Script pour créer des données de test PLD
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.database import SessionLocal
from app.models import PLDCategory, PLDTheme, PLDQuestion

def create_test_data():
    db = SessionLocal()
    
    try:
        # Vérifier si des catégories existent déjà
        existing_categories = db.query(PLDCategory).count()
        if existing_categories > 0:
            print(f"Il y a déjà {existing_categories} catégories PLD en base.")
            return
        
        # Créer les catégories
        categories = [
            {"name": "Shell", "description": "Scripts Bash, commandes Unix et système"},
            {"name": "C", "description": "Programmation système, pointeurs et mémoire"},
            {"name": "Python", "description": "Syntaxe Python, structures de données et algorithmes"},
            {"name": "JavaScript", "description": "DOM, événements et programmation asynchrone"},
            {"name": "SQL", "description": "Bases de données, requêtes et optimisation"},
            {"name": "HTML", "description": "Structure et sémantique web"},
            {"name": "CSS", "description": "Styles et mise en page web"},
            {"name": "Git", "description": "Contrôle de version et collaboration"},
            {"name": "Linux", "description": "Administration système et commandes"},
            {"name": "Docker", "description": "Conteneurisation et déploiement"}
        ]
        
        created_categories = []
        for cat_data in categories:
            category = PLDCategory(
                name=cat_data["name"],
                description=cat_data["description"]
            )
            db.add(category)
            db.flush()  # Pour obtenir l'ID
            created_categories.append(category)
            print(f"Créé catégorie: {category.name}")
        
        # Créer quelques thèmes pour chaque catégorie
        themes_data = [
            # Shell
            {"category": created_categories[0], "name": "Variables et paramètres", "description": "Gestion des variables shell"},
            {"category": created_categories[0], "name": "Conditions et boucles", "description": "Structures de contrôle"},
            {"category": created_categories[0], "name": "Commandes système", "description": "Utilisation des outils Unix"},
            
            # C
            {"category": created_categories[1], "name": "Pointeurs", "description": "Gestion de la mémoire"},
            {"category": created_categories[1], "name": "Structures", "description": "Types de données complexes"},
            
            # Python
            {"category": created_categories[2], "name": "Listes et tuples", "description": "Structures de données"},
            {"category": created_categories[2], "name": "Dictionnaires", "description": "Mappages et hash tables"},
            {"category": created_categories[2], "name": "Classes et objets", "description": "Programmation orientée objet"},
            {"category": created_categories[2], "name": "Modules et packages", "description": "Organisation du code"},
            {"category": created_categories[2], "name": "Gestion d'erreurs", "description": "Exceptions et try/catch"},
            
            # JavaScript
            {"category": created_categories[3], "name": "DOM manipulation", "description": "Interaction avec le HTML"},
            {"category": created_categories[3], "name": "Événements", "description": "Gestion des interactions utilisateur"},
            {"category": created_categories[3], "name": "Async/Await", "description": "Programmation asynchrone"},
            {"category": created_categories[3], "name": "Fonctions", "description": "Déclaration et utilisation"},
            
            # SQL
            {"category": created_categories[4], "name": "SELECT queries", "description": "Récupération de données"},
            {"category": created_categories[4], "name": "JOINs", "description": "Jointures entre tables"},
            
            # HTML
            {"category": created_categories[5], "name": "Balises sémantiques", "description": "Structure du document"},
            {"category": created_categories[5], "name": "Formulaires", "description": "Collecte de données"},
            
            # CSS
            {"category": created_categories[6], "name": "Sélecteurs", "description": "Ciblage des éléments"},
            {"category": created_categories[6], "name": "Flexbox", "description": "Mise en page flexible"},
            
            # Git
            {"category": created_categories[7], "name": "Commits", "description": "Sauvegarde des changements"},
            {"category": created_categories[7], "name": "Branches", "description": "Gestion des versions parallèles"},
            
            # Linux
            {"category": created_categories[8], "name": "Permissions", "description": "Gestion des droits d'accès"},
            {"category": created_categories[8], "name": "Processus", "description": "Gestion des tâches système"},
            
            # Docker
            {"category": created_categories[9], "name": "Images", "description": "Création et gestion d'images"},
            {"category": created_categories[9], "name": "Conteneurs", "description": "Exécution d'applications"}
        ]
        
        created_themes = []
        for theme_data in themes_data:
            theme = PLDTheme(
                name=theme_data["name"],
                description=theme_data["description"],
                category_id=theme_data["category"].id
            )
            db.add(theme)
            db.flush()
            created_themes.append(theme)
            print(f"Créé thème: {theme.name} (catégorie: {theme_data['category'].name})")
        
        # Créer quelques questions pour chaque thème
        for i, theme in enumerate(created_themes):
            # Créer 2-8 questions par thème (variable selon l'importance)
            num_questions = [3, 2, 4, 5, 3, 8, 7, 6, 5, 4, 3, 4, 3, 2, 5, 3, 4, 3, 2, 3, 2, 3, 3, 2, 2, 3][i] if i < 26 else 3
            
            for j in range(num_questions):
                question = PLDQuestion(
                    question=f"Question {j+1} sur {theme.name}",
                    answer=f"Réponse {j+1} pour {theme.name}",
                    explanation=f"Explication détaillée pour la question {j+1} du thème {theme.name}",
                    difficulty=["facile", "moyen", "difficile"][j % 3],
                    theme_id=theme.id
                )
                db.add(question)
        
        db.commit()
        print("\n✅ Données de test PLD créées avec succès!")
        
        # Afficher un résumé
        print("\n📊 Résumé:")
        for category in created_categories:
            question_count = db.query(PLDQuestion).join(PLDTheme).filter(
                PLDTheme.category_id == category.id
            ).count()
            print(f"  {category.name}: {question_count} questions")
            
    except Exception as e:
        print(f"Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()

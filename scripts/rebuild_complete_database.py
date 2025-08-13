#!/usr/bin/env python3
"""
Script pour reconstruire complètement la base de données avec toutes les données nécessaires
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.database import SessionLocal, engine
from app.models import Base, User, Question, PLDCategory, PLDTheme, PLDQuestion
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def rebuild_database():
    """Reconstructuire complètement la base de données"""
    print("🔄 Reconstruction complète de la base de données...")
    
    # 1. Supprimer toutes les tables
    print("🗑️ Suppression des tables existantes...")
    Base.metadata.drop_all(bind=engine)
    
    # 2. Recréer toutes les tables
    print("🏗️ Création des nouvelles tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 3. Créer un utilisateur admin
        print("👤 Création de l'utilisateur admin...")
        admin_user = User(
            username="admin",
            email="admin@holbies.com",
            hashed_password=hash_password("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin_user)
        
        # Créer un utilisateur test
        test_user = User(
            username="test",
            email="test@holbies.com", 
            hashed_password=hash_password("test123"),
            is_active=True,
            is_admin=False
        )
        db.add(test_user)
        
        # 4. Créer les catégories PLD
        print("📚 Création des catégories PLD...")
        categories_data = [
            {"name": "shell", "display_name": "Shell", "description": "Scripts Bash, commandes Unix et système", "icon": "SH"},
            {"name": "c", "display_name": "C", "description": "Programmation système, pointeurs et mémoire", "icon": "C"},
            {"name": "python", "display_name": "Python", "description": "Syntaxe Python, structures de données et algorithmes", "icon": "PY"},
            {"name": "javascript", "display_name": "JavaScript", "description": "DOM, événements et programmation asynchrone", "icon": "JS"},
            {"name": "sql", "display_name": "SQL", "description": "Bases de données, requêtes et optimisation", "icon": "SQL"},
            {"name": "html", "display_name": "HTML", "description": "Structure et sémantique web", "icon": "HTML"},
            {"name": "css", "display_name": "CSS", "description": "Styles et mise en page web", "icon": "CSS"},
            {"name": "git", "display_name": "Git", "description": "Contrôle de version et collaboration", "icon": "GIT"},
            {"name": "linux", "display_name": "Linux", "description": "Administration système et commandes", "icon": "LX"},
            {"name": "docker", "display_name": "Docker", "description": "Conteneurisation et déploiement", "icon": "DK"}
        ]
        
        created_categories = {}
        for cat_data in categories_data:
            category = PLDCategory(
                name=cat_data["name"],
                display_name=cat_data["display_name"],
                description=cat_data["description"],
                icon=cat_data["icon"]
            )
            db.add(category)
            db.flush()  # Pour obtenir l'ID
            created_categories[cat_data["name"]] = category
            print(f"✅ Catégorie créée: {category.display_name}")
        
        # 5. Créer des thèmes pour chaque catégorie
        print("🎯 Création des thèmes...")
        themes_data = [
            # Shell
            {"category": "shell", "name": "variables", "display_name": "Variables et paramètres", "description": "Gestion des variables shell"},
            {"category": "shell", "name": "scripts", "display_name": "Scripts Bash", "description": "Écriture de scripts shell"},
            {"category": "shell", "name": "permissions", "display_name": "Permissions", "description": "Gestion des permissions de fichiers"},
            
            # C
            {"category": "c", "name": "pointers", "display_name": "Pointeurs", "description": "Gestion des pointeurs en C"},
            {"category": "c", "name": "memory", "display_name": "Gestion mémoire", "description": "Allocation et libération de mémoire"},
            {"category": "c", "name": "structures", "display_name": "Structures", "description": "Structures de données en C"},
            
            # Python
            {"category": "python", "name": "basics", "display_name": "Bases Python", "description": "Syntaxe de base Python"},
            {"category": "python", "name": "data-structures", "display_name": "Structures de données", "description": "Listes, dictionnaires, tuples"},
            {"category": "python", "name": "oop", "display_name": "POO", "description": "Programmation orientée objet"},
            
            # JavaScript
            {"category": "javascript", "name": "dom", "display_name": "DOM", "description": "Manipulation du DOM"},
            {"category": "javascript", "name": "events", "display_name": "Événements", "description": "Gestion des événements"},
            {"category": "javascript", "name": "async", "display_name": "Asynchrone", "description": "Programmation asynchrone"},
            
            # SQL
            {"category": "sql", "name": "queries", "display_name": "Requêtes", "description": "Requêtes SQL de base"},
            {"category": "sql", "name": "joins", "display_name": "Jointures", "description": "Jointures entre tables"},
            {"category": "sql", "name": "optimization", "display_name": "Optimisation", "description": "Optimisation des requêtes"},
        ]
        
        created_themes = {}
        for theme_data in themes_data:
            theme = PLDTheme(
                name=theme_data["name"],
                display_name=theme_data["display_name"],
                description=theme_data["description"],
                category_id=created_categories[theme_data["category"]].id
            )
            db.add(theme)
            db.flush()
            created_themes[f"{theme_data['category']}_{theme_data['name']}"] = theme
            print(f"✅ Thème créé: {theme.display_name} ({created_categories[theme_data['category']].display_name})")
        
        # 6. Créer des questions PLD
        print("❓ Création des questions PLD...")
        questions_data = [
            # Shell - Variables
            {
                "theme": "shell_variables",
                "question": "Comment déclarer une variable en Shell et l'afficher ?",
                "expected_answer": "Pour déclarer une variable en Shell, on utilise la syntaxe VARIABLE=valeur (sans espaces autour du =). Pour l'afficher, on utilise echo $VARIABLE ou echo ${VARIABLE}.",
                "technical_terms": ["variable", "echo", "$", "shell", "bash"],
                "explanation": "En Shell, les variables sont déclarées sans espaces et utilisées avec le préfixe $",
                "difficulty": "easy"
            },
            {
                "theme": "shell_variables", 
                "question": "Quelle est la différence entre $1, $@, et $# en Shell ?",
                "expected_answer": "$1 est le premier paramètre du script, $@ représente tous les paramètres passés au script, et $# indique le nombre de paramètres.",
                "technical_terms": ["paramètres", "$1", "$@", "$#", "arguments"],
                "explanation": "Ces variables spéciales permettent de gérer les arguments passés aux scripts Shell",
                "difficulty": "medium"
            },
            
            # C - Pointeurs
            {
                "theme": "c_pointers",
                "question": "Comment déclarer un pointeur vers un entier en C et lui assigner une adresse ?",
                "expected_answer": "On déclare un pointeur vers un entier avec int *ptr; et on lui assigne l'adresse d'une variable avec ptr = &variable; où variable est un int.",
                "technical_terms": ["pointeur", "int", "*", "&", "adresse"],
                "explanation": "Le * déclare un pointeur et & récupère l'adresse d'une variable",
                "difficulty": "medium"
            },
            
            # Python - Bases
            {
                "theme": "python_basics",
                "question": "Comment créer une liste en Python et ajouter un élément ?",
                "expected_answer": "On crée une liste avec ma_liste = [] ou ma_liste = list(). Pour ajouter un élément, on utilise ma_liste.append(element).",
                "technical_terms": ["liste", "append", "[]", "list"],
                "explanation": "Les listes Python sont des structures de données dynamiques modifiables",
                "difficulty": "easy"
            },
            
            # JavaScript - DOM
            {
                "theme": "javascript_dom",
                "question": "Comment sélectionner un élément HTML par son ID en JavaScript ?",
                "expected_answer": "On utilise document.getElementById('monId') pour sélectionner un élément par son ID.",
                "technical_terms": ["document", "getElementById", "DOM", "sélecteur"],
                "explanation": "getElementById retourne l'élément HTML avec l'ID spécifié",
                "difficulty": "easy"
            },
            
            # SQL - Requêtes
            {
                "theme": "sql_queries",
                "question": "Comment récupérer tous les utilisateurs dont l'âge est supérieur à 25 ans ?",
                "expected_answer": "SELECT * FROM users WHERE age > 25;",
                "technical_terms": ["SELECT", "FROM", "WHERE", "condition"],
                "explanation": "La clause WHERE permet de filtrer les résultats selon une condition",
                "difficulty": "easy"
            }
        ]
        
        for q_data in questions_data:
            question = PLDQuestion(
                question_text=q_data["question"],
                expected_answer=q_data["expected_answer"],
                technical_terms=json.dumps(q_data["technical_terms"]),
                explanation=q_data["explanation"],
                difficulty=q_data["difficulty"],
                theme_id=created_themes[q_data["theme"]].id
            )
            db.add(question)
            print(f"✅ Question créée: {q_data['question'][:50]}...")
        
        # 7. Créer quelques questions de quiz classique
        print("📝 Création des questions de quiz classique...")
        classic_questions = [
            {
                "question_text": "Quel est le langage de programmation orienté objet développé par Sun Microsystems ?",
                "option_a": "Python",
                "option_b": "Java", 
                "option_c": "C++",
                "option_d": "JavaScript",
                "correct_answer": "b",
                "explanation": "Java a été développé par Sun Microsystems (maintenant Oracle)",
                "category": "programming",
                "difficulty": "easy"
            },
            {
                "question_text": "Que signifie HTTP ?",
                "option_a": "HyperText Transfer Protocol",
                "option_b": "HyperText Transport Protocol", 
                "option_c": "HyperText Transmission Protocol",
                "option_d": "HyperText Terminal Protocol",
                "correct_answer": "a",
                "explanation": "HTTP signifie HyperText Transfer Protocol",
                "category": "web",
                "difficulty": "easy"
            },
            {
                "question_text": "Quelle commande Git permet de voir l'historique des commits ?",
                "option_a": "git status",
                "option_b": "git log", 
                "option_c": "git history",
                "option_d": "git show",
                "correct_answer": "b",
                "explanation": "git log affiche l'historique des commits",
                "category": "git",
                "difficulty": "easy"
            }
        ]
        
        for q_data in classic_questions:
            question = Question(
                question_text=q_data["question_text"],
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_answer=q_data["correct_answer"],
                explanation=q_data["explanation"],
                category=q_data["category"],
                difficulty=q_data["difficulty"]
            )
            db.add(question)
            print(f"✅ Question classique créée: {q_data['question_text'][:50]}...")
        
        # 8. Commit final
        db.commit()
        print("\n🎉 Base de données reconstruite avec succès !")
        
        # 9. Statistiques finales
        print("\n📊 Statistiques finales:")
        print(f"   👥 Utilisateurs: {db.query(User).count()}")
        print(f"   📚 Catégories PLD: {db.query(PLDCategory).count()}")
        print(f"   🎯 Thèmes PLD: {db.query(PLDTheme).count()}")
        print(f"   ❓ Questions PLD: {db.query(PLDQuestion).count()}")
        print(f"   📝 Questions classiques: {db.query(Question).count()}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    rebuild_database()

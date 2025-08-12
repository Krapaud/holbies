#!/usr/bin/env python3
"""
Script de migration pour transférer les questions PLD du code vers la base de données
"""

import sys
import os
import json

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app.database import SessionLocal, engine
from app.models import Base, PLDCategory, PLDTheme, PLDQuestion

# Données existantes du code
AI_QUESTIONS_DB = {
    "shell": {
        "permission": {
            1: {
                "question_id": 1,
                "question_text": "Expliquez la différence entre chmod 755 et chmod 644 sur un fichier.",
                "expected_answer": "chmod 755 donne les permissions rwx pour le propriétaire et rx pour le groupe et les autres, tandis que chmod 644 donne rw pour le propriétaire et r pour le groupe et les autres. 755 est typique pour les exécutables, 644 pour les fichiers de données.",
                "technical_terms": ["chmod", "permissions", "rwx", "propriétaire", "groupe", "autres", "octal", "755", "644"],
                "explanation": "Les permissions Unix utilisent 3 bits par catégorie : r(4) + w(2) + x(1). 755 = rwxr-xr-x, 644 = rw-r--r--",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            2: {
                "question_id": 2,
                "question_text": "Comment changer le propriétaire d'un fichier et pourquoi utiliser sudo ?",
                "expected_answer": "On utilise chown pour changer le propriétaire : chown utilisateur:groupe fichier. Sudo est nécessaire car seul le root ou le propriétaire actuel peut changer la propriété d'un fichier.",
                "technical_terms": ["chown", "propriétaire", "groupe", "sudo", "root", "permissions", "utilisateur"],
                "explanation": "chown modifie les métadonnées du système de fichiers. Sudo élève temporairement les privilèges pour les opérations administratives.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            3: {
                "question_id": 3,
                "question_text": "Que fait umask et comment calculer les permissions résultantes ?",
                "expected_answer": "umask définit les permissions par défaut en soustrayant ses valeurs des permissions maximales. Pour les fichiers (666), umask 022 donne 644. Pour les dossiers (777), umask 022 donne 755.",
                "technical_terms": ["umask", "permissions par défaut", "masque", "666", "777", "022", "soustraction"],
                "explanation": "umask agit comme un masque inversé : il retire des permissions. Plus umask est élevé, moins il y a de permissions accordées par défaut.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            4: {
                "question_id": 4,
                "question_text": "Expliquez les permissions spéciales : sticky bit, SUID et SGID.",
                "expected_answer": "SUID (4000) permet d'exécuter avec les droits du propriétaire, SGID (2000) avec ceux du groupe, sticky bit (1000) empêche la suppression par d'autres utilisateurs dans un répertoire partagé.",
                "technical_terms": ["sticky bit", "SUID", "SGID", "permissions spéciales", "4000", "2000", "1000", "exécution"],
                "explanation": "Ces permissions spéciales modifient le comportement d'exécution et d'accès au-delà des permissions standards rwx.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            5: {
                "question_id": 5,
                "question_text": "Comment voir les permissions détaillées d'un fichier ?",
                "expected_answer": "ls -l affiche les permissions sous forme de chaîne (rwxrwxrwx), ls -la inclut les fichiers cachés, stat donne des informations détaillées incluant les permissions en octal.",
                "technical_terms": ["ls -l", "ls -la", "stat", "permissions", "octal", "fichiers cachés", "métadonnées"],
                "explanation": "Plusieurs commandes permettent de voir les permissions avec différents niveaux de détail selon les besoins.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            6: {
                "question_id": 6,
                "question_text": "Quelle est la différence entre su et sudo ?",
                "expected_answer": "su change d'utilisateur complètement et nécessite le mot de passe de l'utilisateur cible, sudo exécute une commande avec des privilèges élevés en utilisant votre propre mot de passe et selon la configuration sudoers.",
                "technical_terms": ["su", "sudo", "utilisateur", "mot de passe", "privilèges", "sudoers", "switch user"],
                "explanation": "su est un changement complet d'identité, sudo est une élévation temporaire et contrôlée de privilèges.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            },
            7: {
                "question_id": 7,
                "question_text": "Comment donner temporairement les permissions d'exécution à un script ?",
                "expected_answer": "chmod +x script.sh ajoute les permissions d'exécution pour tous, ou chmod u+x pour le propriétaire seulement. On peut aussi utiliser sh script.sh sans changer les permissions.",
                "technical_terms": ["chmod +x", "chmod u+x", "permissions d'exécution", "script", "sh", "propriétaire"],
                "explanation": "Les permissions d'exécution sont nécessaires pour lancer un script directement. Alternativement, passer par l'interpréteur contourne cette exigence.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "permission",
                "max_score": 100
            }
        },
        "io": {
            8: {
                "question_id": 8,
                "question_text": "Expliquez la différence entre >, >> et < dans le shell.",
                "expected_answer": "> redirige la sortie en écrasant le fichier, >> ajoute à la fin du fichier, < redirige l'entrée depuis un fichier. > et >> concernent la sortie (stdout), < concerne l'entrée (stdin).",
                "technical_terms": ["redirection", "stdout", "stdin", ">", ">>", "<", "écrasement", "ajout", "entrée", "sortie"],
                "explanation": "Les redirections permettent de manipuler les flux d'entrée et sortie standard des commandes Unix.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            9: {
                "question_id": 9,
                "question_text": "Comment fonctionne le pipe | et donnez un exemple d'utilisation ?",
                "expected_answer": "Le pipe | connecte la sortie d'une commande à l'entrée de la suivante. Exemple : ls -l | grep '.txt' filtre les fichiers .txt dans la liste. C'est un mécanisme de communication inter-processus.",
                "technical_terms": ["pipe", "|", "sortie", "entrée", "grep", "ls", "filtre", "inter-processus", "chaînage"],
                "explanation": "Les pipes permettent de chaîner des commandes pour créer des workflows complexes de traitement de données.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            10: {
                "question_id": 10,
                "question_text": "Quelle est la différence entre 2> et 2>&1 ?",
                "expected_answer": "2> redirige stderr (erreurs) vers un fichier, 2>&1 redirige stderr vers stdout. Cela permet de capturer les erreurs avec la sortie normale ou de les traiter séparément.",
                "technical_terms": ["stderr", "stdout", "2>", "2>&1", "redirection", "erreurs", "descripteur de fichier"],
                "explanation": "La gestion séparée des flux d'erreur et de sortie normale permet un meilleur contrôle du traitement des résultats.",
                "difficulty": "hard",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            11: {
                "question_id": 11,
                "question_text": "Comment rechercher un mot dans des fichiers avec grep ?",
                "expected_answer": "grep 'mot' fichier recherche dans un fichier, grep -r 'mot' dossier/ recherche récursivement, grep -i pour ignorer la casse, grep -n pour afficher les numéros de lignes.",
                "technical_terms": ["grep", "recherche", "récursif", "-r", "-i", "-n", "casse", "numéros de lignes", "pattern"],
                "explanation": "grep est un outil puissant de recherche textuelle avec de nombreuses options pour affiner les résultats.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            12: {
                "question_id": 12,
                "question_text": "Comment utiliser find pour localiser des fichiers ?",
                "expected_answer": "find /chemin -name 'pattern' trouve par nom, find . -type f pour les fichiers seulement, find . -size +1M pour les fichiers > 1MB, find . -mtime -7 pour les fichiers modifiés dans les 7 derniers jours.",
                "technical_terms": ["find", "-name", "-type", "-size", "-mtime", "pattern", "fichiers", "répertoires", "critères"],
                "explanation": "find permet des recherches complexes basées sur divers critères : nom, type, taille, date de modification, permissions...",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            13: {
                "question_id": 13,
                "question_text": "Expliquez l'utilisation de head, tail et less.",
                "expected_answer": "head affiche les premières lignes d'un fichier (défaut 10), tail les dernières lignes, less permet de naviguer dans un fichier page par page. tail -f suit un fichier en temps réel.",
                "technical_terms": ["head", "tail", "less", "premières lignes", "dernières lignes", "navigation", "tail -f", "temps réel"],
                "explanation": "Ces outils permettent d'examiner des fichiers de différentes manières selon les besoins : aperçu, fin de logs, lecture complète.",
                "difficulty": "easy",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            },
            14: {
                "question_id": 14,
                "question_text": "Comment combiner plusieurs commandes avec && et || ?",
                "expected_answer": "&& exécute la commande suivante seulement si la précédente réussit (code de retour 0), || exécute si la précédente échoue. Exemple : make && make install || echo 'Échec'",
                "technical_terms": ["&&", "||", "code de retour", "succès", "échec", "enchaînement conditionnel", "make"],
                "explanation": "Ces opérateurs permettent un contrôle de flux conditionnel basé sur le succès ou l'échec des commandes précédentes.",
                "difficulty": "medium",
                "category": "shell",
                "theme": "io",
                "max_score": 100
            }
        }
    }
}

def create_tables():
    """Créer les tables dans la base de données"""
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées")

def migrate_data():
    """Migrer les données du code vers la base de données"""
    db = SessionLocal()
    
    try:
        print("Début de la migration...")
        
        # Nettoyer les données existantes
        print("Suppression des données existantes...")
        db.query(PLDQuestion).delete()
        db.query(PLDTheme).delete() 
        db.query(PLDCategory).delete()
        db.commit()
        
        # Migrer les données
        categories_created = {}
        themes_created = {}
        
        for category_name, themes_data in AI_QUESTIONS_DB.items():
            # Créer la catégorie
            if category_name not in categories_created:
                category = PLDCategory(
                    name=category_name,
                    display_name=category_name.title(),
                    description=f"Questions de programmation {category_name}",
                    icon="🐚" if category_name == "shell" else "📚"
                )
                db.add(category)
                db.flush()  # Pour obtenir l'ID
                categories_created[category_name] = category
                print(f"✅ Catégorie créée: {category_name}")
            
            # Créer les thèmes
            for theme_name, questions_data in themes_data.items():
                theme_key = f"{category_name}_{theme_name}"
                if theme_key not in themes_created:
                    # Choisir une icône appropriée
                    icon = "📝"
                    if theme_name == "permission":
                        icon = "🔐"
                    elif theme_name == "io":
                        icon = "💾"
                    
                    theme = PLDTheme(
                        name=theme_name,
                        display_name=theme_name.title().replace("_", " "),
                        description=f"Questions sur {theme_name} en {category_name}",
                        icon=icon,
                        category_id=categories_created[category_name].id
                    )
                    db.add(theme)
                    db.flush()  # Pour obtenir l'ID
                    themes_created[theme_key] = theme
                    print(f"✅ Thème créé: {category_name}/{theme_name}")
                
                # Créer les questions
                for question_data in questions_data.values():
                    question = PLDQuestion(
                        question_text=question_data["question_text"],
                        expected_answer=question_data["expected_answer"],
                        technical_terms=json.dumps(question_data["technical_terms"]),
                        explanation=question_data["explanation"],
                        difficulty=question_data["difficulty"],
                        max_score=question_data["max_score"],
                        theme_id=themes_created[theme_key].id
                    )
                    db.add(question)
                
                print(f"✅ Questions créées pour {category_name}/{theme_name}: {len(questions_data)}")
        
        # Sauvegarder toutes les modifications
        db.commit()
        print("✅ Migration terminée avec succès!")
        
        # Afficher un résumé
        total_categories = db.query(PLDCategory).count()
        total_themes = db.query(PLDTheme).count()
        total_questions = db.query(PLDQuestion).count()
        
        print(f"""
📊 RÉSUMÉ DE LA MIGRATION:
- Catégories: {total_categories}
- Thèmes: {total_themes}  
- Questions: {total_questions}
        """)
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Script de migration PLD - Code vers Base de données")
    print("=" * 60)
    
    create_tables()
    migrate_data()
    
    print("✅ Migration terminée!")

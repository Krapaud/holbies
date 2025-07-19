#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des questions de quiz
style PLD Holberton School
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Question

# Créer les tables
Base.metadata.create_all(bind=engine)

# Questions de quiz style PLD Holberton School
QUIZ_QUESTIONS = [
    {
        "question_text": "Quelle est la complexité temporelle de la recherche dans une liste chaînée ?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n²)",
        "correct_answer": "c",
        "explanation": "Dans une liste chaînée, pour trouver un élément, il faut parcourir la liste depuis le début, ce qui donne une complexité O(n).",
        "difficulty": "medium",
        "category": "algorithms"
    },
    {
        "question_text": "En Python, que retourne la fonction len() appliquée à une liste vide ?",
        "option_a": "None",
        "option_b": "0",
        "option_c": "False",
        "option_d": "Une erreur",
        "correct_answer": "b",
        "explanation": "len([]) retourne 0, car une liste vide contient 0 éléments.",
        "difficulty": "easy",
        "category": "python"
    },
    {
        "question_text": "Quelle structure de données utilise le principe LIFO (Last In, First Out) ?",
        "option_a": "Queue",
        "option_b": "Stack",
        "option_c": "Array",
        "option_d": "Hash Table",
        "correct_answer": "b",
        "explanation": "Une pile (stack) utilise le principe LIFO : le dernier élément ajouté est le premier à être retiré.",
        "difficulty": "easy",
        "category": "data-structures"
    },
    {
        "question_text": "En C, quelle fonction est utilisée pour allouer dynamiquement de la mémoire ?",
        "option_a": "calloc()",
        "option_b": "malloc()",
        "option_c": "alloc()",
        "option_d": "new()",
        "correct_answer": "b",
        "explanation": "malloc() est la fonction standard en C pour allouer dynamiquement de la mémoire.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence principale entre HTTP et HTTPS ?",
        "option_a": "HTTPS est plus rapide",
        "option_b": "HTTPS utilise le chiffrement SSL/TLS",
        "option_c": "HTTP est plus sécurisé",
        "option_d": "Il n'y a pas de différence",
        "correct_answer": "b",
        "explanation": "HTTPS (HTTP Secure) utilise le chiffrement SSL/TLS pour sécuriser les communications.",
        "difficulty": "medium",
        "category": "web"
    },
    {
        "question_text": "En programmation orientée objet, qu'est-ce que l'encapsulation ?",
        "option_a": "L'héritage entre classes",
        "option_b": "Le polymorphisme",
        "option_c": "La dissimulation des détails d'implémentation",
        "option_d": "La création d'objets",
        "correct_answer": "c",
        "explanation": "L'encapsulation consiste à cacher les détails d'implémentation et à exposer uniquement une interface publique.",
        "difficulty": "medium",
        "category": "oop"
    },
    {
        "question_text": "Quel algorithme de tri a une complexité temporelle moyenne de O(n log n) ?",
        "option_a": "Bubble Sort",
        "option_b": "Selection Sort",
        "option_c": "Quick Sort",
        "option_d": "Insertion Sort",
        "correct_answer": "c",
        "explanation": "Quick Sort a une complexité moyenne de O(n log n), bien que dans le pire cas ce soit O(n²).",
        "difficulty": "medium",
        "category": "algorithms"
    },
    {
        "question_text": "En SQL, quelle commande permet de modifier des données existantes ?",
        "option_a": "INSERT",
        "option_b": "UPDATE",
        "option_c": "SELECT",
        "option_d": "DELETE",
        "correct_answer": "b",
        "explanation": "UPDATE permet de modifier des données existantes dans une base de données SQL.",
        "difficulty": "easy",
        "category": "sql"
    },
    {
        "question_text": "Quelle est la valeur de 2^10 en décimal ?",
        "option_a": "512",
        "option_b": "1024",
        "option_c": "2048",
        "option_d": "256",
        "correct_answer": "b",
        "explanation": "2^10 = 1024, c'est une valeur importante en informatique (1 kilo-octet).",
        "difficulty": "easy",
        "category": "mathematics"
    },
    {
        "question_text": "En Git, quelle commande permet de voir l'historique des commits ?",
        "option_a": "git status",
        "option_b": "git log",
        "option_c": "git diff",
        "option_d": "git show",
        "correct_answer": "b",
        "explanation": "git log affiche l'historique des commits dans le repository.",
        "difficulty": "easy",
        "category": "git"
    },
    {
        "question_text": "Quelle est la complexité spatiale d'un algorithme de tri par fusion (merge sort) ?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n log n)",
        "correct_answer": "c",
        "explanation": "Merge sort nécessite O(n) espace supplémentaire pour stocker les sous-tableaux temporaires.",
        "difficulty": "hard",
        "category": "algorithms"
    },
    {
        "question_text": "En JavaScript, que fait l'opérateur === ?",
        "option_a": "Comparaison avec conversion de type",
        "option_b": "Comparaison stricte sans conversion",
        "option_c": "Assignation",
        "option_d": "Comparaison approximative",
        "correct_answer": "b",
        "explanation": "L'opérateur === fait une comparaison stricte sans conversion de type automatique.",
        "difficulty": "medium",
        "category": "javascript"
    },
    {
        "question_text": "Qu'est-ce qu'une API REST ?",
        "option_a": "Un protocole de sécurité",
        "option_b": "Un style d'architecture pour services web",
        "option_c": "Un langage de programmation",
        "option_d": "Un système de base de données",
        "correct_answer": "b",
        "explanation": "REST est un style d'architecture pour concevoir des services web utilisant HTTP.",
        "difficulty": "medium",
        "category": "web"
    },
    {
        "question_text": "En Python, quelle est la différence entre une liste et un tuple ?",
        "option_a": "Aucune différence",
        "option_b": "Les tuples sont mutables, les listes non",
        "option_c": "Les listes sont mutables, les tuples non",
        "option_d": "Les tuples sont plus lents",
        "correct_answer": "c",
        "explanation": "Les listes sont mutables (modifiables) tandis que les tuples sont immutables.",
        "difficulty": "easy",
        "category": "python"
    },
    {
        "question_text": "Quelle est la sortie de printf('%d', 5/2) en C ?",
        "option_a": "2.5",
        "option_b": "2",
        "option_c": "3",
        "option_d": "Erreur",
        "correct_answer": "b",
        "explanation": "En C, la division de deux entiers donne un entier (division entière), donc 5/2 = 2.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Qu'est-ce que le Big O notation mesure ?",
        "option_a": "La précision d'un algorithme",
        "option_b": "La complexité temporelle ou spatiale",
        "option_c": "La facilité de lecture du code",
        "option_d": "Le nombre de lignes de code",
        "correct_answer": "b",
        "explanation": "La notation Big O mesure la complexité algorithmique (temporelle ou spatiale) dans le pire cas.",
        "difficulty": "medium",
        "category": "algorithms"
    },
    {
        "question_text": "En HTML, quelle balise est utilisée pour créer un lien hypertexte ?",
        "option_a": "<link>",
        "option_b": "<href>",
        "option_c": "<a>",
        "option_d": "<url>",
        "correct_answer": "c",
        "explanation": "La balise <a> avec l'attribut href est utilisée pour créer des liens hypertexte.",
        "difficulty": "easy",
        "category": "html"
    },
    {
        "question_text": "Quelle structure de données est optimale pour implémenter une file d'attente ?",
        "option_a": "Array",
        "option_b": "Stack",
        "option_c": "Queue",
        "option_d": "Tree",
        "correct_answer": "c",
        "explanation": "Une queue (file) est la structure de données naturelle pour implémenter une file d'attente (FIFO).",
        "difficulty": "easy",
        "category": "data-structures"
    },
    {
        "question_text": "En Linux, quelle commande affiche le contenu d'un fichier ?",
        "option_a": "ls",
        "option_b": "cat",
        "option_c": "pwd",
        "option_d": "cd",
        "correct_answer": "b",
        "explanation": "La commande cat permet d'afficher le contenu d'un ou plusieurs fichiers.",
        "difficulty": "easy",
        "category": "linux"
    },
    {
        "question_text": "Qu'est-ce qu'un pointeur en programmation ?",
        "option_a": "Une variable qui stocke une valeur",
        "option_b": "Une variable qui stocke une adresse mémoire",
        "option_c": "Une fonction",
        "option_d": "Un type de données",
        "correct_answer": "b",
        "explanation": "Un pointeur est une variable qui stocke l'adresse mémoire d'une autre variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En CSS, quelle propriété contrôle l'espacement entre les éléments ?",
        "option_a": "padding",
        "option_b": "margin",
        "option_c": "border",
        "option_d": "spacing",
        "correct_answer": "b",
        "explanation": "La propriété margin contrôle l'espacement externe entre les éléments.",
        "difficulty": "easy",
        "category": "css"
    },
    {
        "question_text": "Quelle est la complexité temporelle de l'accès à un élément dans un tableau par index ?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n²)",
        "correct_answer": "a",
        "explanation": "L'accès par index dans un tableau est en temps constant O(1).",
        "difficulty": "easy",
        "category": "algorithms"
    },
    {
        "question_text": "En Python, que fait la méthode split() sur une chaîne ?",
        "option_a": "Divise la chaîne en liste",
        "option_b": "Supprime des espaces",
        "option_c": "Convertit en majuscules",
        "option_d": "Inverse la chaîne",
        "correct_answer": "a",
        "explanation": "split() divise une chaîne en liste selon un délimiteur (espace par défaut).",
        "difficulty": "easy",
        "category": "python"
    },
    {
        "question_text": "Qu'est-ce que le polymorphisme en POO ?",
        "option_a": "L'héritage multiple",
        "option_b": "La capacité d'un objet à prendre plusieurs formes",
        "option_c": "L'encapsulation des données",
        "option_d": "La création d'instances",
        "correct_answer": "b",
        "explanation": "Le polymorphisme permet à un objet de prendre plusieurs formes selon le contexte.",
        "difficulty": "medium",
        "category": "oop"
    },
    {
        "question_text": "En SQL, quelle clause permet de filtrer les résultats ?",
        "option_a": "SELECT",
        "option_b": "FROM",
        "option_c": "WHERE",
        "option_d": "ORDER BY",
        "correct_answer": "c",
        "explanation": "La clause WHERE permet de filtrer les lignes selon des conditions.",
        "difficulty": "easy",
        "category": "sql"
    },
    {
        "question_text": "Quelle est la différence entre '==' et 'is' en Python ?",
        "option_a": "Aucune différence",
        "option_b": "== compare les valeurs, is compare l'identité",
        "option_c": "is compare les valeurs, == compare l'identité",
        "option_d": "is est plus rapide",
        "correct_answer": "b",
        "explanation": "== compare les valeurs tandis que 'is' compare l'identité des objets (même objet en mémoire).",
        "difficulty": "medium",
        "category": "python"
    },
    {
        "question_text": "Qu'est-ce qu'une fonction récursive ?",
        "option_a": "Une fonction qui ne retourne rien",
        "option_b": "Une fonction qui s'appelle elle-même",
        "option_c": "Une fonction avec plusieurs paramètres",
        "option_d": "Une fonction privée",
        "correct_answer": "b",
        "explanation": "Une fonction récursive est une fonction qui s'appelle elle-même pour résoudre un problème.",
        "difficulty": "medium",
        "category": "algorithms"
    },
    {
        "question_text": "En Git, que fait la commande 'git clone' ?",
        "option_a": "Crée une branche",
        "option_b": "Copie un repository distant localement",
        "option_c": "Sauvegarde les changements",
        "option_d": "Fusionne deux branches",
        "correct_answer": "b",
        "explanation": "git clone crée une copie locale d'un repository distant.",
        "difficulty": "easy",
        "category": "git"
    },
    {
        "question_text": "Quelle est la complexité temporelle de l'insertion au début d'une liste chaînée ?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n²)",
        "correct_answer": "a",
        "explanation": "L'insertion au début d'une liste chaînée se fait en temps constant O(1).",
        "difficulty": "medium",
        "category": "data-structures"
    },
    {
        "question_text": "En JavaScript, que fait JSON.parse() ?",
        "option_a": "Convertit objet en chaîne JSON",
        "option_b": "Convertit chaîne JSON en objet",
        "option_c": "Valide du JSON",
        "option_d": "Formate du JSON",
        "correct_answer": "b",
        "explanation": "JSON.parse() convertit une chaîne JSON en objet JavaScript.",
        "difficulty": "easy",
        "category": "javascript"
    },
    {
        "question_text": "Qu'est-ce qu'un hash table (table de hachage) ?",
        "option_a": "Un tableau ordonné",
        "option_b": "Une structure utilisant une fonction de hachage",
        "option_c": "Une liste chaînée",
        "option_d": "Un arbre binaire",
        "correct_answer": "b",
        "explanation": "Une table de hachage utilise une fonction de hachage pour mapper les clés aux valeurs.",
        "difficulty": "medium",
        "category": "data-structures"
    },
    {
        "question_text": "En C, que fait l'opérateur sizeof ?",
        "option_a": "Compte les éléments d'un tableau",
        "option_b": "Retourne la taille en octets",
        "option_c": "Alloue de la mémoire",
        "option_d": "Libère de la mémoire",
        "correct_answer": "b",
        "explanation": "sizeof retourne la taille en octets d'un type ou d'une variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle méthode HTTP est idempotente ?",
        "option_a": "POST",
        "option_b": "GET",
        "option_c": "PATCH",
        "option_d": "Toutes les méthodes",
        "correct_answer": "b",
        "explanation": "GET est idempotent : plusieurs appels identiques produisent le même résultat.",
        "difficulty": "medium",
        "category": "web"
    },
    {
        "question_text": "En Python, que fait l'instruction 'pass' ?",
        "option_a": "Passe à l'itération suivante",
        "option_b": "Ne fait rien (placeholder)",
        "option_c": "Termine la fonction",
        "option_d": "Lève une exception",
        "correct_answer": "b",
        "explanation": "'pass' est une instruction vide qui ne fait rien, utilisée comme placeholder.",
        "difficulty": "easy",
        "category": "python"
    },
    {
        "question_text": "Qu'est-ce que la normalisation en base de données ?",
        "option_a": "Convertir en majuscules",
        "option_b": "Organiser pour réduire la redondance",
        "option_c": "Trier les données",
        "option_d": "Chiffrer les données",
        "correct_answer": "b",
        "explanation": "La normalisation organise les données pour éliminer la redondance et les anomalies.",
        "difficulty": "medium",
        "category": "database"
    },
    {
        "question_text": "En Linux, que fait la commande 'chmod 755' ?",
        "option_a": "Change le propriétaire",
        "option_b": "Définit les permissions rwxr-xr-x",
        "option_c": "Copie un fichier",
        "option_d": "Supprime un fichier",
        "correct_answer": "b",
        "explanation": "chmod 755 donne les permissions lecture/écriture/exécution au propriétaire, lecture/exécution aux autres.",
        "difficulty": "medium",
        "category": "linux"
    },
    {
        "question_text": "Qu'est-ce qu'un algorithme glouton (greedy) ?",
        "option_a": "Un algorithme qui utilise beaucoup de mémoire",
        "option_b": "Un algorithme qui fait le choix localement optimal",
        "option_c": "Un algorithme très lent",
        "option_d": "Un algorithme récursif",
        "correct_answer": "b",
        "explanation": "Un algorithme glouton fait toujours le choix qui semble optimal localement.",
        "difficulty": "hard",
        "category": "algorithms"
    },
    {
        "question_text": "En CSS, que fait la propriété 'position: absolute' ?",
        "option_a": "Position relative au parent",
        "option_b": "Position relative à la viewport",
        "option_c": "Position relative au document",
        "option_d": "Position fixe",
        "correct_answer": "a",
        "explanation": "position: absolute positionne l'élément relativement à son parent positionné le plus proche.",
        "difficulty": "medium",
        "category": "css"
    },
    {
        "question_text": "Qu'est-ce qu'une clé étrangère en base de données ?",
        "option_a": "Une clé de chiffrement",
        "option_b": "Une clé référençant une autre table",
        "option_c": "Une clé unique",
        "option_d": "Une clé temporaire",
        "correct_answer": "b",
        "explanation": "Une clé étrangère est un champ qui référence la clé primaire d'une autre table.",
        "difficulty": "easy",
        "category": "database"
    },
    {
        "question_text": "En JavaScript, que fait Array.map() ?",
        "option_a": "Filtre les éléments",
        "option_b": "Transforme chaque élément",
        "option_c": "Réduit le tableau",
        "option_d": "Trie le tableau",
        "correct_answer": "b",
        "explanation": "Array.map() crée un nouveau tableau en transformant chaque élément avec une fonction.",
        "difficulty": "medium",
        "category": "javascript"
    },
    {
        "question_text": "Qu'est-ce que l'injection SQL ?",
        "option_a": "Une technique d'optimisation",
        "option_b": "Une vulnérabilité de sécurité",
        "option_c": "Une méthode de sauvegarde",
        "option_d": "Un type de jointure",
        "correct_answer": "b",
        "explanation": "L'injection SQL est une vulnérabilité permettant d'exécuter du code SQL malveillant.",
        "difficulty": "medium",
        "category": "security"
    },
    # Ajouter plus de questions pour atteindre 100
    {
        "question_text": "En Python, que fait la fonction enumerate() ?",
        "option_a": "Compte les éléments",
        "option_b": "Retourne index et valeur",
        "option_c": "Trie une liste",
        "option_d": "Filtre une liste",
        "correct_answer": "b",
        "explanation": "enumerate() retourne un objet avec les indices et valeurs d'un itérable.",
        "difficulty": "medium",
        "category": "python"
    },
    {
        "question_text": "Qu'est-ce que DNS ?",
        "option_a": "Un protocole de sécurité",
        "option_b": "Un système de noms de domaine",
        "option_c": "Un serveur web",
        "option_d": "Un langage de programmation",
        "correct_answer": "b",
        "explanation": "DNS (Domain Name System) traduit les noms de domaine en adresses IP.",
        "difficulty": "easy",
        "category": "networking"
    },
    {
        "question_text": "En Git, que fait 'git merge' ?",
        "option_a": "Crée une nouvelle branche",
        "option_b": "Fusionne deux branches",
        "option_c": "Supprime une branche",
        "option_d": "Renomme une branche",
        "correct_answer": "b",
        "explanation": "git merge fusionne les changements d'une branche dans la branche courante.",
        "difficulty": "easy",
        "category": "git"
    },
    {
        "question_text": "Quelle est la différence entre TCP et UDP ?",
        "option_a": "TCP est plus rapide",
        "option_b": "UDP garantit la livraison",
        "option_c": "TCP est fiable, UDP est rapide",
        "option_d": "Aucune différence",
        "correct_answer": "c",
        "explanation": "TCP garantit la livraison et l'ordre, UDP est plus rapide mais non fiable.",
        "difficulty": "medium",
        "category": "networking"
    },
    {
        "question_text": "En C, que fait la fonction malloc() si elle échoue ?",
        "option_a": "Retourne 0",
        "option_b": "Retourne NULL",
        "option_c": "Lève une exception",
        "option_d": "Arrête le programme",
        "correct_answer": "b",
        "explanation": "malloc() retourne NULL si l'allocation mémoire échoue.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Qu'est-ce que REST en architecture web ?",
        "option_a": "Un protocole de sécurité",
        "option_b": "Un style architectural",
        "option_c": "Un serveur web",
        "option_d": "Un langage de requête",
        "correct_answer": "b",
        "explanation": "REST (Representational State Transfer) est un style architectural pour les services web.",
        "difficulty": "medium",
        "category": "web"
    },
    {
        "question_text": "En Python, que fait 'self' dans une méthode de classe ?",
        "option_a": "Référence la classe",
        "option_b": "Référence l'instance",
        "option_c": "Référence la méthode",
        "option_d": "Ne fait rien",
        "correct_answer": "b",
        "explanation": "'self' référence l'instance courante de la classe.",
        "difficulty": "easy",
        "category": "python"
    },
    {
        "question_text": "Qu'est-ce qu'un arbre binaire de recherche ?",
        "option_a": "Un arbre avec deux branches",
        "option_b": "Un arbre ordonné pour la recherche",
        "option_c": "Un arbre équilibré",
        "option_d": "Un arbre complet",
        "correct_answer": "b",
        "explanation": "Un ABR maintient l'ordre : enfant gauche < parent < enfant droit.",
        "difficulty": "medium",
        "category": "data-structures"
    },
    {
        "question_text": "En HTML, quelle balise définit un paragraphe ?",
        "option_a": "<par>",
        "option_b": "<p>",
        "option_c": "<paragraph>",
        "option_d": "<text>",
        "correct_answer": "b",
        "explanation": "La balise <p> définit un paragraphe en HTML.",
        "difficulty": "easy",
        "category": "html"
    },
    {
        "question_text": "Qu'est-ce que l'héritage en POO ?",
        "option_a": "Partage de propriétés entre classes",
        "option_b": "Création d'objets",
        "option_c": "Encapsulation des données",
        "option_d": "Polymorphisme",
        "correct_answer": "a",
        "explanation": "L'héritage permet à une classe de hériter des propriétés d'une classe parent.",
        "difficulty": "easy",
        "category": "oop"
    }
]

def populate_questions():
    """Peuple la base de données avec les questions de quiz"""
    db = SessionLocal()
    try:
        # Vérifier si des questions existent déjà
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"La base de données contient déjà {existing_count} questions.")
            response = input("Voulez-vous les supprimer et recommencer ? (y/N): ")
            if response.lower() == 'y':
                db.query(Question).delete()
                db.commit()
                print("Questions existantes supprimées.")
            else:
                print("Arrêt du script.")
                return

        # Ajouter les nouvelles questions
        for q_data in QUIZ_QUESTIONS:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"✅ {len(QUIZ_QUESTIONS)} questions ajoutées avec succès!")
        
        # Afficher un résumé par catégorie
        categories = {}
        for q in QUIZ_QUESTIONS:
            cat = q['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nRépartition par catégorie:")
        for category, count in categories.items():
            print(f"  - {category}: {count} questions")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des questions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Peuplement de la base de données avec les questions de quiz...")
    populate_questions()
    print("✨ Terminé!")

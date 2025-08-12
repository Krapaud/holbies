#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des questions de quiz
style PLD Holberton School - Organisé par difficulté avec réponses équilibrées
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Force PostgreSQL URL
os.environ['DATABASE_URL'] = 'postgresql://postgres@localhost/holbies_db'

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Question

print(f"Using database: {engine.url}")

# Créer les tables
Base.metadata.create_all(bind=engine)
print("Tables créées!")

# Questions de quiz sur le langage C - style PLD Holberton School
# Organisées par difficulté : easy -> medium -> hard
# Réponses équilibrées entre A, B, C, D
QUIZ_QUESTIONS = [
    # ===== QUESTIONS FACILES =====
    {
        "question_text": "Quelle est la fonction d'entrée principale d'un programme C ?",
        "option_a": "start()",
        "option_b": "main()",
        "option_c": "begin()",
        "option_d": "entry()",
        "correct_answer": "b",
        "explanation": "La fonction main() est le point d'entrée obligatoire de tout programme C.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quel caractère termine une chaîne de caractères ?",
        "option_a": "'\\0'",
        "option_b": "'\\n'",
        "option_c": "'\\t'",
        "option_d": "EOF",
        "correct_answer": "a",
        "explanation": "Le caractère null '\\0' marque la fin d'une chaîne de caractères en C.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction printf() en C ?",
        "option_a": "Lit une entrée utilisateur",
        "option_b": "Alloue de la mémoire",
        "option_c": "Affiche du texte formaté",
        "option_d": "Compile le programme",
        "correct_answer": "c",
        "explanation": "printf() affiche du texte formaté sur la sortie standard.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quelle fonction libère la mémoire allouée par malloc() ?",
        "option_a": "delete()",
        "option_b": "release()",
        "option_c": "dealloc()",
        "option_d": "free()",
        "correct_answer": "d",
        "explanation": "free() libère la mémoire précédemment allouée par malloc(), calloc() ou realloc().",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la valeur de NULL en C ?",
        "option_a": "0",
        "option_b": "-1",
        "option_c": "1",
        "option_d": "undefined",
        "correct_answer": "a",
        "explanation": "NULL est défini comme 0 en C, représentant un pointeur qui ne pointe vers rien.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction permet de comparer deux chaînes en C ?",
        "option_a": "compare()",
        "option_b": "strcmp()",
        "option_c": "strcompare()",
        "option_d": "equals()",
        "correct_answer": "b",
        "explanation": "strcmp() compare deux chaînes de caractères et retourne 0 si elles sont égales.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quel est le type de retour de la fonction main() ?",
        "option_a": "void",
        "option_b": "char",
        "option_c": "int",
        "option_d": "float",
        "correct_answer": "c",
        "explanation": "La fonction main() retourne un int, généralement 0 pour indiquer un succès.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction strlen() en C ?",
        "option_a": "Alloue de la mémoire pour une chaîne",
        "option_b": "Copie une chaîne",
        "option_c": "Compare deux chaînes",
        "option_d": "Retourne la longueur d'une chaîne",
        "correct_answer": "d",
        "explanation": "strlen() retourne le nombre de caractères dans une chaîne (sans compter le \\0).",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quelle est la différence entre '=' et '==' ?",
        "option_a": "= assigne, == compare",
        "option_b": "Aucune différence",
        "option_c": "== assigne, = compare",
        "option_d": "= est plus rapide",
        "correct_answer": "a",
        "explanation": "= est l'opérateur d'assignation, == est l'opérateur de comparaison.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quelle directive de préprocesseur inclut une bibliothèque standard ?",
        "option_a": "#import",
        "option_b": "#include",
        "option_c": "#library",
        "option_d": "#use",
        "correct_answer": "b",
        "explanation": "#include permet d'inclure des fichiers d'en-tête dans le code source.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'break' dans une boucle ?",
        "option_a": "Passe à l'itération suivante",
        "option_b": "Redémarre la boucle",
        "option_c": "Sort de la boucle",
        "option_d": "Arrête le programme",
        "correct_answer": "c",
        "explanation": "'break' permet de sortir immédiatement de la boucle en cours.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'continue' dans une boucle ?",
        "option_a": "Sort de la boucle",
        "option_b": "Redémarre la boucle",
        "option_c": "Arrête le programme",
        "option_d": "Passe à l'itération suivante",
        "correct_answer": "d",
        "explanation": "'continue' passe directement à l'itération suivante de la boucle.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction scanf() en C ?",
        "option_a": "Lit l'entrée formatée",
        "option_b": "Affiche du texte",
        "option_c": "Alloue de la mémoire",
        "option_d": "Compare des chaînes",
        "correct_answer": "a",
        "explanation": "scanf() lit et formate l'entrée depuis l'entrée standard.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que signifie const devant une variable ?",
        "option_a": "Variable globale",
        "option_b": "Variable non modifiable",
        "option_c": "Variable statique",
        "option_d": "Variable automatique",
        "correct_answer": "b",
        "explanation": "const indique que la variable ne peut pas être modifiée après initialisation.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction permet de convertir une chaîne en entier en C ?",
        "option_a": "strtoint()",
        "option_b": "parseInt()",
        "option_c": "atoi()",
        "option_d": "convert()",
        "correct_answer": "c",
        "explanation": "atoi() (ASCII to Integer) convertit une chaîne en entier.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'return 0;' dans main() ?",
        "option_a": "Arrête le programme avec erreur",
        "option_b": "Redémarre le programme",
        "option_c": "Ne fait rien",
        "option_d": "Indique un succès au système",
        "correct_answer": "d",
        "explanation": "return 0 indique au système d'exploitation que le programme s'est terminé avec succès.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction copie une chaîne en C ?",
        "option_a": "strcpy()",
        "option_b": "copy()",
        "option_c": "strdup()",
        "option_d": "memcpy()",
        "correct_answer": "a",
        "explanation": "strcpy() copie une chaîne source vers une chaîne destination.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur % ?",
        "option_a": "Division",
        "option_b": "Modulo (reste de division)",
        "option_c": "Pourcentage",
        "option_d": "Multiplication",
        "correct_answer": "b",
        "explanation": "L'opérateur % retourne le reste de la division entière.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que signifie 'void' comme type de retour d'une fonction ?",
        "option_a": "Retourne un entier",
        "option_b": "Retourne un pointeur",
        "option_c": "Ne retourne rien",
        "option_d": "Retourne une erreur",
        "correct_answer": "c",
        "explanation": "void indique qu'une fonction ne retourne aucune valeur.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur sizeof(char) ?",
        "option_a": "Retourne 0",
        "option_b": "Retourne 8",
        "option_c": "Dépend du système",
        "option_d": "Retourne 1",
        "correct_answer": "d",
        "explanation": "sizeof(char) retourne toujours 1 par définition en C.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    
    # ===== QUESTIONS MOYENNES =====
    {
        "question_text": "En C, quelle fonction est utilisée pour allouer dynamiquement de la mémoire ?",
        "option_a": "malloc()",
        "option_b": "calloc()",
        "option_c": "alloc()",
        "option_d": "new()",
        "correct_answer": "a",
        "explanation": "malloc() est la fonction standard en C pour allouer dynamiquement de la mémoire.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la sortie de printf(\"%d\", 5/2) en C ?",
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
        "question_text": "Qu'est-ce qu'un pointeur en C ?",
        "option_a": "Une variable qui stocke une valeur",
        "option_b": "Une fonction",
        "option_c": "Une variable qui stocke une adresse mémoire",
        "option_d": "Un type de données",
        "correct_answer": "c",
        "explanation": "Un pointeur est une variable qui stocke l'adresse mémoire d'une autre variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur sizeof ?",
        "option_a": "Compte les éléments d'un tableau",
        "option_b": "Alloue de la mémoire",
        "option_c": "Libère de la mémoire",
        "option_d": "Retourne la taille en octets",
        "correct_answer": "d",
        "explanation": "sizeof retourne la taille en octets d'un type ou d'une variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait la fonction malloc() si elle échoue ?",
        "option_a": "Retourne NULL",
        "option_b": "Retourne 0",
        "option_c": "Lève une exception",
        "option_d": "Arrête le programme",
        "correct_answer": "a",
        "explanation": "malloc() retourne NULL si l'allocation mémoire échoue.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre char* et char[] en C ?",
        "option_a": "Aucune différence",
        "option_b": "char* est un pointeur, char[] est un tableau",
        "option_c": "char[] est plus rapide",
        "option_d": "char* utilise moins de mémoire",
        "correct_answer": "b",
        "explanation": "char* déclare un pointeur vers char, char[] déclare un tableau de caractères.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait l'opérateur & devant une variable en C ?",
        "option_a": "Déréférence la variable",
        "option_b": "Fait un ET logique",
        "option_c": "Retourne l'adresse de la variable",
        "option_d": "Concatène deux variables",
        "correct_answer": "c",
        "explanation": "L'opérateur & retourne l'adresse mémoire de la variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur * devant un pointeur ?",
        "option_a": "Retourne l'adresse",
        "option_b": "Fait une multiplication",
        "option_c": "Crée un nouveau pointeur",
        "option_d": "Déréférence le pointeur",
        "correct_answer": "d",
        "explanation": "L'opérateur * déréférence un pointeur, donnant accès à la valeur stockée à l'adresse.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que signifie l'indicateur -Wall lors de la compilation avec gcc ?",
        "option_a": "Active tous les avertissements",
        "option_b": "Compile tout",
        "option_c": "Optimise le code",
        "option_d": "Génère du code de débogage",
        "correct_answer": "a",
        "explanation": "-Wall active la plupart des messages d'avertissement utiles.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction permet de lire une ligne complète en C ?",
        "option_a": "scanf()",
        "option_b": "fgets()",
        "option_c": "gets()",
        "option_d": "readline()",
        "correct_answer": "b",
        "explanation": "fgets() est la méthode sécurisée pour lire une ligne (gets() est déprécié).",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la taille d'un int sur un système 32 bits ?",
        "option_a": "2 octets",
        "option_b": "8 octets",
        "option_c": "4 octets",
        "option_d": "Dépend du compilateur",
        "correct_answer": "c",
        "explanation": "Sur la plupart des systèmes 32 bits, un int fait 4 octets (32 bits).",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait la fonction calloc() ?",
        "option_a": "Alloue sans initialiser",
        "option_b": "Libère la mémoire",
        "option_c": "Réalloue la mémoire",
        "option_d": "Alloue et initialise à zéro",
        "correct_answer": "d",
        "explanation": "calloc() alloue de la mémoire et l'initialise à zéro.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que signifie 'static' devant une variable en C ?",
        "option_a": "Durée de vie du programme",
        "option_b": "Variable constante",
        "option_c": "Variable globale",
        "option_d": "Variable privée",
        "correct_answer": "a",
        "explanation": "static donne à la variable une durée de vie égale à celle du programme.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quel opérateur permet d'accéder aux membres d'une structure via un pointeur ?",
        "option_a": ".",
        "option_b": "->",
        "option_c": "*",
        "option_d": "&",
        "correct_answer": "b",
        "explanation": "L'opérateur -> permet d'accéder aux membres via un pointeur vers structure.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre ++i et i++ en C ?",
        "option_a": "Aucune différence",
        "option_b": "i++ est plus rapide",
        "option_c": "++i incrémente avant, i++ après",
        "option_d": "++i est déprécié",
        "correct_answer": "c",
        "explanation": "++i incrémente avant d'utiliser la valeur, i++ incrémente après.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait la directive #define ?",
        "option_a": "Définit une fonction",
        "option_b": "Inclut un fichier",
        "option_c": "Déclare une variable",
        "option_d": "Définit une macro",
        "correct_answer": "d",
        "explanation": "#define crée une macro qui sera remplacée par le préprocesseur.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction realloc() en C ?",
        "option_a": "Redimensionne mémoire allouée",
        "option_b": "Alloue nouvelle mémoire",
        "option_c": "Libère la mémoire",
        "option_d": "Initialise la mémoire",
        "correct_answer": "a",
        "explanation": "realloc() redimensionne un bloc de mémoire précédemment alloué.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la sortie de printf(\"%c\", 65) en C ?",
        "option_a": "65",
        "option_b": "A",
        "option_c": "a",
        "option_d": "Erreur",
        "correct_answer": "b",
        "explanation": "65 correspond au caractère 'A' dans la table ASCII.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur & entre deux entiers ?",
        "option_a": "Addition",
        "option_b": "Adresse mémoire",
        "option_c": "ET bit à bit",
        "option_d": "ET logique",
        "correct_answer": "c",
        "explanation": "Entre deux entiers, & effectue une opération ET bit à bit.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'goto' ?",
        "option_a": "Appelle une fonction",
        "option_b": "Sort d'une boucle",
        "option_c": "Termine le programme",
        "option_d": "Saute à une étiquette",
        "correct_answer": "d",
        "explanation": "goto fait un saut inconditionnel vers une étiquette dans le code.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre un tableau et un pointeur en C ?",
        "option_a": "Le tableau a une taille fixe",
        "option_b": "Aucune différence",
        "option_c": "Le pointeur est plus rapide",
        "option_d": "Le tableau utilise moins de mémoire",
        "correct_answer": "a",
        "explanation": "Un tableau a une taille fixe déterminée à la compilation, un pointeur peut pointer vers différentes zones.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction memset() en C ?",
        "option_a": "Copie la mémoire",
        "option_b": "Initialise la mémoire",
        "option_c": "Alloue la mémoire",
        "option_d": "Libère la mémoire",
        "correct_answer": "b",
        "explanation": "memset() initialise une zone mémoire avec une valeur donnée.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    
    # ===== QUESTIONS DIFFICILES =====
    {
        "question_text": "En C, quelle est la différence entre int *p[10] et int (*p)[10] ?",
        "option_a": "p[10] est un tableau de pointeurs, (*p)[10] est un pointeur vers tableau",
        "option_b": "Aucune différence",
        "option_c": "(*p)[10] est plus efficace",
        "option_d": "p[10] alloue plus de mémoire",
        "correct_answer": "a",
        "explanation": "int *p[10] déclare un tableau de 10 pointeurs vers int, int (*p)[10] un pointeur vers un tableau de 10 int.",
        "difficulty": "hard",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait cette déclaration : const int * const ptr ?",
        "option_a": "Pointeur vers valeur constante",
        "option_b": "Pointeur constant vers valeur constante",
        "option_c": "Pointeur constant vers valeur variable",
        "option_d": "Déclaration invalide",
        "correct_answer": "b",
        "explanation": "const int * const ptr est un pointeur constant vers une valeur constante (ni le pointeur ni la valeur ne peuvent être modifiés).",
        "difficulty": "hard",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait le mot-clé volatile ?",
        "option_a": "Optimise les accès mémoire",
        "option_b": "Rend la variable constante",
        "option_c": "Empêche l'optimisation du compilateur",
        "option_d": "Alloue en mémoire volatile",
        "correct_answer": "c",
        "explanation": "volatile indique au compilateur de ne pas optimiser les accès à cette variable.",
        "difficulty": "hard",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre union et struct en C ?",
        "option_a": "union est plus rapide",
        "option_b": "struct est déprécié",
        "option_c": "Aucune différence",
        "option_d": "struct alloue de la mémoire séparée, union partage la même mémoire",
        "correct_answer": "d",
        "explanation": "Dans une struct, chaque membre a sa propre mémoire. Dans une union, tous les membres partagent la même zone mémoire.",
        "difficulty": "hard",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que signifie cette déclaration : int (*func)(int, int) ?",
        "option_a": "Pointeur vers fonction qui prend deux int et retourne int",
        "option_b": "Fonction qui retourne un pointeur vers int",
        "option_c": "Tableau de fonctions",
        "option_d": "Déclaration invalide",
        "correct_answer": "a",
        "explanation": "int (*func)(int, int) déclare un pointeur vers une fonction qui prend deux paramètres int et retourne un int.",
        "difficulty": "hard",
        "category": "c-programming"
    }
]

def populate_questions():
    """Peuple la base de données avec les questions de quiz"""
    db = SessionLocal()
    try:
        # Choix de la difficulté
        print("Choisissez le niveau de difficulté à ajouter:")
        print("1. Facile (easy)")
        print("2. Moyen (medium)")
        print("3. Difficile (hard)")
        print("4. Tous les niveaux")
        
        choice = input("Votre choix (1-4): ").strip()
        
        difficulty_filter = None
        if choice == "1":
            difficulty_filter = "easy"
        elif choice == "2":
            difficulty_filter = "medium"
        elif choice == "3":
            difficulty_filter = "hard"
        elif choice == "4":
            difficulty_filter = None
        else:
            print("Choix invalide. Ajout de tous les niveaux.")
            difficulty_filter = None
        
        # Filtrer les questions selon la difficulté choisie
        if difficulty_filter:
            questions_to_add = [q for q in QUIZ_QUESTIONS if q['difficulty'] == difficulty_filter]
            print(f"Ajout des questions de niveau: {difficulty_filter}")
        else:
            questions_to_add = QUIZ_QUESTIONS
            print("Ajout de toutes les questions")
        
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
        for q_data in questions_to_add:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        print(f"✅ {len(questions_to_add)} questions ajoutées avec succès!")
        
        # Afficher un résumé par difficulté
        difficulties = {}
        for q in questions_to_add:
            diff = q['difficulty']
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        print("\nRépartition par difficulté:")
        for difficulty, count in difficulties.items():
            print(f"  - {difficulty}: {count} questions")
            
        # Résumé des bonnes réponses
        answers = {}
        for q in questions_to_add:
            ans = q['correct_answer']
            answers[ans] = answers.get(ans, 0) + 1
        
        print("\nRépartition des bonnes réponses:")
        for answer, count in sorted(answers.items()):
            percentage = (count / len(questions_to_add)) * 100
            print(f"  - Option {answer.upper()}: {count} questions ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des questions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Peuplement de la base de données avec les questions de quiz...")
    populate_questions()
    print("✨ Terminé!")

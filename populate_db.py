#!/usr/bin/env python3
"""
Script pour peupler la base de données avec des questions de quiz
style PLD Holberton School
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
QUIZ_QUESTIONS = [
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
        "option_b": "Une variable qui stocke une adresse mémoire",
        "option_c": "Une fonction",
        "option_d": "Un type de données",
        "correct_answer": "b",
        "explanation": "Un pointeur est une variable qui stocke l'adresse mémoire d'une autre variable.",
        "difficulty": "medium",
        "category": "c-programming"
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
        "question_text": "Que fait l'opérateur & devant une variable en C ?",
        "option_a": "Déréférence la variable",
        "option_b": "Retourne l'adresse de la variable",
        "option_c": "Fait un ET logique",
        "option_d": "Concatène deux variables",
        "correct_answer": "b",
        "explanation": "L'opérateur & retourne l'adresse mémoire de la variable.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quelle fonction libère la mémoire allouée par malloc() ?",
        "option_a": "delete()",
        "option_b": "free()",
        "option_c": "release()",
        "option_d": "dealloc()",
        "correct_answer": "b",
        "explanation": "free() libère la mémoire précédemment allouée par malloc(), calloc() ou realloc().",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la valeur de NULL en C ?",
        "option_a": "-1",
        "option_b": "0",
        "option_c": "1",
        "option_d": "undefined",
        "correct_answer": "b",
        "explanation": "NULL est défini comme 0 en C, représentant un pointeur qui ne pointe vers rien.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur * devant un pointeur ?",
        "option_a": "Retourne l'adresse",
        "option_b": "Déréférence le pointeur",
        "option_c": "Fait une multiplication",
        "option_d": "Crée un nouveau pointeur",
        "correct_answer": "b",
        "explanation": "L'opérateur * déréférence un pointeur, donnant accès à la valeur stockée à l'adresse.",
        "difficulty": "medium",
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
        "option_b": "int",
        "option_c": "char",
        "option_d": "float",
        "correct_answer": "b",
        "explanation": "La fonction main() retourne un int, généralement 0 pour indiquer un succès.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction strlen() en C ?",
        "option_a": "Alloue de la mémoire pour une chaîne",
        "option_b": "Retourne la longueur d'une chaîne",
        "option_c": "Copie une chaîne",
        "option_d": "Compare deux chaînes",
        "correct_answer": "b",
        "explanation": "strlen() retourne le nombre de caractères dans une chaîne (sans compter le \\0).",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quelle est la différence entre '=' et '==' ?",
        "option_a": "Aucune différence",
        "option_b": "= assigne, == compare",
        "option_c": "== assigne, = compare",
        "option_d": "= est plus rapide",
        "correct_answer": "b",
        "explanation": "= est l'opérateur d'assignation, == est l'opérateur de comparaison.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que signifie l'indicateur -Wall lors de la compilation avec gcc ?",
        "option_a": "Compile tout",
        "option_b": "Active tous les avertissements",
        "option_c": "Optimise le code",
        "option_d": "Génère du code de débogage",
        "correct_answer": "b",
        "explanation": "-Wall active la plupart des messages d'avertissement utiles.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, quel caractère termine une chaîne de caractères ?",
        "option_a": "'\\n'",
        "option_b": "'\\0'",
        "option_c": "'\\t'",
        "option_d": "EOF",
        "correct_answer": "b",
        "explanation": "Le caractère null '\\0' marque la fin d'une chaîne de caractères en C.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction printf() en C ?",
        "option_a": "Lit une entrée utilisateur",
        "option_b": "Affiche du texte formaté",
        "option_c": "Alloue de la mémoire",
        "option_d": "Compile le programme",
        "correct_answer": "b",
        "explanation": "printf() affiche du texte formaté sur la sortie standard.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'break' dans une boucle ?",
        "option_a": "Passe à l'itération suivante",
        "option_b": "Sort de la boucle",
        "option_c": "Redémarre la boucle",
        "option_d": "Arrête le programme",
        "correct_answer": "b",
        "explanation": "'break' permet de sortir immédiatement de la boucle en cours.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction permet de lire une ligne complète en C ?",
        "option_a": "scanf()",
        "option_b": "gets()",
        "option_c": "fgets()",
        "option_d": "readline()",
        "correct_answer": "c",
        "explanation": "fgets() est la méthode sécurisée pour lire une ligne (gets() est déprécié).",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'continue' dans une boucle ?",
        "option_a": "Sort de la boucle",
        "option_b": "Passe à l'itération suivante",
        "option_c": "Redémarre la boucle",
        "option_d": "Arrête le programme",
        "correct_answer": "b",
        "explanation": "'continue' passe directement à l'itération suivante de la boucle.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la taille d'un int sur un système 32 bits ?",
        "option_a": "2 octets",
        "option_b": "4 octets",
        "option_c": "8 octets",
        "option_d": "Dépend du compilateur",
        "correct_answer": "b",
        "explanation": "Sur la plupart des systèmes 32 bits, un int fait 4 octets (32 bits).",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait la fonction calloc() ?",
        "option_a": "Alloue et initialise à zéro",
        "option_b": "Alloue sans initialiser",
        "option_c": "Libère la mémoire",
        "option_d": "Réalloue la mémoire",
        "correct_answer": "a",
        "explanation": "calloc() alloue de la mémoire et l'initialise à zéro.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Que signifie 'static' devant une variable en C ?",
        "option_a": "Variable constante",
        "option_b": "Variable globale",
        "option_c": "Durée de vie du programme",
        "option_d": "Variable privée",
        "correct_answer": "c",
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
        "question_text": "Que fait la fonction scanf() en C ?",
        "option_a": "Affiche du texte",
        "option_b": "Lit l'entrée formatée",
        "option_c": "Alloue de la mémoire",
        "option_d": "Compare des chaînes",
        "correct_answer": "b",
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
        "option_b": "atoi()",
        "option_c": "parseInt()",
        "option_d": "convert()",
        "correct_answer": "b",
        "explanation": "atoi() (ASCII to Integer) convertit une chaîne en entier.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'return 0;' dans main() ?",
        "option_a": "Arrête le programme avec erreur",
        "option_b": "Indique un succès au système",
        "option_c": "Redémarre le programme",
        "option_d": "Ne fait rien",
        "correct_answer": "b",
        "explanation": "return 0 indique au système d'exploitation que le programme s'est terminé avec succès.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre ++i et i++ en C ?",
        "option_a": "Aucune différence",
        "option_b": "++i incrémente avant, i++ après",
        "option_c": "i++ est plus rapide",
        "option_d": "++i est déprécié",
        "correct_answer": "b",
        "explanation": "++i incrémente avant d'utiliser la valeur, i++ incrémente après.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait la directive #define ?",
        "option_a": "Définit une fonction",
        "option_b": "Définit une macro",
        "option_c": "Inclut un fichier",
        "option_d": "Déclare une variable",
        "correct_answer": "b",
        "explanation": "#define crée une macro qui sera remplacée par le préprocesseur.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction copie une chaîne en C ?",
        "option_a": "copy()",
        "option_b": "strcpy()",
        "option_c": "strdup()",
        "option_d": "memcpy()",
        "correct_answer": "b",
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
        "question_text": "Que fait la fonction realloc() en C ?",
        "option_a": "Alloue nouvelle mémoire",
        "option_b": "Redimensionne mémoire allouée",
        "option_c": "Libère la mémoire",
        "option_d": "Initialise la mémoire",
        "correct_answer": "b",
        "explanation": "realloc() redimensionne un bloc de mémoire précédemment alloué.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que signifie 'void' comme type de retour d'une fonction ?",
        "option_a": "Retourne un entier",
        "option_b": "Ne retourne rien",
        "option_c": "Retourne un pointeur",
        "option_d": "Retourne une erreur",
        "correct_answer": "b",
        "explanation": "void indique qu'une fonction ne retourne aucune valeur.",
        "difficulty": "easy",
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
        "option_b": "ET bit à bit",
        "option_c": "Adresse mémoire",
        "option_d": "ET logique",
        "correct_answer": "b",
        "explanation": "Entre deux entiers, & effectue une opération ET bit à bit.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction concatène deux chaînes en C ?",
        "option_a": "concat()",
        "option_b": "strcat()",
        "option_c": "append()",
        "option_d": "join()",
        "correct_answer": "b",
        "explanation": "strcat() concatène la chaîne source à la fin de la chaîne destination.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'goto' ?",
        "option_a": "Appelle une fonction",
        "option_b": "Saute à une étiquette",
        "option_c": "Sort d'une boucle",
        "option_d": "Termine le programme",
        "correct_answer": "b",
        "explanation": "goto fait un saut inconditionnel vers une étiquette dans le code.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle est la différence entre un tableau et un pointeur en C ?",
        "option_a": "Aucune différence",
        "option_b": "Le tableau a une taille fixe",
        "option_c": "Le pointeur est plus rapide",
        "option_d": "Le tableau utilise moins de mémoire",
        "correct_answer": "b",
        "explanation": "Un tableau a une taille fixe déterminée à la compilation, un pointeur peut pointer vers différentes zones.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur sizeof(char) ?",
        "option_a": "Retourne 0",
        "option_b": "Retourne 1",
        "option_c": "Retourne 8",
        "option_d": "Dépend du système",
        "correct_answer": "b",
        "explanation": "sizeof(char) retourne toujours 1 par définition en C.",
        "difficulty": "easy",
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
    {
        "question_text": "En C, que signifie l'erreur 'Segmentation fault' ?",
        "option_a": "Erreur de syntaxe",
        "option_b": "Accès mémoire invalide",
        "option_c": "Division par zéro",
        "option_d": "Fichier non trouvé",
        "correct_answer": "b",
        "explanation": "Segmentation fault indique un accès à une zone mémoire non autorisée.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction permet de fermer un fichier en C ?",
        "option_a": "close()",
        "option_b": "fclose()",
        "option_c": "end()",
        "option_d": "stop()",
        "correct_answer": "b",
        "explanation": "fclose() ferme un fichier ouvert avec fopen().",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'opérateur ternaire ?: ?",
        "option_a": "Compare trois valeurs",
        "option_b": "Condition compacte if-else",
        "option_c": "Boucle for simplifiée",
        "option_d": "Déclaration de variable",
        "correct_answer": "b",
        "explanation": "L'opérateur ternaire (condition ? valeur1 : valeur2) est un if-else compact.",
        "difficulty": "medium",
        "category": "c-programming"
    },
    {
        "question_text": "Quelle fonction ouvre un fichier en C ?",
        "option_a": "open()",
        "option_b": "fopen()",
        "option_c": "file()",
        "option_d": "read()",
        "correct_answer": "b",
        "explanation": "fopen() ouvre un fichier et retourne un pointeur vers FILE.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "En C, que fait l'instruction 'switch' ?",
        "option_a": "Boucle conditionnelle",
        "option_b": "Sélection multiple",
        "option_c": "Échange de variables",
        "option_d": "Arrêt du programme",
        "correct_answer": "b",
        "explanation": "switch permet de faire une sélection parmi plusieurs cas possibles.",
        "difficulty": "easy",
        "category": "c-programming"
    },
    {
        "question_text": "Que fait la fonction exit() en C ?",
        "option_a": "Sort d'une fonction",
        "option_b": "Termine le programme",
        "option_c": "Sort d'une boucle",
        "option_d": "Ferme un fichier",
        "correct_answer": "b",
        "explanation": "exit() termine immédiatement l'exécution du programme.",
        "difficulty": "easy",
        "category": "c-programming"
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

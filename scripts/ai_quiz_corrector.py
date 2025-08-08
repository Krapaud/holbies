#!/usr/bin/env python3
"""
Quiz interactif avec saisie manuelle et correction par IA
Système de scoring basé sur la proximité de la réponse et l'usage de termes techniques
"""

import re
import difflib
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Question:
    """Structure d'une question de quiz avec réponse textuelle"""
    id: int
    question_text: str
    expected_answer: str
    technical_terms: List[str]
    explanation: str
    difficulty: str
    category: str
    max_score: int = 100

class AIQuizCorrector:
    """Correcteur IA pour les réponses textuelles"""
    
    def __init__(self):
        self.bonus_multiplier = 1.2  # Multiplicateur pour les termes techniques
        self.similarity_weight = 0.7  # Poids de la similarité textuelle
        self.technical_weight = 0.3   # Poids des termes techniques
        
    def normalize_text(self, text: str) -> str:
        """Normalise le texte pour la comparaison"""
        # Supprime la ponctuation et met en minuscules
        text = re.sub(r'[^\w\s]', '', text.lower())
        # Supprime les espaces multiples
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def calculate_similarity(self, user_answer: str, expected_answer: str) -> float:
        """Calcule la similarité entre deux textes"""
        user_norm = self.normalize_text(user_answer)
        expected_norm = self.normalize_text(expected_answer)
        
        # Utilise la similarité de séquence
        similarity = difflib.SequenceMatcher(None, user_norm, expected_norm).ratio()
        
        # Bonus pour les mots-clés présents
        user_words = set(user_norm.split())
        expected_words = set(expected_norm.split())
        word_overlap = len(user_words.intersection(expected_words)) / len(expected_words) if expected_words else 0
        
        # Moyenne pondérée
        return (similarity * 0.6 + word_overlap * 0.4)
    
    def find_technical_terms(self, user_answer: str, technical_terms: List[str]) -> List[str]:
        """Trouve les termes techniques utilisés dans la réponse"""
        user_norm = self.normalize_text(user_answer)
        found_terms = []
        
        for term in technical_terms:
            term_norm = self.normalize_text(term)
            if term_norm in user_norm:
                found_terms.append(term)
        
        return found_terms
    
    def correct_answer(self, question: Question, user_answer: str) -> Dict:
        """Corrige une réponse utilisateur et attribue un score"""
        if not user_answer.strip():
            return {
                'score': 0,
                'max_score': question.max_score,
                'percentage': 0,
                'similarity': 0,
                'technical_terms_found': [],
                'technical_bonus': 0,
                'feedback': "Aucune réponse fournie.",
                'detailed_explanation': question.explanation
            }
        
        # Calcul de la similarité
        similarity = self.calculate_similarity(user_answer, question.expected_answer)
        
        # Recherche des termes techniques
        technical_terms_found = self.find_technical_terms(user_answer, question.technical_terms)
        technical_ratio = len(technical_terms_found) / len(question.technical_terms) if question.technical_terms else 0
        
        # Score de base basé sur la similarité et les termes techniques
        base_score = (similarity * self.similarity_weight + technical_ratio * self.technical_weight) * question.max_score
        
        # Bonus pour les termes techniques
        technical_bonus = len(technical_terms_found) * 5  # 5 points par terme technique
        
        # Score final
        final_score = min(base_score + technical_bonus, question.max_score)
        
        # Génération du feedback
        feedback = self.generate_feedback(similarity, technical_terms_found, question.technical_terms, final_score, question.max_score)
        
        return {
            'score': round(final_score, 1),
            'max_score': question.max_score,
            'percentage': round((final_score / question.max_score) * 100, 1),
            'similarity': round(similarity * 100, 1),
            'technical_terms_found': technical_terms_found,
            'technical_bonus': technical_bonus,
            'feedback': feedback,
            'detailed_explanation': question.explanation
        }
    
    def generate_feedback(self, similarity: float, found_terms: List[str], all_terms: List[str], score: float, max_score: float) -> str:
        """Génère un feedback personnalisé"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            feedback = "🏆 Excellente réponse ! "
        elif percentage >= 75:
            feedback = "👍 Très bonne réponse ! "
        elif percentage >= 60:
            feedback = "📚 Bonne réponse, mais peut être améliorée. "
        elif percentage >= 40:
            feedback = "💪 Réponse partiellement correcte. "
        else:
            feedback = "📖 La réponse nécessite des améliorations importantes. "
        
        # Ajout d'informations sur les termes techniques
        if found_terms:
            feedback += f"Termes techniques utilisés correctement : {', '.join(found_terms)}. "
        
        missed_terms = [term for term in all_terms if term not in found_terms]
        if missed_terms:
            feedback += f"Termes techniques manqués : {', '.join(missed_terms)}. "
        
        feedback += f"Similarité avec la réponse attendue : {similarity * 100:.1f}%."
        
        return feedback

class AIQuizGame:
    """Jeu de quiz avec correction IA"""
    
    def __init__(self):
        self.corrector = AIQuizCorrector()
        self.questions = self.load_questions()
        self.current_question_index = 0
        self.total_score = 0
        self.max_total_score = 0
        self.results = []
    
    def load_questions(self) -> List[Question]:
        """Charge les questions depuis la base de données des quiz"""
        questions_data = [
            {
                "id": 1,
                "question_text": "Expliquez ce qu'est un pointeur en C et comment il fonctionne.",
                "expected_answer": "Un pointeur est une variable qui stocke l'adresse mémoire d'une autre variable. Il permet d'accéder indirectement aux données en mémoire en utilisant l'opérateur de déréférencement *.",
                "technical_terms": ["pointeur", "adresse mémoire", "variable", "déréférencement", "opérateur *", "indirection"],
                "explanation": "Un pointeur en C est fondamental pour la gestion de la mémoire dynamique et l'efficacité du code. L'opérateur & récupère l'adresse d'une variable, tandis que * déréférence un pointeur pour accéder à la valeur.",
                "difficulty": "medium",
                "category": "c-programming"
            },
            {
                "id": 2,
                "question_text": "Décrivez la différence entre malloc() et calloc() en C.",
                "expected_answer": "malloc() alloue un bloc de mémoire de taille spécifiée sans l'initialiser, tandis que calloc() alloue de la mémoire pour un tableau d'éléments et initialise tous les octets à zéro.",
                "technical_terms": ["malloc", "calloc", "allocation dynamique", "mémoire", "initialisation", "zéro", "heap", "octets"],
                "explanation": "malloc() est plus rapide car elle n'initialise pas la mémoire, mais calloc() garantit une mémoire propre initialisée à zéro, ce qui peut éviter des bugs liés aux valeurs non initialisées.",
                "difficulty": "medium",
                "category": "c-programming"
            },
            {
                "id": 3,
                "question_text": "Qu'est-ce que la segmentation fault et pourquoi se produit-elle ?",
                "expected_answer": "Une segmentation fault est une erreur qui se produit quand un programme tente d'accéder à une zone mémoire qui ne lui appartient pas ou qui n'est pas autorisée, souvent causée par un déréférencement de pointeur invalide.",
                "technical_terms": ["segmentation fault", "SIGSEGV", "mémoire", "pointeur invalide", "déréférencement", "accès mémoire", "protection mémoire"],
                "explanation": "Les segmentation faults sont un mécanisme de protection du système d'exploitation pour empêcher les programmes d'écraser la mémoire d'autres processus ou du système.",
                "difficulty": "medium",
                "category": "c-programming"
            },
            {
                "id": 4,
                "question_text": "Expliquez le concept de gestion automatique de la mémoire vs manuelle en C.",
                "expected_answer": "En C, la gestion mémoire est manuelle : le programmeur doit explicitement allouer avec malloc/calloc et libérer avec free. Contrairement aux langages avec garbage collector, C donne le contrôle total mais exige une discipline stricte.",
                "technical_terms": ["gestion mémoire", "malloc", "free", "garbage collector", "allocation manuelle", "libération", "fuites mémoire", "stack", "heap"],
                "explanation": "La gestion manuelle offre performance et contrôle précis, mais augmente le risque de fuites mémoire et d'erreurs. Les langages modernes automatisent souvent cette gestion.",
                "difficulty": "hard",
                "category": "c-programming"
            },
            {
                "id": 5,
                "question_text": "Décrivez ce qui se passe lors de la compilation d'un programme C.",
                "expected_answer": "La compilation C se fait en plusieurs étapes : préprocesseur (macros, includes), compilateur (code source vers assembleur), assembleur (assembleur vers code objet), et éditeur de liens (liaison des modules pour créer l'exécutable).",
                "technical_terms": ["préprocesseur", "compilateur", "assembleur", "éditeur de liens", "linker", "code objet", "exécutable", "macros", "bibliothèques"],
                "explanation": "Chaque étape a un rôle spécifique : le préprocesseur traite les directives, le compilateur optimise et génère du code machine, l'éditeur de liens résout les symboles externes.",
                "difficulty": "hard",
                "category": "c-programming"
            },
            {
                "id": 6,
                "question_text": "Expliquez la différence entre une variable automatique et statique en C.",
                "expected_answer": "Une variable automatique (locale) est créée à l'entrée d'une fonction et détruite à la sortie, stockée sur la pile. Une variable statique conserve sa valeur entre les appels de fonction et existe pendant toute la durée du programme.",
                "technical_terms": ["variable automatique", "variable statique", "pile", "stack", "durée de vie", "portée", "allocation", "fonction"],
                "explanation": "Les variables automatiques sont efficaces en mémoire mais temporaires, tandis que les variables statiques permettent de conserver un état entre les appels mais consomment de la mémoire en permanence.",
                "difficulty": "medium",
                "category": "c-programming"
            },
            {
                "id": 7,
                "question_text": "Qu'est-ce qu'un buffer overflow et comment peut-on l'éviter ?",
                "expected_answer": "Un buffer overflow se produit quand des données écrites dans un buffer dépassent sa taille allouée, écrasant la mémoire adjacente. On peut l'éviter en utilisant des fonctions sécurisées comme strncpy, snprintf, et en validant les tailles d'entrée.",
                "technical_terms": ["buffer overflow", "débordement", "buffer", "strncpy", "snprintf", "validation", "sécurité", "mémoire adjacente"],
                "explanation": "Les buffer overflows sont une source majeure de vulnérabilités de sécurité. La programmation défensive avec vérification des bornes est essentielle.",
                "difficulty": "hard",
                "category": "c-programming"
            },
            {
                "id": 8,
                "question_text": "Expliquez le rôle et l'utilisation de l'opérateur sizeof en C.",
                "expected_answer": "L'opérateur sizeof retourne la taille en octets d'un type de données ou d'une variable au moment de la compilation. Il est essentiel pour l'allocation dynamique et la portabilité entre différentes architectures.",
                "technical_terms": ["sizeof", "octets", "compilation", "allocation dynamique", "portabilité", "architecture", "type de données"],
                "explanation": "sizeof est évalué à la compilation, pas à l'exécution. Il garantit la portabilité car la taille des types peut varier selon les systèmes (32-bit vs 64-bit).",
                "difficulty": "easy",
                "category": "c-programming"
            },
            {
                "id": 9,
                "question_text": "Décrivez les différences entre les opérateurs de pré et post-incrémentation en C.",
                "expected_answer": "L'opérateur de pré-incrémentation (++i) incrémente la variable puis retourne sa nouvelle valeur. Le post-incrémentation (i++) retourne la valeur actuelle puis incrémente. La différence est importante dans les expressions complexes.",
                "technical_terms": ["pré-incrémentation", "post-incrémentation", "++i", "i++", "valeur de retour", "expression", "effet de bord"],
                "explanation": "Cette distinction est cruciale dans les boucles et expressions où l'ordre d'évaluation affecte le résultat. Le pré-incrémentation peut être légèrement plus efficace en C++.",
                "difficulty": "medium",
                "category": "c-programming"
            },
            {
                "id": 10,
                "question_text": "Expliquez le concept de récursion en C et donnez un exemple d'utilisation.",
                "expected_answer": "La récursion est une technique où une fonction s'appelle elle-même pour résoudre un problème en le décomposant en sous-problèmes similaires. Exemple : calcul factoriel où fact(n) = n * fact(n-1) avec un cas de base fact(0) = 1.",
                "technical_terms": ["récursion", "fonction récursive", "cas de base", "pile d'appels", "factoriel", "sous-problèmes", "auto-appel"],
                "explanation": "La récursion nécessite un cas de base pour éviter l'infini. Elle consomme de la mémoire pile et peut causer un stack overflow si trop profonde.",
                "difficulty": "medium",
                "category": "c-programming"
            }
        ]
        
        return [Question(**q) for q in questions_data]
    
    def display_question(self, question: Question) -> None:
        """Affiche une question"""
        print(f"\n{'='*60}")
        print(f"QUESTION {question.id} - Difficulté: {question.difficulty.upper()}")
        print(f"{'='*60}")
        print(f"\n{question.question_text}\n")
        print("Répondez de manière détaillée en utilisant des termes techniques appropriés.")
        print("Plus votre réponse est précise et technique, plus votre score sera élevé.")
        print(f"Score maximum: {question.max_score} points")
        print("-" * 60)
    
    def get_user_answer(self) -> str:
        """Récupère la réponse de l'utilisateur"""
        print("\nVotre réponse:")
        lines = []
        print("(Tapez '###' sur une ligne vide pour terminer votre réponse)")
        
        while True:
            try:
                line = input()
                if line.strip() == '###':
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n\nQuiz interrompu.")
                return ""
        
        return '\n'.join(lines)
    
    def display_results(self, result: Dict, question: Question) -> None:
        """Affiche les résultats de la correction"""
        print(f"\n{'='*60}")
        print("RÉSULTATS DE LA CORRECTION")
        print(f"{'='*60}")
        print(f"Score obtenu: {result['score']:.1f}/{result['max_score']} points ({result['percentage']:.1f}%)")
        print(f"Similarité avec la réponse attendue: {result['similarity']:.1f}%")
        
        if result['technical_terms_found']:
            print(f"Termes techniques utilisés: {', '.join(result['technical_terms_found'])}")
            print(f"Bonus technique: +{result['technical_bonus']} points")
        
        print(f"\n📝 Feedback: {result['feedback']}")
        
        print(f"\n💡 Réponse attendue:")
        print(f"{question.expected_answer}")
        
        print(f"\n📚 Explication détaillée:")
        print(f"{result['detailed_explanation']}")
        
        print(f"\n⚡ Termes techniques importants pour cette question:")
        print(f"{', '.join(question.technical_terms)}")
        print("-" * 60)
    
    def display_final_score(self) -> None:
        """Affiche le score final"""
        percentage = (self.total_score / self.max_total_score) * 100 if self.max_total_score > 0 else 0
        
        print(f"\n{'='*60}")
        print("RÉSULTATS FINAUX DU QUIZ")
        print(f"{'='*60}")
        print(f"Score total: {self.total_score:.1f}/{self.max_total_score} points")
        print(f"Pourcentage: {percentage:.1f}%")
        
        if percentage >= 90:
            print("🏆 Excellent ! Vous maîtrisez parfaitement ces concepts.")
        elif percentage >= 75:
            print("👍 Très bien ! Quelques améliorations possibles.")
        elif percentage >= 60:
            print("📚 Correct ! Continuez à étudier pour améliorer vos connaissances.")
        elif percentage >= 40:
            print("💪 Effort appréciable ! Il y a encore du travail à faire.")
        else:
            print("📖 Il est temps de revoir les bases !")
        
        print(f"\nDétail par question:")
        for i, result in enumerate(self.results, 1):
            print(f"Question {i}: {result['score']:.1f}/{result['max_score']} points ({result['percentage']:.1f}%)")
        
        print(f"{'='*60}")
    
    def run_quiz(self) -> None:
        """Lance le quiz interactif"""
        print("🧠 QUIZ INTERACTIF AVEC CORRECTION IA")
        print("Répondez aux questions de manière détaillée pour obtenir le meilleur score !")
        
        for i, question in enumerate(self.questions):
            self.display_question(question)
            user_answer = self.get_user_answer()
            
            if not user_answer:  # Quiz interrompu
                break
            
            result = self.corrector.correct_answer(question, user_answer)
            self.results.append(result)
            self.total_score += result['score']
            self.max_total_score += result['max_score']
            
            self.display_results(result, question)
            
            # Demander si continuer
            if i < len(self.questions) - 1:
                print(f"\nQuestion suivante ? (o/n): ", end="")
                continue_quiz = input().strip().lower()
                if continue_quiz in ['n', 'non', 'no']:
                    break
        
        self.display_final_score()

def main():
    """Fonction principale"""
    try:
        quiz = AIQuizGame()
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\n\n👋 Quiz terminé. À bientôt !")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()

"""
Module d'IA pour générer des feedbacks intelligents
Version simplifiée avec fallback intelligent si Hugging Face n'est pas disponible
"""
import json
from typing import Dict, List

# Import de Hugging Face Transformers (optionnel)
try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
    print("🤖 Hugging Face Transformers disponible - Mode IA activé !")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("📚 Mode feedback intelligent local (Hugging Face non installé)")
    print("💡 Pour activer l'IA: ./scripts/install-ai-gratuit.sh")

class AIFeedbackGenerator:
    """Générateur de feedback IA avec fallback intelligent"""
    
    def __init__(self):
        self.ai_model = None
        self.using_ai = False
        
        if TRANSFORMERS_AVAILABLE:
            try:
                print("� Tentative de chargement du modèle IA...")
                # Utiliser un modèle plus léger pour commencer
                self.ai_model = pipeline(
                    "text-generation", 
                    model="gpt2",
                    device=-1,  # CPU
                    max_length=100
                )
                self.using_ai = True
                print("✅ Modèle IA chargé avec succès - Feedback IA activé !")
            except Exception as e:
                print(f"⚠️ Erreur chargement modèle IA: {e}")
                print("📚 Utilisation du feedback intelligent local")
        else:
            print("📚 Mode feedback intelligent local actif")
    
    def generate_intelligent_feedback(
        self, 
        user_answer: str, 
        question_text: str, 
        expected_answer: str,
        technical_terms: List[str],
        score: float,
        max_score: float
    ) -> Dict[str, str]:
        """
        Génère un feedback intelligent avec IA ou fallback local
        """
        if self.using_ai and self.ai_model:
            return self._generate_ai_feedback(
                user_answer, question_text, expected_answer, 
                technical_terms, score, max_score
            )
        else:
            return self._generate_smart_local_feedback(
                user_answer, question_text, expected_answer, 
                technical_terms, score, max_score
            )
    
    def _generate_ai_feedback(
        self, 
        user_answer: str, 
        question_text: str, 
        expected_answer: str,
        technical_terms: List[str],
        score: float,
        max_score: float
    ) -> Dict[str, str]:
        """Génère un feedback avec l'IA Hugging Face"""
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        try:
            # Prompt optimisé pour l'éducation technique
            context = f"Question: {question_text}\nRéponse: {user_answer}\nScore: {percentage:.0f}%"
            
            # Prompt éducatif français
            prompt = f"Professeur évaluant un étudiant:\n{context}\nFeedback pédagogique:"
            
            # Génération IA
            response = self.ai_model(
                prompt, 
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.ai_model.tokenizer.eos_token_id
            )
            
            ai_text = response[0]['generated_text'].replace(prompt, '').strip()
            
            # Analyser la réponse utilisateur
            terms_found = [term for term in technical_terms if term.lower() in user_answer.lower()]
            user_words = set(user_answer.lower().split())
            expected_words = set(expected_answer.lower().split())
            common_words = user_words.intersection(expected_words)
            
            # Structurer le feedback selon le score
            if percentage >= 80:
                feedback_principal = f"Excellente maîtrise ! {ai_text[:80]}... Vous démontrez une compréhension solide."
                points_forts = f"Usage correct de {len(terms_found)} terme(s) technique(s). Réponse bien structurée avec {len(common_words)} éléments clés."
                points_amelioration = "Votre niveau est très bon, continuez à approfondir pour atteindre l'excellence."
                conseils_techniques = f"Pour perfectionner: réviser {', '.join([t for t in technical_terms if t not in terms_found][:2])}"
                encouragement = "🏆 Performance exceptionnelle ! L'IA reconnaît votre expertise."
                
            elif percentage >= 60:
                feedback_principal = f"Bonne compréhension de base. {ai_text[:80]}... Quelques améliorations possibles."
                points_forts = f"L'IA détecte {len(terms_found)} terme(s) technique(s) corrects et {len(common_words)} éléments pertinents."
                points_amelioration = "Enrichissez votre réponse avec plus de précision et de détails techniques."
                conseils_techniques = f"Focalisez-vous sur: {', '.join(technical_terms[:3])}"
                encouragement = "👍 L'IA confirme: vous êtes sur la bonne voie !"
                
            elif percentage >= 40:
                feedback_principal = f"Compréhension partielle. {ai_text[:80]}... Besoin d'approfondissement."
                points_forts = f"L'IA reconnaît {len(common_words)} éléments corrects dans votre réponse."
                points_amelioration = "Développez davantage vos connaissances techniques et utilisez le vocabulaire approprié."
                conseils_techniques = f"Concepts clés à maîtriser: {', '.join(technical_terms[:2])}"
                encouragement = "� L'IA vous encourage: continuez vos efforts !"
                
            else:
                feedback_principal = f"Il faut reprendre les bases. {ai_text[:80]}... Ne vous découragez pas."
                points_forts = f"L'IA note votre effort avec une réponse de {len(user_answer)} caractères."
                points_amelioration = "Revoyez les concepts fondamentaux avant de continuer."
                conseils_techniques = f"Priorité absolue: {', '.join(technical_terms[:2])}"
                encouragement = "💪 L'IA croit en vous: chaque erreur est un apprentissage !"
                
            return {
                "feedback_principal": feedback_principal,
                "points_forts": points_forts,
                "points_amelioration": points_amelioration,
                "conseils_techniques": conseils_techniques,
                "encouragement": encouragement
            }
            
        except Exception as e:
            # Feedback d'urgence si l'IA échoue
            return {
                "feedback_principal": f"Erreur IA ({e}), mais votre score de {percentage:.0f}% montre votre niveau.",
                "points_forts": f"Détection de {len(terms_found)} terme(s) technique(s) dans votre réponse.",
                "points_amelioration": "Réessayez en détaillant davantage votre réponse.",
                "conseils_techniques": f"Concepts importants: {', '.join(technical_terms[:3])}",
                "encouragement": "🔧 Système en cours d'optimisation, continuez à apprendre !"
            }
    
    def _generate_smart_local_feedback(
        self, 
        user_answer: str, 
        question_text: str, 
        expected_answer: str,
        technical_terms: List[str],
        score: float,
        max_score: float
    ) -> Dict[str, str]:
        """Génère un feedback intelligent local (sans IA externe)"""
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        # Analyse avancée de la réponse
        user_words = set(user_answer.lower().split())
        expected_words = set(expected_answer.lower().split())
        common_words = user_words.intersection(expected_words)
        terms_found = [term for term in technical_terms if term.lower() in user_answer.lower()]
        answer_length = len(user_answer.strip())
        
        # Analyse sémantique basique
        command_keywords = ['chmod', 'chown', 'sudo', 'mkdir', 'rm', 'cp', 'mv', 'ls', 'cd', 'pwd']
        commands_used = [cmd for cmd in command_keywords if cmd in user_answer.lower()]
        
        # Feedback adaptatif selon le score
        if percentage >= 85:
            feedback_principal = f"🏆 Excellente maîtrise ! Votre réponse démontre une compréhension parfaite avec {len(common_words)} éléments-clés identifiés."
            points_forts = f"Utilisation précise de {len(terms_found)} terme(s) technique(s). Structure claire avec {len(commands_used)} commande(s) appropriée(s)."
            points_amelioration = "Votre niveau est exceptionnel. Continuez à maintenir cette expertise et explorez des cas d'usage avancés."
            conseils_techniques = f"Pour aller plus loin: approfondissez {', '.join([t for t in technical_terms if t not in terms_found][:2]) or 'les concepts avancés'}"
            encouragement = "🌟 Performance exceptionnelle ! Vous maîtrisez parfaitement ce domaine."
            
        elif percentage >= 70:
            feedback_principal = f"👍 Très bonne compréhension ! {len(common_words)} éléments corrects avec une approche solide."
            points_forts = f"Bonne utilisation de {len(terms_found)} terme(s) technique(s). Réponse de {answer_length} caractères bien développée."
            points_amelioration = "Quelques détails à peaufiner pour atteindre l'excellence. Précisez davantage certains aspects techniques."
            conseils_techniques = f"Renforcez: {', '.join([t for t in technical_terms if t not in terms_found][:3]) or 'la précision technique'}"
            encouragement = "🎯 Excellent travail ! Vous êtes très proche de la maîtrise totale."
            
        elif percentage >= 50:
            feedback_principal = f"📚 Compréhension correcte avec {len(common_words)} points valides. Quelques améliorations nécessaires."
            points_forts = f"Base solide avec {len(terms_found)} terme(s) technique(s) approprié(s). Effort visible dans votre réponse."
            points_amelioration = "Développez davantage votre réponse et intégrez plus de précision technique."
            conseils_techniques = f"Focalisez-vous sur: {', '.join(technical_terms[:3])}"
            encouragement = "💪 Bon départ ! Continuez à approfondir ces concepts."
            
        elif percentage >= 25:
            feedback_principal = f"⚡ Compréhension partielle détectée. {len(common_words)} élément(s) correct(s) identifié(s)."
            points_forts = f"Vous avez fourni une réponse de {answer_length} caractères, montrant votre engagement."
            points_amelioration = "Revoyez les concepts fondamentaux et enrichissez votre vocabulaire technique."
            conseils_techniques = f"Priorité: maîtriser {', '.join(technical_terms[:2])}"
            encouragement = "🌱 Vous progressez ! Chaque effort vous rapproche de la maîtrise."
            
        else:
            feedback_principal = f"🔄 Il faut reprendre les bases. Analysons ensemble votre approche."
            points_forts = f"Votre participation avec {answer_length} caractères montre votre volonté d'apprendre."
            points_amelioration = "Commencez par réviser les concepts de base avant d'aborder les détails."
            conseils_techniques = f"Étudiez d'abord: {', '.join(technical_terms[:2])}"
            encouragement = "🚀 Ne vous découragez pas ! Chaque expert a commencé par apprendre les bases."
        
        return {
            "feedback_principal": feedback_principal,
            "points_forts": points_forts,
            "points_amelioration": points_amelioration,
            "conseils_techniques": conseils_techniques,
            "encouragement": encouragement
        }
    
    def format_feedback_for_display(self, feedback_data: Dict[str, str]) -> str:
        """Formate le feedback pour l'affichage dans l'interface"""
        return f"""
        <div class="ai-feedback-detailed">
            <div class="feedback-section">
                <h5>🤖 Analyse IA</h5>
                <p>{feedback_data.get('feedback_principal', '')}</p>
            </div>
            
            <div class="feedback-section">
                <h5>✅ Points forts détectés</h5>
                <p>{feedback_data.get('points_forts', '')}</p>
            </div>
            
            <div class="feedback-section">
                <h5>💡 Suggestions d'amélioration</h5>
                <p>{feedback_data.get('points_amelioration', '')}</p>
            </div>
            
            <div class="feedback-section">
                <h5>🔧 Conseils techniques IA</h5>
                <p>{feedback_data.get('conseils_techniques', '')}</p>
            </div>
            
            <div class="feedback-section encouragement">
                <h5>🎯 Encouragement IA</h5>
                <p>{feedback_data.get('encouragement', '')}</p>
            </div>
        </div>
        """

# Instance globale
ai_feedback_generator = AIFeedbackGenerator()

// AI Quiz JavaScript functionality
class AIQuizManager {
    constructor() {
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.maxTotalScore = 0;
        this.selectedCategory = null;
        this.selectedTheme = null;
        this.currentSession = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthentication();
        this.loadQuestions();
    }

    async checkAuthentication() {
        if (!window.holbiesApp || !window.holbiesApp.token) {
            window.location.href = '/login';
            return;
        }
    }

    setupEventListeners() {
        // Les event listeners pour les catégories sont gérés par les attributs onclick
        const submitBtn = document.getElementById('submit-answer');
        const nextBtn = document.getElementById('next-question');
        const retakeBtn = document.getElementById('retake-pld-btn');
        const answerTextarea = document.getElementById('user-answer');

        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitAnswer());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }

        if (retakeBtn) {
            retakeBtn.addEventListener('click', () => this.retakeQuiz());
        }

        // Compteur de caractères avec feedback visuel (si élément présent)
        if (answerTextarea) {
            answerTextarea.addEventListener('input', () => {
                const count = answerTextarea.value.length;
                const charCounter = document.getElementById('char-count');
                if (charCounter) {
                    charCounter.textContent = count;
                    
                    // Feedback visuel basé sur la longueur
                    if (count < 50) {
                        charCounter.style.color = '#ff6b6b'; // Rouge - trop court
                    } else if (count < 100) {
                        charCounter.style.color = '#ffa726'; // Orange - court
                    } else if (count < 300) {
                        charCounter.style.color = '#66bb6a'; // Vert - bien
                    } else {
                        charCounter.style.color = '#42a5f5'; // Bleu - détaillé
                    }
                }
            });
        }
    }

    async loadQuestions() {
        if (!this.selectedCategory) {
            return;
        }
        
        try {
            const url = `/api/pld/questions/${this.selectedCategory}${this.selectedTheme ? '/' + this.selectedTheme : ''}`;
            const response = await window.holbiesApp.apiRequest(url, {
                method: 'GET'
            });
            
            this.questions = response.questions || response;
            
            console.log('Questions chargées:', this.questions.length);
            
        } catch (error) {
            console.error('Erreur chargement questions:', error);
            showError('Erreur lors du chargement des questions');
        }
    }

    selectCategory(category) {
        this.selectedCategory = category;
        
        // Mettre à jour l'interface
        const cards = document.querySelectorAll('.category-card');
        cards.forEach(card => {
            card.classList.remove('selected');
            if (card.getAttribute('data-category') === category) {
                card.classList.add('selected');
            }
        });
        
        // Message de chargement avec contexte
        showInfo(`Chargement des thèmes ${category.toUpperCase()}...`);
        
        // Charger et afficher les thèmes pour cette catégorie
        this.loadThemes();
    }

    async loadThemes() {
        try {
            const response = await window.holbiesApp.apiRequest(`/api/pld/categories/${this.selectedCategory}/themes`, {
                method: 'GET'
            });
            
            // Si la réponse est vide ou null, gérer comme une catégorie vide
            if (!response || !response.themes || response.themes.length === 0) {
                // Messages personnalisés selon la catégorie
                const categoryMessages = {
                    'c': 'Aucun thème C/C++ disponible pour le moment. Cette section sera bientôt enrichie !',
                    'python': 'Aucun thème Python disponible actuellement. Revenez bientôt pour découvrir de nouveaux défis !',
                    'javascript': 'Aucun thème JavaScript disponible pour l\'instant. De nouveaux contenus arrivent prochainement !',
                    'sql': 'Aucun thème SQL disponible actuellement. Cette catégorie sera complétée sous peu !',
                    'backend': 'Aucun thème Backend disponible pour le moment. Nouveaux contenus en préparation !',
                    'frontend': 'Aucun thème Frontend disponible actuellement. Restez connecté pour les nouveautés !',
                    'algorithms': 'Aucun algorithme disponible pour l\'instant. De nouveaux défis algorithmiques arrivent !',
                    'databases': 'Aucun thème de bases de données disponible actuellement. Contenu en cours d\'élaboration !'
                };
                
                const defaultMessage = `Aucun thème disponible pour la catégorie "${this.selectedCategory}". Nouveaux contenus bientôt disponibles !`;
                const message = categoryMessages[this.selectedCategory.toLowerCase()] || defaultMessage;
                
                showWarning(message);
                
                // Garder la catégorie sélectionnée et rester sur la même page
                return;
            }
            
            this.displayThemes(response.themes);
        } catch (error) {
            // Messages d'erreur contextuels
            let errorMessage = 'Impossible de charger les thèmes pour le moment.';
            let errorTitle = 'Erreur de chargement';
            
            if (error.message.includes('404')) {
                errorMessage = `La catégorie "${this.selectedCategory}" n'existe pas ou a été supprimée.`;
                errorTitle = 'Catégorie introuvable';
            } else if (error.message.includes('500')) {
                errorMessage = 'Erreur serveur temporaire. Veuillez réessayer dans quelques instants.';
                errorTitle = 'Erreur serveur';
            } else if (error.message.includes('Network')) {
                errorMessage = 'Problème de connexion réseau. Vérifiez votre connexion internet.';
                errorTitle = 'Problème de connexion';
            }
            
            showError(errorMessage);
        }
    }
    
    displayThemes(themes) {
        const startScreen = document.getElementById('pld-start');
        const themeScreen = document.getElementById('pld-themes');
        const themesGrid = document.getElementById('themes-grid');

        // Vérifier que les éléments existent
        if (!themesGrid) {
            showError('Erreur d\'interface : éléments manquants');
            return;
        }

        // Vider la grille des thèmes
        themesGrid.innerHTML = '';

        if (!Array.isArray(themes) || themes.length === 0) {
            // Ce cas ne devrait plus arriver grâce à la gestion 204
            showWarning('Aucun thème trouvé pour cette catégorie');
            return;
        }
        
        // Message de succès pour les catégories avec contenu
        showSuccess(`${themes.length} thème(s) trouvé(s) en ${this.selectedCategory.toUpperCase()}`);

        // Créer les cartes de thème
        themes.forEach((theme, index) => {
            const themeCard = document.createElement('div');
            themeCard.className = 'theme-card';
            themeCard.setAttribute('data-theme', theme.name);
            themeCard.onclick = () => this.selectTheme(theme.name);

            // Choisir une icône appropriée selon le thème
            let icon = '📝';
            if (theme.name.includes('permission')) icon = '🔐';
            else if (theme.name.includes('io')) icon = '💾';
            else if (theme.name.includes('variable')) icon = '🔢';
            else if (theme.name.includes('function')) icon = '⚙️';

            themeCard.innerHTML = `
                <div class="theme-icon">${icon}</div>
                <div class="theme-name">${theme.display_name || theme.name}</div>
                <div class="theme-description">${theme.description || 'Thème de programmation'}</div>
                <div class="theme-stats">
                    <span class="theme-question-count">${theme.question_count || 'N/A'} questions</span>
                    <span class="theme-difficulty">THÈME</span>
                </div>
            `;

            // Animation d'apparition progressive
            themeCard.style.animationDelay = `${(index + 1) * 0.1}s`;
            themesGrid.appendChild(themeCard);
        });

        // Transition vers l'écran de sélection de thème (si les éléments existent)
        if (startScreen && themeScreen) {
            startScreen.classList.add('hidden');
            themeScreen.classList.remove('hidden');
        }
    }

    selectTheme(theme) {
        console.log('selectTheme appelé avec:', theme);
        showInfo(`Préparation du quiz "${theme}"...`);
        
        this.selectedTheme = theme;
        
        // Charger les questions pour ce thème spécifique
        this.loadQuestions().then(() => {
            console.log('Questions chargées:', this.questions.length, 'questions');
            if (this.questions && this.questions.length > 0) {
                // Démarrer la session après chargement des questions
                setTimeout(() => {
                    showSuccess(`Quiz "${theme}" prêt ! ${this.questions.length} questions chargées.`);
                    console.log('Démarrage de la session...');
                    this.startSession();
                }, 1000);
            } else {
                console.log('Aucune question trouvée pour le thème');
                showError(`Aucune question trouvée pour le thème "${theme}"`);
            }
        }).catch(error => {
            console.error('Erreur lors du chargement:', error);
            showError(`Erreur lors du chargement du thème "${theme}"`);
        });
    }

    selectAllThemes() {
        this.selectedTheme = null; // null signifie toute la catégorie
        
        // Charger toutes les questions de la catégorie
        this.loadQuestions().then(() => {
            setTimeout(() => {
                this.startSession();
            }, 500);
        });
    }

    backToCategories() {
        const startScreen = document.getElementById('pld-start');
        const themeScreen = document.getElementById('pld-themes');
        
        // Réinitialiser les sélections
        this.selectedCategory = null;
        this.selectedTheme = null;
        
        // Supprimer les sélections visuelles
        document.querySelectorAll('.category-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Retourner à l'écran de démarrage (si les éléments existent)
        if (themeScreen && startScreen) {
            themeScreen.classList.add('hidden');
            startScreen.classList.remove('hidden');
        }
    }

    async startSession() {
        console.log('startSession() appelée');
        try {
            console.log('Appel API /api/pld/start...');
            this.currentSession = await window.holbiesApp.apiRequest('/api/pld/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });
            
            console.log('Session créée:', this.currentSession);
            
            // Switch to question screen
            console.log('Affichage de la première question...');
            this.showQuestion();
            
        } catch (error) {
            console.error('Erreur lors du démarrage de session:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors du démarrage de la session: ' + error.message, 'error');
            }
        }
    }

    showQuestion() {
        console.log('showQuestion() appelée, currentQuestionIndex:', this.currentQuestionIndex);
        console.log('Questions disponibles:', this.questions.length);
        
        const startScreen = document.getElementById('pld-start');
        const themeScreen = document.getElementById('pld-themes');
        const questionScreen = document.getElementById('pld-quiz');
        const resultsScreen = document.getElementById('pld-results');

        console.log('Éléments trouvés:', {
            startScreen: !!startScreen,
            themeScreen: !!themeScreen,
            questionScreen: !!questionScreen,
            resultsScreen: !!resultsScreen
        });

        // Hide other screens
        startScreen.classList.add('hidden');
        if (themeScreen) themeScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');
        questionScreen.classList.remove('hidden');

        const question = this.questions[this.currentQuestionIndex];
        console.log('Question courante:', question);
        
        // Update question content
        const questionTitle = document.getElementById('question-title');
        const questionText = document.getElementById('question-text');
        
        if (questionTitle) {
            questionTitle.textContent = `Question ${this.currentQuestionIndex + 1}`;
        }
        if (questionText) {
            questionText.textContent = question.question_text;
        }
        
        // Clear previous answer
        const userAnswer = document.getElementById('user-answer');
        if (userAnswer) {
            userAnswer.value = '';
        }
        
        // Update progress
        this.updateProgress();
        
        // Update question counter
        this.updateQuestionCounter();
        
        console.log('Question affichée avec succès');
    }

    async submitAnswer() {
        const answerTextarea = document.getElementById('user-answer');
        const userAnswer = answerTextarea.value.trim();

        if (!userAnswer) {
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Veuillez saisir une réponse avant de continuer.', 'error');
            } else {
                alert('Veuillez saisir une réponse avant de continuer.');
            }
            return;
        }

        if (!this.currentSession) {
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Aucune session active. Redémarrez le quiz.', 'error');
            } else {
                alert('Aucune session active. Redémarrez le quiz.');
            }
            return;
        }

        const submitBtn = document.getElementById('submit-answer');
        if (window.holbiesApp) {
            window.holbiesApp.showLoading(submitBtn);
        }

        try {
            const question = this.questions[this.currentQuestionIndex];
            
            const submission = {
                session_id: this.currentSession.id,
                question_id: question.question_id,
                user_answer: userAnswer
            };

            const result = await window.holbiesApp.apiRequest('/api/pld/submit-answer', {
                method: 'POST',
                body: JSON.stringify(submission)
            });

            // Store result
            this.results.push(result);
            this.totalScore += result.score;
            this.maxTotalScore += result.max_score;

            // Show feedback (for now, just continue to next question)
            this.showAnswerFeedback(result, question);

        } catch (error) {
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors de la soumission: ' + error.message, 'error');
            } else {
                alert('Erreur lors de la soumission: ' + error.message);
            }
        } finally {
            if (window.holbiesApp) {
                window.holbiesApp.hideLoading(submitBtn);
            }
        }
    }

    showAnswerFeedback(result, question) {
        // Afficher l'écran de feedback avec les détails
        const questionScreen = document.getElementById('pld-quiz');
        const feedbackScreen = document.getElementById('pld-feedback');
        
        // Cacher l'écran de question, afficher le feedback
        questionScreen.classList.add('hidden');
        feedbackScreen.classList.remove('hidden');
        
        // Remplir les informations de feedback
        const userAnswerDisplay = document.getElementById('user-answer-display');
        const questionScore = document.getElementById('question-score');
        const feedbackText = document.getElementById('feedback-text');
        const expectedAnswer = document.getElementById('expected-answer');
        
        if (userAnswerDisplay) {
            userAnswerDisplay.textContent = document.getElementById('user-answer').value;
        }
        
        if (questionScore) {
            questionScore.textContent = `${result.score}/${result.max_score}`;
        }
        
        if (feedbackText) {
            // Utiliser le feedback IA intelligent si disponible
            if (result.ai_feedback) {
                const percentage = result.percentage || 0;
                
                // Déterminer l'emoji et la classe selon le score
                let scoreEmoji = '📊';
                let scoreClass = '';
                if (percentage >= 90) {
                    scoreEmoji = '🏆';
                    scoreClass = 'high-score';
                } else if (percentage >= 75) {
                    scoreEmoji = '🎯';
                    scoreClass = 'good-score';
                } else if (percentage >= 50) {
                    scoreEmoji = '📈';
                    scoreClass = 'average-score';
                } else {
                    scoreEmoji = '💪';
                    scoreClass = 'low-score';
                }
                
                feedbackText.innerHTML = `
                    <div class="ai-feedback-intelligent">
                        <div class="score-summary ${scoreClass}">
                            <h4>${scoreEmoji} Résultat: ${result.score}/${result.max_score} points (${result.percentage}%)</h4>
                        </div>
                        
                        <div class="feedback-section">
                            <h5>🤖 Analyse IA</h5>
                            <p>${result.ai_feedback.feedback_principal || 'Analyse en cours...'}</p>
                        </div>
                        
                        <div class="feedback-section points-forts">
                            <h5>✅ Points forts</h5>
                            <p>${result.ai_feedback.points_forts || 'Effort visible dans votre réponse'}</p>
                        </div>
                        
                        <div class="feedback-section points-amelioration">
                            <h5>💡 Points d'amélioration</h5>
                            <p>${result.ai_feedback.points_amelioration || 'Continuez à étudier ce concept'}</p>
                        </div>
                        
                        <div class="feedback-section conseils">
                            <h5>🔧 Conseils techniques</h5>
                            <p>${result.ai_feedback.conseils_techniques || 'Pratiquez davantage ce type de questions'}</p>
                        </div>
                        
                        <div class="feedback-section encouragement">
                            <h5>🎯 Encouragement</h5>
                            <p>${result.ai_feedback.encouragement || 'Continuez vos efforts !'}</p>
                        </div>
                    </div>
                `;
                
                // Ajouter des animations séquentielles
                setTimeout(() => {
                    const sections = feedbackText.querySelectorAll('.feedback-section');
                    sections.forEach((section, index) => {
                        section.style.animationDelay = `${index * 0.1}s`;
                        section.classList.add('animate-in');
                    });
                }, 100);
                
                // Effet confettis pour très bonnes réponses
                if (percentage >= 85) {
                    this.showConfettiEffect();
                }
                
            } else {
                // Fallback si pas de feedback IA avec style amélioré
                feedbackText.innerHTML = `
                    <div class="ai-feedback-intelligent">
                        <div class="score-summary">
                            <h4>📊 Score obtenu: ${result.score}/${result.max_score} points (${result.percentage}%)</h4>
                        </div>
                        <div class="feedback-section">
                            <h5>📝 Feedback</h5>
                            <p>${result.feedback}</p>
                        </div>
                    </div>
                `;
            }
        }
        
        if (expectedAnswer) {
            // Maintenant on peut soit cacher la réponse attendue, soit la montrer de manière moins prominente
            expectedAnswer.innerHTML = `
                <details>
                    <summary>📖 Voir la réponse de référence</summary>
                    <div class="reference-answer">
                        ${result.expected_answer}
                    </div>
                </details>
            `;
        }
        
        // Afficher un message de performance avec plus de variété
        if (window.holbiesApp) {
            const percentage = result.percentage || 0;
            let message = '';
            let type = 'info';
            
            if (percentage >= 90) {
                message = `🏆 Performance exceptionnelle ! Score: ${result.score}/${result.max_score}`;
                type = 'success';
            } else if (percentage >= 75) {
                message = `🎯 Très bonne réponse ! Score: ${result.score}/${result.max_score}`;
                type = 'success';
            } else if (percentage >= 60) {
                message = `👍 Bonne réponse ! Score: ${result.score}/${result.max_score}`;
                type = 'success';
            } else if (percentage >= 40) {
                message = `📚 Réponse partielle. Score: ${result.score}/${result.max_score}`;
                type = 'warning';
            } else {
                message = `💪 Continuez vos efforts ! Score: ${result.score}/${result.max_score}`;
                type = 'warning';
            }
            
            window.holbiesApp.showMessage(message, type);
        }
    }

    nextQuestion() {
        // Cacher l'écran de feedback
        const feedbackScreen = document.getElementById('pld-feedback');
        if (feedbackScreen) {
            feedbackScreen.classList.add('hidden');
        }
        
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex >= this.questions.length) {
            this.showFinalResults();
        } else {
            this.showQuestion();
        }
    }

    async showFinalResults() {
        const questionScreen = document.getElementById('pld-quiz');
        const feedbackScreen = document.getElementById('pld-feedback');
        const resultsScreen = document.getElementById('pld-results');
        
        // Compléter la session sur le serveur
        if (this.currentSession) {
            try {
                await window.holbiesApp.apiRequest(`/api/pld/complete?session_id=${this.currentSession.id}`, {
                    method: 'POST'
                });
            } catch (error) {
                // Continue with displaying results even if completion fails
                console.log('Could not complete session on server:', error);
            }
        }
        
        // Hide other screens, show results
        questionScreen.classList.add('hidden');
        if (feedbackScreen) feedbackScreen.classList.add('hidden');
        resultsScreen.classList.remove('hidden');

        // Calculate final statistics
        const averageScore = this.totalScore / this.maxTotalScore * 100;
        
        // Update results display
        document.getElementById('final-score').textContent = `${this.totalScore.toFixed(1)}/${this.maxTotalScore}`;
        
        // Generate detailed results
        const resultsDetails = document.getElementById('results-summary');
        if (resultsDetails) {
            let detailsHTML = '<h3>Détail par question :</h3>';
            
            this.results.forEach((result, index) => {
                const question = this.questions[index];
                detailsHTML += `
                    <div class="result-item">
                        <h4>Question ${index + 1}</h4>
                        <p><strong>Score :</strong> ${result.score}/${result.max_score} (${result.percentage}%)</p>
                        <p><strong>Feedback :</strong> ${result.feedback}</p>
                    </div>
                `;
            });
            
            // Add performance message
            detailsHTML += `<div class="performance-message">`;
            if (averageScore >= 90) {
                detailsHTML += '<p class="text-success">🏆 Performance exceptionnelle ! Vous maîtrisez parfaitement ces concepts.</p>';
            } else if (averageScore >= 75) {
                detailsHTML += '<p class="text-success">👍 Très bonne performance ! Quelques détails à peaufiner.</p>';
            } else if (averageScore >= 60) {
                detailsHTML += '<p class="text-warning">📚 Bonne base ! Continuez à étudier pour améliorer la précision.</p>';
            } else if (averageScore >= 40) {
                detailsHTML += '<p class="text-warning">💪 Effort appréciable ! Travaillez davantage les termes techniques.</p>';
            } else {
                detailsHTML += '<p class="text-danger">📖 Il est temps de revoir les concepts fondamentaux !</p>';
            }
            detailsHTML += '</div>';
            
            resultsDetails.innerHTML = detailsHTML;
        }
        
        // Update progress to 100%
        this.updateProgress(100);
    }

    retakeQuiz() {
        // Reset state
        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.maxTotalScore = 0;
        this.selectedCategory = null;
        this.selectedTheme = null;
        
        // Reset category selection
        const cards = document.querySelectorAll('.category-card');
        cards.forEach(card => {
            card.classList.remove('selected');
        });

        // Show start screen
        const startScreen = document.getElementById('pld-start');
        const questionScreen = document.getElementById('pld-quiz');
        const themeScreen = document.getElementById('pld-themes');
        const feedbackScreen = document.getElementById('pld-feedback');
        const resultsScreen = document.getElementById('pld-results');

        startScreen.classList.remove('hidden');
        questionScreen.classList.add('hidden');
        if (themeScreen) themeScreen.classList.add('hidden');
        if (feedbackScreen) feedbackScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');

        // Reset progress
        this.updateProgress(0);
        this.updateQuestionCounter();
    }

    updateProgress(percentage = null) {
        const progressFill = document.getElementById('progress-fill');
        
        if (progressFill) {
            if (percentage !== null) {
                progressFill.style.width = `${percentage}%`;
            } else {
                const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
                progressFill.style.width = `${progress}%`;
            }
        }
    }

    updateQuestionCounter() {
        const currentQuestionEl = document.getElementById('current-question');
        const totalQuestionsEl = document.getElementById('total-questions');

        if (currentQuestionEl && totalQuestionsEl) {
            currentQuestionEl.textContent = this.currentQuestionIndex + 1;
            totalQuestionsEl.textContent = this.questions.length;
        }
    }

    // Effet confettis pour les excellents scores
    showConfettiEffect() {
        const confettiContainer = document.createElement('div');
        confettiContainer.className = 'confetti-container';
        confettiContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10000;
        `;
        
        // Créer plusieurs confettis
        for (let i = 0; i < 30; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: absolute;
                width: 10px;
                height: 10px;
                background: ${this.getRandomColor()};
                top: -10px;
                left: ${Math.random() * 100}%;
                animation: confettiDrop ${2 + Math.random() * 3}s linear forwards;
                transform: rotate(${Math.random() * 360}deg);
            `;
            confettiContainer.appendChild(confetti);
        }
        
        document.body.appendChild(confettiContainer);
        
        // Nettoyer après l'animation
        setTimeout(() => {
            document.body.removeChild(confettiContainer);
        }, 5000);
    }
    
    getRandomColor() {
        const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
}

// Fonction globale pour la sélection de catégorie (accessible depuis onclick)
function selectCategory(category) {
    if (window.aiQuizManager && typeof window.aiQuizManager.selectCategory === 'function') {
        window.aiQuizManager.selectCategory(category);
    } else {
        setTimeout(() => selectCategory(category), 100);
    }
}

// Fonction globale pour la sélection de thème
function selectTheme(theme) {
    if (window.aiQuizManager && typeof window.aiQuizManager.selectTheme === 'function') {
        window.aiQuizManager.selectTheme(theme);
    } else {
        setTimeout(() => selectTheme(theme), 100);
    }
}

// Fonction globale pour sélectionner toute la catégorie
function selectAllThemes() {
    if (window.aiQuizManager && typeof window.aiQuizManager.selectAllThemes === 'function') {
        window.aiQuizManager.selectAllThemes();
    }
}

// Fonction globale pour retourner aux catégories
function backToCategories() {
    if (window.aiQuizManager && typeof window.aiQuizManager.backToCategories === 'function') {
        window.aiQuizManager.backToCategories();
    }
}

// Initialisation propre et robuste
document.addEventListener('DOMContentLoaded', function() {
    
    // Configurer les event listeners pour remplacer les onclick inline
    setupEventListeners();
    
    // S'assurer que holbiesApp existe avant d'initialiser AIQuizManager
    function initializeAIQuizManager() {
        try {
            if (typeof AIQuizManager !== 'function') {
                return false;
            }
            
            window.aiQuizManager = new AIQuizManager();
            
            return true;
        } catch (error) {
            return false;
        }
    }
    
    // Essayer d'initialiser immédiatement
    if (!initializeAIQuizManager()) {
        // Si ça échoue, attendre un peu et réessayer
        setTimeout(() => {
            initializeAIQuizManager();
        }, 500);
    }
});

// Configuration des event listeners pour remplacer les onclick inline
function setupEventListeners() {
    
    // Event listeners pour les catégories dans la sidebar
    document.querySelectorAll('.category-menu-item').forEach(item => {
        item.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            if (category) {
                selectCategory(category);
            }
        });
    });
    
    // Event listeners pour les catégories dans les sections cachées
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            if (category) {
                selectCategory(category);
            }
        });
    });
    
    // Event listeners pour les éléments de catégories basiques
    document.querySelectorAll('.basic-category-item').forEach(item => {
        item.addEventListener('click', function() {
            const categoryText = this.querySelector('span').textContent.toLowerCase();
            if (categoryText) {
                selectCategory(categoryText);
            }
        });
    });
    
    // Event listener pour le bouton retour
    const backButton = document.querySelector('.back-button');
    if (backButton) {
        backButton.addEventListener('click', backToCategories);
    }
    
    // Event listeners pour les boutons d'actions des résultats
    document.querySelectorAll('[data-action="restart"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (window.aiQuizManager && typeof window.aiQuizManager.retakeQuiz === 'function') {
                window.aiQuizManager.retakeQuiz();
            }
        });
    });
    
    document.querySelectorAll('[data-action="home"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (window.aiQuizManager && typeof window.aiQuizManager.goToStart === 'function') {
                window.aiQuizManager.goToStart();
            } else {
                // Fallback simple
                const startSection = document.getElementById('pld-start');
                const resultsSection = document.getElementById('pld-results');
                if (startSection && resultsSection) {
                    resultsSection.classList.add('hidden');
                    startSection.classList.remove('hidden');
                }
            }
        });
    });
}

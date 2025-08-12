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
        const submitBtn = document.getElementById('submit-ai-answer-btn');
        const nextBtn = document.getElementById('next-ai-question-btn');
        const retakeBtn = document.getElementById('retake-pld-btn');

        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitAnswer());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }

        if (retakeBtn) {
            retakeBtn.addEventListener('click', () => this.retakeQuiz());
        }
    }

    async loadQuestions() {
        if (!this.selectedCategory) {
            console.log('Aucune catégorie sélectionnée, attente de la sélection...');
            return;
        }
        
        try {
            let url = `/api/pld/ai-questions?category=${this.selectedCategory}`;
            if (this.selectedTheme) {
                url += `&theme=${this.selectedTheme}`;
            }
            
            this.questions = await window.holbiesApp.apiRequest(url);
            console.log(`Questions ${this.selectedCategory}${this.selectedTheme ? '/' + this.selectedTheme : ''} chargées:`, this.questions.length);
        } catch (error) {
            console.error('Error loading AI questions:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors du chargement des questions: ' + error.message, 'error');
            }
        }
    }

    selectCategory(category) {
        this.selectedCategory = category;
        console.log('Catégorie sélectionnée:', category);
        
        // Mettre à jour l'interface
        const cards = document.querySelectorAll('.category-card');
        cards.forEach(card => {
            card.classList.remove('selected');
            if (card.getAttribute('data-category') === category) {
                card.classList.add('selected');
            }
        });
        
        // Charger et afficher les thèmes pour cette catégorie
        this.loadThemes();
    }

    async loadThemes() {
        try {
            const data = await window.holbiesApp.apiRequest(`/api/pld/categories/${this.selectedCategory}/themes`);
            this.displayThemes(data.themes);
        } catch (error) {
            console.error('Erreur:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors du chargement des thèmes: ' + error.message, 'error');
            }
        }
    }

    displayThemes(themes) {
        const startScreen = document.getElementById('pld-start');
        const themeScreen = document.getElementById('pld-theme-selection');
        const categoryDisplay = document.getElementById('selected-category-display');
        const themesGrid = document.getElementById('themes-grid');

        // Mettre à jour l'affichage de la catégorie sélectionnée
        categoryDisplay.textContent = this.selectedCategory.charAt(0).toUpperCase() + this.selectedCategory.slice(1);

        // Vider la grille des thèmes
        themesGrid.innerHTML = '';

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
                <div class="theme-name">${theme.display_name}</div>
                <div class="theme-description">${theme.description}</div>
                <div class="theme-stats">
                    <span class="theme-question-count">${theme.question_count} questions</span>
                    <span class="theme-difficulty">THÈME</span>
                </div>
            `;

            // Animation d'apparition progressive
            themeCard.style.animationDelay = `${(index + 1) * 0.1}s`;
            themesGrid.appendChild(themeCard);
        });

        // Transition vers l'écran de sélection de thème
        startScreen.classList.add('hidden');
        themeScreen.classList.remove('hidden');
    }

    selectTheme(theme) {
        this.selectedTheme = theme;
        console.log('Thème sélectionné:', theme);
        
        // Mettre à jour l'interface
        const cards = document.querySelectorAll('.theme-card');
        cards.forEach(card => {
            card.classList.remove('selected');
            if (card.getAttribute('data-theme') === theme) {
                card.classList.add('selected');
            }
        });
        
        // Charger les questions de ce thème
        this.loadQuestions().then(() => {
            // Démarrer automatiquement la session après chargement
            setTimeout(() => {
                this.startSession();
            }, 500);
        });
    }

    selectAllThemes() {
        this.selectedTheme = null; // null signifie toute la catégorie
        console.log('Toute la catégorie sélectionnée:', this.selectedCategory);
        
        // Charger toutes les questions de la catégorie
        this.loadQuestions().then(() => {
            setTimeout(() => {
                this.startSession();
            }, 500);
        });
    }

    backToCategories() {
        const startScreen = document.getElementById('pld-start');
        const themeScreen = document.getElementById('pld-theme-selection');
        
        // Réinitialiser les sélections
        this.selectedCategory = null;
        this.selectedTheme = null;
        
        // Supprimer les sélections visuelles
        document.querySelectorAll('.category-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Retourner à l'écran de démarrage
        themeScreen.classList.add('hidden');
        startScreen.classList.remove('hidden');
    }

    async startSession() {
        try {
            const startScreen = document.getElementById('pld-start');
            
            this.currentSession = await window.holbiesApp.apiRequest('/api/pld/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ quiz_type: 'ai' })
            });
            
            console.log('AI Quiz session started:', this.currentSession);
            
            // Switch to question screen
            this.showQuestion();
            
        } catch (error) {
            console.error('Error starting AI quiz session:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors du démarrage de la session: ' + error.message, 'error');
            }
        }
    }

    showQuestion() {
        const startScreen = document.getElementById('pld-start');
        const questionScreen = document.getElementById('pld-question');
        const resultsScreen = document.getElementById('pld-results');

        // Hide other screens
        startScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');
        questionScreen.classList.remove('hidden');

        const question = this.questions[this.currentQuestionIndex];
        
        // Update question content
        document.getElementById('ai-question-text').textContent = question.question_text;
        document.getElementById('ai-question-difficulty').textContent = question.difficulty.toUpperCase();
        document.getElementById('ai-question-score').textContent = question.max_score;
        
        // Display technical terms hint
        const termsHint = document.getElementById('technical-terms-hint');
        termsHint.textContent = `Termes techniques à utiliser : ${question.technical_terms.join(', ')}`;
        
        // Clear previous answer
        document.getElementById('ai-user-answer').value = '';
        
        // Update progress
        this.updateProgress();
        
        // Update question counter
        this.updateQuestionCounter();
    }

    async submitAnswer() {
        const answerTextarea = document.getElementById('ai-user-answer');
        const userAnswer = answerTextarea.value.trim();

        if (!userAnswer) {
            window.holbiesApp.showMessage('Veuillez saisir une réponse avant de continuer.', 'error');
            return;
        }

        if (!this.currentSession) {
            window.holbiesApp.showMessage('Aucune session active. Redémarrez le quiz.', 'error');
            return;
        }

        const submitBtn = document.getElementById('submit-ai-answer-btn');
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

            console.log('Submitting AI answer:', submission);

            const result = await window.holbiesApp.apiRequest('/api/pld/submit-answer', {
                method: 'POST',
                body: JSON.stringify(submission)
            });

            console.log('AI Correction result:', result);

            // Store result
            this.results.push(result);
            this.totalScore += result.score;
            this.maxTotalScore += result.max_score;

            // Show feedback
            this.showAnswerFeedback(result, question);

        } catch (error) {
            console.error('Error submitting AI answer:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors de la soumission: ' + error.message, 'error');
            }
        } finally {
            if (window.holbiesApp) {
                window.holbiesApp.hideLoading(submitBtn);
            }
        }
    }

    showAnswerFeedback(result, question) {
        const modal = document.getElementById('ai-answer-modal');
        const modalTitle = document.getElementById('ai-modal-title');
        const answerFeedback = document.getElementById('ai-answer-feedback');
        const nextBtn = document.getElementById('next-ai-question-btn');

        // Set title based on score
        const percentage = result.percentage;
        if (percentage >= 90) {
            modalTitle.innerHTML = '🏆 Excellente réponse !';
        } else if (percentage >= 75) {
            modalTitle.innerHTML = '👍 Très bonne réponse !';
        } else if (percentage >= 60) {
            modalTitle.innerHTML = '📚 Bonne réponse';
        } else if (percentage >= 40) {
            modalTitle.innerHTML = '💪 Réponse partiellement correcte';
        } else {
            modalTitle.innerHTML = '📖 Réponse à améliorer';
        }

        // Set feedback content
        answerFeedback.innerHTML = `
            <div class="ai-feedback-score">
                <h3>Score : ${result.score}/${result.max_score} points (${result.percentage}%)</h3>
            </div>
            
            <div class="ai-feedback-similarity">
                <strong>Similarité avec la réponse attendue :</strong> ${result.similarity}%
            </div>
            
            ${result.technical_terms_found.length > 0 ? `
                <div class="ai-feedback-technical">
                    <strong>✅ Termes techniques utilisés :</strong> ${result.technical_terms_found.join(', ')}
                    <br><strong>Bonus technique :</strong> +${result.technical_bonus} points
                </div>
            ` : ''}
            
            <div class="ai-feedback-message">
                <strong>Feedback :</strong> ${result.feedback}
            </div>
            
            <div class="ai-feedback-expected">
                <strong>Réponse attendue :</strong>
                <p>${question.expected_answer}</p>
            </div>
            
            <div class="ai-feedback-explanation">
                <strong>Explication détaillée :</strong>
                <p>${result.detailed_explanation}</p>
            </div>
            
            <div class="ai-feedback-terms">
                <strong>Termes techniques importants :</strong>
                <p>${question.technical_terms.join(', ')}</p>
            </div>
        `;

        // Update next button text
        if (this.currentQuestionIndex >= this.questions.length - 1) {
            nextBtn.textContent = 'Voir les Résultats Finaux';
        } else {
            nextBtn.textContent = 'Question Suivante';
        }

        // Show modal
        modal.classList.remove('hidden');
    }

    closeModal() {
        const modal = document.getElementById('ai-answer-modal');
        modal.classList.add('hidden');
    }

    nextQuestion() {
        this.closeModal();
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex >= this.questions.length) {
            this.showFinalResults();
        } else {
            this.showQuestion();
        }
    }

    async showFinalResults() {
        const questionScreen = document.getElementById('pld-question');
        const resultsScreen = document.getElementById('pld-results');
        
        // Compléter la session sur le serveur
        if (this.currentSession) {
            try {
                await window.holbiesApp.apiRequest(`/api/pld/complete?session_id=${this.currentSession.id}`, {
                    method: 'POST'
                });
                console.log('AI Quiz session completed successfully');
            } catch (error) {
                console.error('Error completing AI quiz session:', error);
                // Continue with displaying results even if completion fails
            }
        }
        
        // Hide question screen, show results
        questionScreen.classList.add('hidden');
        resultsScreen.classList.remove('hidden');

        // Calculate final statistics
        const averageScore = this.totalScore / this.maxTotalScore * 100;
        
        // Update results display
        document.getElementById('ai-final-score').textContent = `${this.totalScore.toFixed(1)}/${this.maxTotalScore}`;
        document.getElementById('ai-final-percentage').textContent = `${averageScore.toFixed(1)}%`;
        
        // Generate detailed results
        const resultsDetails = document.getElementById('ai-results-details');
        let detailsHTML = '<h3>Détail par question :</h3>';
        
        this.results.forEach((result, index) => {
            const question = this.questions[index];
            detailsHTML += `
                <div class="ai-result-item">
                    <h4>Question ${index + 1} : ${question.difficulty}</h4>
                    <p><strong>Score :</strong> ${result.score}/${result.max_score} (${result.percentage}%)</p>
                    <p><strong>Similarité :</strong> ${result.similarity}%</p>
                    ${result.technical_terms_found.length > 0 ? 
                        `<p><strong>Termes techniques :</strong> ${result.technical_terms_found.join(', ')}</p>` : ''}
                </div>
            `;
        });
        
        // Add performance message
        detailsHTML += `<div class="ai-performance-message">`;
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
        
        // Update progress to 100%
        this.updateProgress(100);
    }

    retakeQuiz() {
        // Reset state
        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.selectedCategory = null;
        
        // Reset category selection
        const cards = document.querySelectorAll('.category-card');
        cards.forEach(card => {
            card.classList.remove('selected');
        });

        // Show start screen
        const startScreen = document.getElementById('pld-start');
        const questionScreen = document.getElementById('pld-question');
        const resultsScreen = document.getElementById('pld-results');

        startScreen.classList.remove('hidden');
        questionScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');

        // Reset progress
        this.updateProgress(0);
        this.updateQuestionCounter();
    }

    updateProgress(percentage = null) {
        const progressFill = document.getElementById('ai-progress-fill');
        
        if (percentage !== null) {
            progressFill.style.width = `${percentage}%`;
        } else {
            const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
            progressFill.style.width = `${progress}%`;
        }
    }

    updateQuestionCounter() {
        const currentQuestionEl = document.getElementById('ai-current-question');
        const totalQuestionsEl = document.getElementById('ai-total-questions');

        if (currentQuestionEl && totalQuestionsEl) {
            currentQuestionEl.textContent = this.currentQuestionIndex + 1;
            totalQuestionsEl.textContent = this.questions.length;
        }
    }
}

// Fonction globale pour la sélection de catégorie (accessible depuis onclick)
function selectCategory(category) {
    if (window.aiQuizManager) {
        window.aiQuizManager.selectCategory(category);
    }
}

// Fonction globale pour la sélection de thème
function selectTheme(theme) {
    if (window.aiQuizManager) {
        window.aiQuizManager.selectTheme(theme);
    }
}

// Fonction globale pour sélectionner toute la catégorie
function selectAllThemes() {
    if (window.aiQuizManager) {
        window.aiQuizManager.selectAllThemes();
    }
}

// Fonction globale pour retourner aux catégories
function backToCategories() {
    if (window.aiQuizManager) {
        window.aiQuizManager.backToCategories();
    }
}

// Initialize AI quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiQuizManager = new AIQuizManager();
});

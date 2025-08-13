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
        const answerTextarea = document.getElementById('ai-user-answer');
        const charCounter = document.getElementById('char-count');

        if (submitBtn) {
            submitBtn.addEventListener('click', () => this.submitAnswer());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }

        if (retakeBtn) {
            retakeBtn.addEventListener('click', () => this.retakeQuiz());
        }

        // Compteur de caractères avec feedback visuel
        if (answerTextarea && charCounter) {
            answerTextarea.addEventListener('input', () => {
                const count = answerTextarea.value.length;
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
            });
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
            const response = await fetch(`/api/pld/categories/${this.selectedCategory}/themes`, {
                method: 'GET',
                credentials: 'same-origin'
            });
            
            // Gérer spécifiquement le cas de catégorie vide (204 No Content)
            if (response.status === 204) {
                
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
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.displayThemes(data.themes);
        } catch (error) {
            console.error('❌ Erreur lors du chargement des thèmes:', error);
            
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
            console.error('❌ Élément themes-grid introuvable');
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
        } else {
            console.log('⚠️ Éléments d\'interface non trouvés pour la transition');
        }
    }

    selectTheme(theme) {
        showInfo(`Préparation du quiz "${theme}"...`);
        
        this.selectedTheme = theme;
        
        // Logique pour commencer le quiz
        // (à implémenter selon vos besoins)
        
        setTimeout(() => {
            showSuccess(`Quiz "${theme}" prêt ! Bonne chance !`);
        }, 1500);
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
        } else {
            console.log('⚠️ Éléments pour retour aux catégories non trouvés');
        }
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

        // Set title based on score with emoji
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

        // Create structured feedback with better visual organization
        answerFeedback.innerHTML = `
            <!-- Section des scores principale -->
            <div class="feedback-score-section">
                <div class="score-item">
                    <span class="score-value">${Math.round(result.score)}</span>
                    <span class="score-label">Points obtenus</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${Math.round(result.percentage)}%</span>
                    <span class="score-label">Performance</span>
                </div>
                <div class="score-item">
                    <span class="score-value">${Math.round(result.similarity)}</span>
                    <span class="score-label">Similarité</span>
                </div>
                <div class="score-item">
                    <span class="score-value">+${result.technical_bonus || 0}</span>
                    <span class="score-label">Bonus Tech.</span>
                </div>
            </div>
            
            <!-- Section feedback principal -->
            <div class="feedback-details-section">
                <h4>🤖 Analyse IA</h4>
                <p style="color: var(--text-secondary); line-height: 1.6;">${result.feedback}</p>
            </div>
            
            ${result.technical_terms_found && result.technical_terms_found.length > 0 ? `
                <div class="feedback-details-section">
                    <h4>✅ Termes techniques détectés</h4>
                    <div class="technical-terms-found">
                        ${result.technical_terms_found.map(term => 
                            `<span class="technical-term">${term}</span>`
                        ).join('')}
                    </div>
                </div>
            ` : ''}
            
            <div class="feedback-details-section">
                <h4>📖 Réponse attendue</h4>
                <p style="color: var(--text-secondary); line-height: 1.6; background: rgba(0,0,0,0.3); padding: var(--spacing-md); border-radius: var(--border-radius); border-left: 3px solid var(--primary-color);">
                    ${question.expected_answer}
                </p>
            </div>
            
            ${result.detailed_explanation ? `
                <div class="feedback-details-section">
                    <h4>🔍 Explication détaillée</h4>
                    <p style="color: var(--text-secondary); line-height: 1.6;">
                        ${result.detailed_explanation}
                    </p>
                </div>
            ` : ''}
            
            <div class="feedback-details-section">
                <h4>🎯 Termes clés à retenir</h4>
                <div class="technical-terms-found">
                    ${question.technical_terms.map(term => 
                        `<span class="technical-term" style="opacity: ${result.technical_terms_found.includes(term) ? '1' : '0.5'}">${term}</span>`
                    ).join('')}
                </div>
                <p style="font-size: 0.9rem; color: var(--text-secondary); margin-top: var(--spacing-sm);">
                    <i>Les termes en surbrillance ont été détectés dans votre réponse</i>
                </p>
            </div>
        `;

        // Update next button text
        if (this.currentQuestionIndex >= this.questions.length - 1) {
            nextBtn.innerHTML = '<span>🎯 Voir les Résultats Finaux</span>';
        } else {
            nextBtn.innerHTML = '<span>➡️ Question Suivante</span>';
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
    console.log(`🎯 Tentative sélection catégorie: ${category}`);
    
    if (window.aiQuizManager && typeof window.aiQuizManager.selectCategory === 'function') {
        window.aiQuizManager.selectCategory(category);
    } else {
        console.log('⏳ AIQuizManager pas encore prêt, attente...');
        setTimeout(() => selectCategory(category), 100);
    }
}

// Fonction globale pour la sélection de thème
function selectTheme(theme) {
    if (window.aiQuizManager && typeof window.aiQuizManager.selectTheme === 'function') {
        window.aiQuizManager.selectTheme(theme);
    } else {
        console.log('⏳ AIQuizManager pas encore prêt pour sélection thème...');
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
    console.log('🚀 DOM Content Loaded - Initialisation PLD...');
    
    // Configurer les event listeners pour remplacer les onclick inline
    setupEventListeners();
    
    // S'assurer que holbiesApp existe avant d'initialiser AIQuizManager
    function initializeAIQuizManager() {
        try {
            if (typeof AIQuizManager !== 'function') {
                console.error('❌ Classe AIQuizManager non trouvée');
                return false;
            }
            
            window.aiQuizManager = new AIQuizManager();
            console.log('✅ AIQuizManager initialisé avec succès');
            
            return true;
        } catch (error) {
            console.error('❌ Erreur lors de l\'initialisation d\'AIQuizManager:', error);
            return false;
        }
    }
    
    // Essayer d'initialiser immédiatement
    if (!initializeAIQuizManager()) {
        // Si ça échoue, attendre un peu et réessayer
        console.log('🔄 Retry d\'initialisation dans 500ms...');
        setTimeout(() => {
            initializeAIQuizManager();
        }, 500);
    }
});

// Configuration des event listeners pour remplacer les onclick inline
function setupEventListeners() {
    console.log('⚙️ Configuration des event listeners...');
    
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
    
    console.log('✅ Event listeners configurés');
}

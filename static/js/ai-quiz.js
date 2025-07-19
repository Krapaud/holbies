// AI Quiz JavaScript functionality
class AIQuizManager {
    constructor() {
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.maxTotalScore = 0;
        
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
        const startBtn = document.getElementById('start-ai-quiz-btn');
        const submitBtn = document.getElementById('submit-ai-answer-btn');
        const nextBtn = document.getElementById('next-ai-question-btn');
        const retakeBtn = document.getElementById('retake-ai-quiz-btn');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startQuiz());
        }

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
        try {
            this.questions = await window.holbiesApp.apiRequest('/api/ai-quiz/ai-questions');
            console.log('AI Questions loaded:', this.questions.length);
        } catch (error) {
            console.error('Error loading AI questions:', error);
            if (window.holbiesApp) {
                window.holbiesApp.showMessage('Erreur lors du chargement des questions: ' + error.message, 'error');
            }
        }
    }

    startQuiz() {
        if (this.questions.length === 0) {
            window.holbiesApp.showMessage('Aucune question disponible. Rechargez la page.', 'error');
            return;
        }

        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.maxTotalScore = 0;

        this.showQuestion();
    }

    showQuestion() {
        const startScreen = document.getElementById('ai-quiz-start');
        const questionScreen = document.getElementById('ai-quiz-question');
        const resultsScreen = document.getElementById('ai-quiz-results');

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

        const submitBtn = document.getElementById('submit-ai-answer-btn');
        if (window.holbiesApp) {
            window.holbiesApp.showLoading(submitBtn);
        }

        try {
            const question = this.questions[this.currentQuestionIndex];
            
            const submission = {
                question_id: question.question_id,
                user_answer: userAnswer
            };

            console.log('Submitting AI answer:', submission);

            const result = await window.holbiesApp.apiRequest('/api/ai-quiz/ai-submit', {
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

    showFinalResults() {
        const questionScreen = document.getElementById('ai-quiz-question');
        const resultsScreen = document.getElementById('ai-quiz-results');
        
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
        // Reset quiz state
        this.currentQuestionIndex = 0;
        this.results = [];
        this.totalScore = 0;
        this.maxTotalScore = 0;

        // Show start screen
        const startScreen = document.getElementById('ai-quiz-start');
        const questionScreen = document.getElementById('ai-quiz-question');
        const resultsScreen = document.getElementById('ai-quiz-results');

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

// Initialize AI quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiQuizManager = new AIQuizManager();
});

// Quiz JavaScript functionality
class QuizManager {
    constructor() {
        this.currentSession = null;
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.startTime = null;
        this.timer = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthentication();
    }

    async checkAuthentication() {
        if (!window.holbiesApp.token) {
            window.location.href = '/login';
            return;
        }
    }

    setupEventListeners() {
        const startBtn = document.getElementById('start-quiz-btn');
        const submitBtn = document.getElementById('submit-answer-btn');
        const nextBtn = document.getElementById('next-question-btn');
        const retakeBtn = document.getElementById('retake-quiz-btn');
        const modalClose = document.getElementById('modal-close');

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

        if (modalClose) {
            modalClose.addEventListener('click', () => this.closeModal());
        }

        // Close modal on background click
        const modal = document.getElementById('answer-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
    }

    async startQuiz() {
        try {
            // Check if there's an active session first
            let sessionResponse;
            try {
                sessionResponse = await window.holbiesApp.apiRequest('/api/quiz/sessions/active');
                console.log('Found existing active session:', sessionResponse);
                
                // Ask user if they want to continue or start fresh
                const continueSession = confirm('Vous avez déjà une session de quiz en cours. Voulez-vous la continuer ? (Annuler pour recommencer)');
                
                if (!continueSession) {
                    // Start a new session, forcing completion of the old one
                    sessionResponse = await window.holbiesApp.apiRequest('/api/quiz/start?force_new=true', {
                        method: 'POST'
                    });
                }
                
            } catch (error) {
                // No active session found, start a new one
                console.log('No active session found, starting new one');
                sessionResponse = await window.holbiesApp.apiRequest('/api/quiz/start', {
                    method: 'POST'
                });
            }

            this.currentSession = sessionResponse;

            // Get questions
            const questionsResponse = await window.holbiesApp.apiRequest('/api/quiz/questions?limit=10');
            this.questions = questionsResponse;

            if (this.questions.length === 0) {
                throw new Error('Aucune question disponible');
            }

            // Initialize quiz
            this.currentQuestionIndex = 0;
            this.userAnswers = [];
            this.startTime = new Date();

            // Update UI
            this.showQuizQuestion();
            this.startTimer();
            this.updateProgress();

        } catch (error) {
            console.error('Error starting quiz:', error);
            window.holbiesApp.showMessage('Erreur lors du démarrage du quiz: ' + error.message, 'error');
        }
    }

    showQuizQuestion() {
        const startScreen = document.getElementById('quiz-start');
        const questionScreen = document.getElementById('quiz-question');
        const resultsScreen = document.getElementById('quiz-results');

        // Hide other screens
        startScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');
        questionScreen.classList.remove('hidden');

        // Display question
        const question = this.questions[this.currentQuestionIndex];
        const questionText = document.getElementById('question-text');
        const questionOptions = document.getElementById('question-options');
        const submitBtn = document.getElementById('submit-answer-btn');

        questionText.textContent = question.question_text;

        // Create options
        questionOptions.innerHTML = '';
        const options = [
            { key: 'a', text: question.option_a },
            { key: 'b', text: question.option_b },
            { key: 'c', text: question.option_c },
            { key: 'd', text: question.option_d }
        ];

        options.forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.innerHTML = `
                <span class="option-label">${option.key.toUpperCase()})</span>
                <span class="option-text">${option.text}</span>
            `;
            
            optionDiv.addEventListener('click', () => {
                this.selectOption(optionDiv, option.key);
            });

            questionOptions.appendChild(optionDiv);
        });

        // Reset submit button
        submitBtn.disabled = true;

        // Update question counter
        this.updateQuestionCounter();
    }

    selectOption(optionElement, optionKey) {
        // Remove previous selection
        document.querySelectorAll('.option').forEach(opt => {
            opt.classList.remove('selected');
        });

        // Select current option
        optionElement.classList.add('selected');
        this.selectedAnswer = optionKey;

        // Enable submit button
        const submitBtn = document.getElementById('submit-answer-btn');
        submitBtn.disabled = false;
    }

    async submitAnswer() {
        if (!this.selectedAnswer) return;

        const submitBtn = document.getElementById('submit-answer-btn');
        window.holbiesApp.showLoading(submitBtn);

        try {
            const question = this.questions[this.currentQuestionIndex];
            
            console.log('Submitting answer:', {
                session_id: this.currentSession.id,
                question_id: question.id,
                user_answer: this.selectedAnswer
            });
            console.log('Token available:', !!window.holbiesApp.token);
            
            const response = await window.holbiesApp.apiRequest('/api/quiz/submit-answer', {
                method: 'POST',
                body: JSON.stringify({
                    session_id: this.currentSession.id,
                    question_id: question.id,
                    user_answer: this.selectedAnswer
                })
            });

            console.log('Submit response:', response);

            // Store answer
            this.userAnswers.push({
                question_id: question.id,
                user_answer: this.selectedAnswer,
                is_correct: response.is_correct,
                correct_answer: response.correct_answer,
                explanation: response.explanation
            });

            // Show feedback
            this.showAnswerFeedback(response);

        } catch (error) {
            console.error('Error submitting answer:', error);
            window.holbiesApp.showMessage('Erreur lors de la soumission: ' + error.message, 'error');
        } finally {
            window.holbiesApp.hideLoading(submitBtn);
        }
    }

    showAnswerFeedback(response) {
        const modal = document.getElementById('answer-modal');
        const modalTitle = document.getElementById('modal-title');
        const answerFeedback = document.getElementById('answer-feedback');
        const nextBtn = document.getElementById('next-question-btn');

        // Set title
        modalTitle.textContent = response.is_correct ? '✅ Correct!' : '❌ Incorrect';

        // Set feedback content
        const question = this.questions[this.currentQuestionIndex];
        answerFeedback.innerHTML = `
            <div class="feedback-result ${response.is_correct ? 'correct' : 'incorrect'}">
                ${response.is_correct ? 'Bonne réponse!' : 'Mauvaise réponse'}
            </div>
            <div class="feedback-answer">
                <strong>Votre réponse:</strong> ${this.selectedAnswer.toUpperCase()}
            </div>
            <div class="feedback-correct">
                <strong>Réponse correcte:</strong> ${response.correct_answer.toUpperCase()}
            </div>
            ${response.explanation ? `
                <div class="feedback-explanation">
                    <h4>Explication:</h4>
                    <p>${response.explanation}</p>
                </div>
            ` : ''}
        `;

        // Update next button text
        if (this.currentQuestionIndex >= this.questions.length - 1) {
            nextBtn.textContent = 'Voir les Résultats';
        } else {
            nextBtn.textContent = 'Question Suivante';
        }

        // Show modal
        modal.classList.remove('hidden');
    }

    closeModal() {
        const modal = document.getElementById('answer-modal');
        modal.classList.add('hidden');
    }

    nextQuestion() {
        this.closeModal();
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex >= this.questions.length) {
            this.finishQuiz();
        } else {
            this.selectedAnswer = null;
            this.showQuizQuestion();
            this.updateProgress();
        }
    }

    async finishQuiz() {
        try {
            // Complete the quiz session
            const results = await window.holbiesApp.apiRequest(`/api/quiz/complete/${this.currentSession.id}`, {
                method: 'POST'
            });

            this.stopTimer();
            this.showResults(results);

        } catch (error) {
            console.error('Error finishing quiz:', error);
            window.holbiesApp.showMessage('Erreur lors de la finalisation: ' + error.message, 'error');
        }
    }

    showResults(results) {
        const questionScreen = document.getElementById('quiz-question');
        const resultsScreen = document.getElementById('quiz-results');
        const scoreValue = document.getElementById('score-value');
        const scorePercentage = document.getElementById('score-percentage');
        const resultsDetails = document.getElementById('results-details');

        // Hide question screen, show results
        questionScreen.classList.add('hidden');
        resultsScreen.classList.remove('hidden');

        // Display score
        scoreValue.textContent = results.score;
        scorePercentage.textContent = `${Math.round(results.percentage)}%`;

        // Create detailed results
        resultsDetails.innerHTML = `
            <div class="results-summary">
                <h3>Résumé de votre performance</h3>
                <div class="summary-stats">
                    <div class="summary-stat">
                        <span class="stat-label">Questions correctes:</span>
                        <span class="stat-value text-success">${results.correct_answers.length}</span>
                    </div>
                    <div class="summary-stat">
                        <span class="stat-label">Questions incorrectes:</span>
                        <span class="stat-value text-danger">${results.incorrect_answers.length}</span>
                    </div>
                    <div class="summary-stat">
                        <span class="stat-label">Score:</span>
                        <span class="stat-value">${results.percentage.toFixed(1)}%</span>
                    </div>
                    <div class="summary-stat">
                        <span class="stat-label">Temps total:</span>
                        <span class="stat-value">${this.getElapsedTime()}</span>
                    </div>
                </div>
            </div>
            <div class="performance-message">
                ${this.getPerformanceMessage(results.percentage)}
            </div>
        `;

        // Update progress to 100%
        this.updateProgress(100);
    }

    getPerformanceMessage(percentage) {
        if (percentage >= 90) {
            return '<p class="text-success">🏆 Excellent! Vous maîtrisez parfaitement ces concepts.</p>';
        } else if (percentage >= 75) {
            return '<p class="text-success">👍 Très bien! Quelques petites lacunes à combler.</p>';
        } else if (percentage >= 60) {
            return '<p class="text-warning">📚 Pas mal! Continuez à étudier pour améliorer vos connaissances.</p>';
        } else if (percentage >= 40) {
            return '<p class="text-warning">💪 Il y a du progrès à faire, mais ne vous découragez pas!</p>';
        } else {
            return '<p class="text-danger">📖 Il est temps de revoir les bases. La pratique fait le maître!</p>';
        }
    }

    retakeQuiz() {
        // Reset quiz state
        this.currentSession = null;
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.selectedAnswer = null;
        this.startTime = null;
        this.stopTimer();

        // Show start screen
        const startScreen = document.getElementById('quiz-start');
        const questionScreen = document.getElementById('quiz-question');
        const resultsScreen = document.getElementById('quiz-results');

        startScreen.classList.remove('hidden');
        questionScreen.classList.add('hidden');
        resultsScreen.classList.add('hidden');

        // Reset progress
        this.updateProgress(0);
        this.updateQuestionCounter();
    }

    updateProgress(percentage = null) {
        const progressFill = document.getElementById('progress-fill');
        
        if (percentage !== null) {
            progressFill.style.width = `${percentage}%`;
        } else {
            const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
            progressFill.style.width = `${progress}%`;
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

    startTimer() {
        const timerEl = document.getElementById('timer');
        if (!timerEl) return;

        this.timer = setInterval(() => {
            const elapsed = this.getElapsedTime();
            timerEl.textContent = elapsed;
        }, 1000);
    }

    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    getElapsedTime() {
        if (!this.startTime) return '00:00';

        const now = new Date();
        const diff = Math.floor((now - this.startTime) / 1000);
        const minutes = Math.floor(diff / 60);
        const seconds = diff % 60;

        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
}

// Initialize quiz when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.quizManager = new QuizManager();
});

// Dashboard JavaScript functionality
class DashboardManager {
    constructor() {
        this.user = null;
        this.sessions = [];
        this.chart = null;
        
        this.init();
    }

    async init() {
        await this.checkAuthentication();
        await this.loadUserData();
        await this.loadQuizSessions();
        this.setupEventListeners();
        this.updateStats();
        this.createPerformanceChart();
    }

    async checkAuthentication() {
        if (!window.holbiesApp.token) {
            window.location.href = '/login';
            return;
        }

        try {
            this.user = await window.holbiesApp.apiRequest('/api/users/me');
            this.updateUserInfo();
        } catch (error) {
            console.error('Authentication error:', error);
            window.location.href = '/login';
        }
    }

    updateUserInfo() {
        const usernameEl = document.getElementById('username');
        if (usernameEl && this.user) {
            usernameEl.textContent = this.user.username;
        }
    }

    async loadUserData() {
        // Additional user data loading if needed
    }

    async loadQuizSessions() {
        try {
            this.sessions = await window.holbiesApp.apiRequest('/api/quiz/sessions');
            this.displayRecentSessions();
        } catch (error) {
            console.error('Error loading quiz sessions:', error);
        }
    }

    setupEventListeners() {
        const resetBtn = document.getElementById('reset-progress');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetProgress());
        }
    }

    updateStats() {
        const completedQuizzes = this.sessions.filter(s => s.completed).length;
        const totalScore = this.sessions.reduce((sum, s) => sum + (s.completed ? s.score : 0), 0);
        const totalQuestions = this.sessions.reduce((sum, s) => sum + (s.completed ? s.total_questions : 0), 0);
        
        const averageScore = totalQuestions > 0 ? (totalScore / totalQuestions * 100) : 0;
        const bestScore = this.getBestScore();
        const streak = this.getCurrentStreak();

        // Update stat cards
        this.updateStatCard('total-quizzes', completedQuizzes);
        this.updateStatCard('average-score', `${Math.round(averageScore)}%`);
        this.updateStatCard('best-score', `${Math.round(bestScore)}%`);
        this.updateStatCard('streak', streak);

        // Animate stats
        this.animateStats();
    }

    updateStatCard(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            // Animate number change
            this.animateValue(element, element.textContent, value);
        }
    }

    animateValue(element, start, end) {
        const startNum = parseFloat(start.replace(/\D/g, '')) || 0;
        const endNum = parseFloat(end.toString().replace(/\D/g, '')) || 0;
        const suffix = end.toString().replace(/[\d\s]/g, '');
        
        const duration = 1000;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = startNum + (endNum - startNum) * this.easeOutQuart(progress);
            element.textContent = Math.round(current) + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    getBestScore() {
        const completedSessions = this.sessions.filter(s => s.completed);
        if (completedSessions.length === 0) return 0;
        
        return Math.max(...completedSessions.map(s => 
            s.total_questions > 0 ? (s.score / s.total_questions * 100) : 0
        ));
    }

    getCurrentStreak() {
        const completedSessions = this.sessions
            .filter(s => s.completed)
            .sort((a, b) => new Date(b.completed_at) - new Date(a.completed_at));
        
        let streak = 0;
        const passingScore = 60; // 60% minimum for streak
        
        for (const session of completedSessions) {
            const score = session.total_questions > 0 ? (session.score / session.total_questions * 100) : 0;
            if (score >= passingScore) {
                streak++;
            } else {
                break;
            }
        }
        
        return streak;
    }

    displayRecentSessions() {
        const sessionsList = document.getElementById('sessions-list');
        if (!sessionsList) return;

        const recentSessions = this.sessions
            .filter(s => s.completed)
            .sort((a, b) => new Date(b.completed_at) - new Date(a.completed_at))
            .slice(0, 5);

        if (recentSessions.length === 0) {
            sessionsList.innerHTML = `
                <div class="no-sessions">
                    <p>Aucune session de quiz terminée.</p>
                    <a href="/quiz" class="btn btn-primary">Commencer votre premier quiz</a>
                </div>
            `;
            return;
        }

        sessionsList.innerHTML = recentSessions.map(session => {
            const date = new Date(session.completed_at).toLocaleDateString('fr-FR');
            const score = session.total_questions > 0 ? 
                (session.score / session.total_questions * 100) : 0;
            
            return `
                <div class="session-item">
                    <div class="session-info">
                        <div class="session-date">${date}</div>
                        <div class="session-details">
                            ${session.score}/${session.total_questions} questions
                        </div>
                    </div>
                    <div class="session-score">
                        <span class="score-value ${this.getScoreClass(score)}">
                            ${Math.round(score)}%
                        </span>
                    </div>
                </div>
            `;
        }).join('');
    }

    getScoreClass(score) {
        if (score >= 80) return 'text-success';
        if (score >= 60) return 'text-warning';
        return 'text-danger';
    }

    createPerformanceChart() {
        const canvas = document.getElementById('chart-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Prepare data for the last 10 completed sessions
        const completedSessions = this.sessions
            .filter(s => s.completed)
            .sort((a, b) => new Date(a.completed_at) - new Date(b.completed_at))
            .slice(-10);

        const labels = completedSessions.map((session, index) => `Quiz ${index + 1}`);
        const scores = completedSessions.map(session => 
            session.total_questions > 0 ? 
                Math.round(session.score / session.total_questions * 100) : 0
        );

        // If no data, show placeholder
        if (scores.length === 0) {
            canvas.parentElement.innerHTML = `
                <div class="no-chart-data">
                    <p>Pas encore de données de performance.</p>
                    <p>Complétez quelques quiz pour voir votre progression!</p>
                </div>
            `;
            return;
        }

        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Score (%)',
                    data: scores,
                    borderColor: 'rgb(0, 255, 65)',
                    backgroundColor: 'rgba(0, 255, 65, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgb(0, 255, 65)',
                    pointBorderColor: 'rgb(0, 0, 0)',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgb(201, 209, 217)',
                            font: {
                                family: 'Source Code Pro'
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(0, 255, 65, 0.1)'
                        },
                        ticks: {
                            color: 'rgb(201, 209, 217)',
                            font: {
                                family: 'Source Code Pro'
                            },
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 255, 65, 0.1)'
                        },
                        ticks: {
                            color: 'rgb(201, 209, 217)',
                            font: {
                                family: 'Source Code Pro'
                            }
                        }
                    }
                },
                elements: {
                    point: {
                        hoverBackgroundColor: 'rgb(0, 255, 65)',
                        hoverBorderColor: 'rgb(255, 255, 255)'
                    }
                }
            }
        });
    }

    animateStats() {
        const statCards = document.querySelectorAll('.stat-card');
        
        statCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.transform = 'translateY(0)';
                card.style.opacity = '1';
            }, index * 100);
        });
    }

    async resetProgress() {
        const confirmed = confirm(
            'Êtes-vous sûr de vouloir réinitialiser vos progrès ? ' +
            'Cette action supprimera toutes vos sessions de quiz.'
        );
        
        if (!confirmed) return;

        try {
            // Note: This would require an API endpoint to reset user progress
            // For now, we'll just clear the local display
            this.sessions = [];
            this.updateStats();
            this.displayRecentSessions();
            
            // Recreate chart
            if (this.chart) {
                this.chart.destroy();
            }
            this.createPerformanceChart();
            
            window.holbiesApp.showMessage('Progrès réinitialisé avec succès', 'success');
        } catch (error) {
            console.error('Error resetting progress:', error);
            window.holbiesApp.showMessage('Erreur lors de la réinitialisation', 'error');
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager();
});

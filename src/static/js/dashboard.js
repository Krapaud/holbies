// Dashboard functionality
class Dashboard {
    constructor() {
        this.token = localStorage.getItem('token');
        this.init();
    }

    init() {
        if (!this.token) {
            window.location.href = '/login';
            return;
        }

        this.loadUserInfo();
        this.loadStats();
        this.loadRecentSessions();
        this.setupEventListeners();
        this.createChart();
    }

    async loadUserInfo() {
        try {
            const response = await fetch('/api/users/me', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const user = await response.json();
                document.getElementById('username').textContent = user.username || 'User';
            }
        } catch (error) {
            console.error('Error loading user info:', error);
        }
    }

    async loadStats() {
        try {
            const response = await fetch('/api/quiz/user/stats', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const stats = await response.json();
                this.updateStatsDisplay(stats);
            } else {
                // Set default values if no stats available
                this.updateStatsDisplay({
                    total_quizzes: 0,
                    average_score: 0,
                    best_score: 0,
                    current_streak: 0
                });
            }
        } catch (error) {
            console.error('Error loading stats:', error);
            // Set default values on error
            this.updateStatsDisplay({
                total_quizzes: 0,
                average_score: 0,
                best_score: 0,
                current_streak: 0
            });
        }
    }

    updateStatsDisplay(stats) {
        document.getElementById('total-quizzes').textContent = stats.total_quizzes || 0;
        document.getElementById('average-score').textContent = `${Math.round(stats.average_score || 0)}%`;
        document.getElementById('best-score').textContent = `${Math.round(stats.best_score || 0)}%`;
        document.getElementById('streak').textContent = stats.current_streak || 0;
    }

    async loadRecentSessions() {
        try {
            const response = await fetch('/api/quiz/user/recent', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const sessions = await response.json();
                this.displayRecentSessions(sessions);
            } else {
                this.displayRecentSessions([]);
            }
        } catch (error) {
            console.error('Error loading recent sessions:', error);
            this.displayRecentSessions([]);
        }
    }

    displayRecentSessions(sessions) {
        const sessionsList = document.getElementById('sessions-list');
        
        if (sessions.length === 0) {
            sessionsList.innerHTML = '<p class="no-sessions">Aucune session récente trouvée.</p>';
            return;
        }

        sessionsList.innerHTML = sessions.map(session => `
            <div class="session-item">
                <div class="session-info">
                    <div class="session-title">${session.quiz_type || 'Quiz'}</div>
                    <div class="session-date">${new Date(session.created_at).toLocaleDateString('fr-FR')}</div>
                </div>
                <div class="session-score">${Math.round(session.score || 0)}%</div>
            </div>
        `).join('');
    }

    createChart() {
        const canvas = document.getElementById('chart-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        
        // Sample data - replace with real data from API
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
                datasets: [{
                    label: 'Score Moyen (%)',
                    data: [65, 70, 75, 82, 78, 85],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#666'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#666'
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Reset progress button
        const resetBtn = document.getElementById('reset-progress');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                if (confirm('Êtes-vous sûr de vouloir réinitialiser votre progression ?')) {
                    this.resetProgress();
                }
            });
        }
    }

    async resetProgress() {
        try {
            const response = await fetch('/api/quiz/user/reset', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                alert('Progression réinitialisée avec succès !');
                location.reload();
            } else {
                alert('Erreur lors de la réinitialisation.');
            }
        } catch (error) {
            console.error('Error resetting progress:', error);
            alert('Erreur lors de la réinitialisation.');
        }
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});
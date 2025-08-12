// Enhanced Dashboard functionality
class Dashboard {
    constructor() {
        this.token = localStorage.getItem('token');
        this.chart = null;
        this.refreshInterval = null;
        this.init();
    }

    init() {
        if (!this.token) {
            window.location.href = '/login';
            return;
        }

        this.showLoading();
        this.updateTime();
        this.loadUserInfo();
        this.loadStats();
        this.loadRecentSessions();
        this.loadProgressData();
        this.setupEventListeners();
        this.createChart();
        this.setupAutoRefresh();
        this.hideLoading();
    }

    showLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.add('show');
    }

    hideLoading() {
        setTimeout(() => {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.classList.remove('show');
        }, 1000);
    }

    updateTime() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const now = new Date();
            const options = {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            timeElement.textContent = now.toLocaleDateString('fr-FR', options);
        }

        // Update every minute
        setTimeout(() => this.updateTime(), 60000);
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
                
                // Update user level and title
                this.updateUserLevel(user);
            }
        } catch (error) {
            console.error('Error loading user info:', error);
        }
    }

    updateUserLevel(user) {
        const xp = user.xp || 0;
        const level = Math.floor(xp / 100) + 1;
        const currentLevelXp = xp % 100;
        const nextLevelXp = 100;
        
        const levelTitles = {
            1: 'Débutant',
            2: 'Apprenti',
            3: 'Développeur',
            4: 'Expert',
            5: 'Maître',
            6: 'Légende'
        };
        
        document.getElementById('user-level').textContent = level;
        document.getElementById('level-title').textContent = levelTitles[Math.min(level, 6)] || 'Légende';
        document.getElementById('current-xp').textContent = currentLevelXp;
        document.getElementById('next-level-xp').textContent = nextLevelXp;
        
        const progressBar = document.getElementById('level-progress');
        if (progressBar) {
            progressBar.style.width = `${(currentLevelXp / nextLevelXp) * 100}%`;
        }
    }

    async loadStats() {
        try {
            console.log('📊 Chargement des statistiques utilisateur...');
            
            // Charger les vraies statistiques de performance
            const response = await fetch('/api/performance/stats/performance', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const result = await response.json();
                
                if (result.success && result.data) {
                    console.log('✅ Statistiques chargées:', result.data);
                    
                    const stats = result.data;
                    
                    // Calculer les statistiques pour l'affichage dashboard
                    const dashboardStats = {
                        total_quizzes: (stats.quiz?.sessions_completed || 0) + (stats.ai_quiz?.sessions_completed || 0),
                        average_score: this.calculateCombinedAverage(stats),
                        best_score: Math.max(stats.quiz?.best_score || 0, stats.ai_quiz?.best_score || 0),
                        current_streak: stats.global?.streak_days || 0,
                        quiz_sessions: stats.quiz?.sessions_completed || 0,
                        ai_quiz_sessions: stats.ai_quiz?.sessions_completed || 0,
                        level: stats.global?.level || 1,
                        xp: stats.global?.experience_points || 0
                    };
                    
                    this.updateStatsDisplay(dashboardStats);
                    this.animateStatsCounters(dashboardStats);
                    
                    // Mettre à jour les informations utilisateur
                    this.updateUserLevelFromStats(dashboardStats);
                    
                } else {
                    console.log('📭 Aucune statistique trouvée, utilisation des valeurs par défaut');
                    this.useDefaultStats();
                }
            } else {
                console.log('⚠️ API stats non disponible, utilisation des valeurs par défaut');
                this.useDefaultStats();
            }
        } catch (error) {
            console.error('❌ Erreur lors du chargement des stats:', error);
            this.useDefaultStats();
        }
    }

    calculateCombinedAverage(stats) {
        const quizAvg = stats.quiz?.average_score || 0;
        const aiAvg = stats.ai_quiz?.average_score || 0;
        const quizSessions = stats.quiz?.sessions_completed || 0;
        const aiSessions = stats.ai_quiz?.sessions_completed || 0;
        
        if (quizSessions === 0 && aiSessions === 0) {
            return 0;
        }
        
        // Pour l'AI Quiz, normaliser sur 100 (diviser par 3 environ)
        const normalizedAiAvg = aiAvg > 100 ? aiAvg / 3 : aiAvg;
        
        // Moyenne pondérée
        const totalSessions = quizSessions + aiSessions;
        const weightedAvg = ((quizAvg * quizSessions) + (normalizedAiAvg * aiSessions)) / totalSessions;
        
        return Math.round(weightedAvg);
    }

    updateUserLevelFromStats(stats) {
        document.getElementById('user-level').textContent = stats.level;
        document.getElementById('current-xp').textContent = stats.xp % 1000;
        document.getElementById('next-level-xp').textContent = 1000;
        
        const levelTitles = {
            1: 'Débutant',
            2: 'Apprenti',
            3: 'Développeur',
            4: 'Expert',
            5: 'Maître',
            6: 'Légende'
        };
        
        document.getElementById('level-title').textContent = levelTitles[Math.min(stats.level, 6)] || 'Légende';
        
        const progressBar = document.getElementById('level-progress');
        if (progressBar) {
            const progress = (stats.xp % 1000) / 1000 * 100;
            progressBar.style.width = `${progress}%`;
        }
    }

    useDefaultStats() {
        const defaultStats = {
            total_quizzes: 0,
            average_score: 0,
            best_score: 0,
            current_streak: 0,
            level: 1,
            xp: 0
        };
        this.updateStatsDisplay(defaultStats);
        this.animateStatsCounters(defaultStats);
        this.updateUserLevelFromStats(defaultStats);
    }

    updateStatsDisplay(stats) {
        document.getElementById('total-quizzes').textContent = stats.total_quizzes || 0;
        document.getElementById('average-score').textContent = `${Math.round(stats.average_score || 0)}%`;
        document.getElementById('best-score').textContent = `${Math.round(stats.best_score || 0)}%`;
        document.getElementById('streak').textContent = stats.current_streak || 0;
        
        // Update change indicators
        this.updateChangeIndicators(stats);
    }

    updateChangeIndicators(stats) {
        // Simulate some change data - replace with real historical data
        const changes = {
            quizzes: Math.max(0, Math.floor(Math.random() * 5)),
            score: Math.floor((Math.random() - 0.5) * 10),
            streak: stats.current_streak > 0 ? 'Continue comme ça!' : 'Commencez une série!'
        };
        
        const quizzesChange = document.getElementById('quizzes-change');
        if (quizzesChange) {
            quizzesChange.textContent = changes.quizzes > 0 ? `+${changes.quizzes} cette semaine` : 'Aucun cette semaine';
            quizzesChange.className = `stat-change ${changes.quizzes > 0 ? 'positive' : 'neutral'}`;
        }
        
        const scoreChange = document.getElementById('score-change');
        if (scoreChange) {
            const prefix = changes.score > 0 ? '+' : '';
            scoreChange.textContent = `${prefix}${changes.score}% ce mois`;
            scoreChange.className = `stat-change ${changes.score > 0 ? 'positive' : changes.score < 0 ? 'negative' : 'neutral'}`;
        }
        
        const streakChange = document.getElementById('streak-change');
        if (streakChange) {
            streakChange.textContent = changes.streak;
            streakChange.className = `stat-change ${stats.current_streak > 0 ? 'positive' : 'neutral'}`;
        }
    }

    animateStatsCounters(stats) {
        const counters = [
            { element: 'total-quizzes', target: stats.total_quizzes || 0, suffix: '' },
            { element: 'average-score', target: Math.round(stats.average_score || 0), suffix: '%' },
            { element: 'best-score', target: Math.round(stats.best_score || 0), suffix: '%' },
            { element: 'streak', target: stats.current_streak || 0, suffix: '' }
        ];
        
        counters.forEach(counter => {
            this.animateCounter(counter.element, counter.target, counter.suffix);
        });
    }

    animateCounter(elementId, target, suffix = '') {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        const duration = 1500;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, 16);
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
            sessionsList.innerHTML = '<p class="no-sessions">Aucune session récente trouvée. Commencez votre premier quiz!</p>';
            return;
        }

        sessionsList.innerHTML = sessions.map((session, index) => {
            const date = new Date(session.created_at);
            const scoreClass = session.score >= 80 ? 'excellent' : session.score >= 60 ? 'good' : 'needs-improvement';
            
            return `
                <div class="session-item" style="animation-delay: ${index * 0.1}s">
                    <div class="session-info">
                        <div class="session-title">${session.quiz_type || 'Quiz'}</div>
                        <div class="session-date">${date.toLocaleDateString('fr-FR')} à ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}</div>
                    </div>
                    <div class="session-score ${scoreClass}">${Math.round(session.score || 0)}%</div>
                </div>
            `;
        }).join('');
    }

    async loadProgressData() {
        // Load achievements data (static for now)
        try {
            console.log('📊 Chargement des achievements...');
            // Set default achievements since the endpoint doesn't exist yet
            this.updateAchievements([]);
            console.log('✅ Achievements chargés (mode statique)');
        } catch (error) {
            console.error('Error loading achievements:', error);
            // Set default achievements
            this.updateAchievements([]);
        }
    }

    updateAchievements(userAchievements) {
        const achievements = [
            { id: 'first-quiz', name: 'Premier Quiz', description: 'Compléter votre premier quiz' },
            { id: 'perfect-score', name: 'Score Parfait', description: 'Obtenir 100% à un quiz' },
            { id: 'week-streak', name: 'Série 7j', description: 'Maintenir une série de 7 jours' },
            { id: 'ai-master', name: 'Maître IA', description: 'Compléter 10 quiz IA' }
        ];
        
        achievements.forEach(achievement => {
            const badge = document.getElementById(achievement.id);
            if (badge) {
                const isUnlocked = userAchievements.some(ua => ua.achievement_id === achievement.id);
                badge.className = `achievement-badge ${isUnlocked ? 'unlocked' : 'locked'}`;
                badge.title = achievement.description;
            }
        });
    }

    createChart() {
        const canvas = document.getElementById('performance-chart');
        if (!canvas) return;

        // Force canvas dimensions before Chart.js initialization
        canvas.width = 1200;
        canvas.height = 500;
        canvas.style.width = '1200px';
        canvas.style.height = '500px';

        const ctx = canvas.getContext('2d');
        
        // Show loading
        const loading = document.getElementById('chart-loading');
        if (loading) loading.classList.add('show');
        
        // Load real performance data
        this.loadPerformanceData().then(data => {
            if (loading) loading.classList.remove('show');
            
            // Create chart with real data
            this.chart = new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                    devicePixelRatio: 2,
                    layout: {
                        padding: 20
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: '📊 Performance au Fil du Temps',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            color: '#2c3e50',
                            padding: 15
                        },
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                usePointStyle: true,
                                padding: 15,
                                font: {
                                    size: 13,
                                    weight: '500'
                                },
                                color: '#333'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.9)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#e1003c',
                            borderWidth: 2,
                            cornerRadius: 10,
                            padding: 12,
                            titleFont: {
                                size: 14,
                                weight: 'bold'
                            },
                            bodyFont: {
                                size: 13,
                                weight: '500'
                            },
                            displayColors: true,
                            callbacks: {
                                title: function(context) {
                                    return 'Date: ' + context[0].label;
                                },
                                label: function(context) {
                                    const value = context.parsed.y;
                                    const datasetLabel = context.dataset.label;
                                    
                                    if (value === 0) {
                                        return datasetLabel + ': Aucune activité';
                                    }
                                    
                                    return datasetLabel + ': ' + value.toFixed(1) + ' pts';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)',
                                lineWidth: 1
                            },
                            ticks: {
                                color: '#333',
                                font: {
                                    size: 12,
                                    weight: '500'
                                },
                                padding: 8,
                                callback: function(value) {
                                    return value + ' pts';
                                }
                            },
                            title: {
                                display: true,
                                text: 'Score Moyen',
                                color: '#333',
                                font: {
                                    size: 13,
                                    weight: 'bold'
                                },
                                padding: 10
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)',
                                lineWidth: 1
                            },
                            ticks: {
                                color: '#333',
                                font: {
                                    size: 12,
                                    weight: '500'
                                },
                                padding: 8,
                                maxRotation: 0
                            },
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#333',
                                font: {
                                    size: 13,
                                    weight: 'bold'
                                },
                                padding: 10
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
            
            // Force resize after chart creation with a delay
            setTimeout(() => {
                if (this.chart && this.chart.canvas) {
                    this.chart.canvas.style.width = '1200px';
                    this.chart.canvas.style.height = '500px';
                    this.chart.canvas.width = 1200;
                    this.chart.canvas.height = 500;
                    this.chart.resize(1200, 500);
                }
            }, 200);
        }).catch(error => {
            console.error('Error loading performance data:', error);
            if (loading) loading.classList.remove('show');
            this.createEmptyChart(ctx);
        });
    }

    async loadPerformanceData() {
        try {
            console.log('🔄 Chargement des données de performance...');
            
            const response = await fetch('/api/performance/stats/timeline?days=30', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const result = await response.json();
                
                if (result.success && result.data && result.data.length > 0) {
                    console.log('✅ Données de performance chargées:', result.data.length, 'entrées');
                    return this.prepareChartData(result.data);
                } else {
                    console.log('📭 Aucune donnée de performance trouvée');
                    return this.getEmptyChartData();
                }
            } else {
                console.error('❌ Erreur API performance:', response.status);
                return this.getEmptyChartData();
            }
        } catch (error) {
            console.error('❌ Erreur lors du chargement des données:', error);
            return this.getEmptyChartData();
        }
    }

    prepareChartData(timeline) {
        console.log('📊 Préparation des données pour le graphique dashboard');
        
        // Grouper les données par date
        const dateGroups = {};
        timeline.forEach(item => {
            if (item.date) {
                const date = item.date.split('T')[0];
                if (!dateGroups[date]) {
                    dateGroups[date] = {quiz: null, ai_quiz: null};
                }
                dateGroups[date][item.type] = item;
            }
        });
        
        // Créer les datasets
        const dates = Object.keys(dateGroups).sort();
        const quizData = [];
        const aiQuizData = [];
        
        dates.forEach(date => {
            const group = dateGroups[date];
            
            const quizValue = group.quiz ? parseFloat(group.quiz.avg_score || 0) : 0;
            const aiValue = group.ai_quiz ? parseFloat(group.ai_quiz.avg_score || 0) : 0;
            
            quizData.push(quizValue);
            aiQuizData.push(aiValue);
        });
        
        console.log('📈 Données préparées pour dashboard:', {
            dates: dates.length,
            quiz_points: quizData.length,
            ai_points: aiQuizData.length
        });
        
        return {
            labels: dates.map(date => new Date(date).toLocaleDateString('fr-FR', {
                day: '2-digit',
                month: '2-digit'
            })),
            datasets: [
                {
                    label: 'Quiz Classique',
                    data: quizData,
                    borderColor: '#e1003c',
                    backgroundColor: 'rgba(225, 0, 60, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#e1003c',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 9,
                    borderWidth: 3
                },
                {
                    label: 'AI Quiz',
                    data: aiQuizData,
                    borderColor: '#ff9800',
                    backgroundColor: 'rgba(255, 152, 0, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointBackgroundColor: '#ff9800',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 3,
                    pointRadius: 6,
                    pointHoverRadius: 9,
                    borderWidth: 3
                }
            ]
        };
    }

    getEmptyChartData() {
        return {
            labels: ['Aucune donnée'],
            datasets: [{
                label: 'Aucune activité',
                data: [0],
                borderColor: '#ccc',
                backgroundColor: 'rgba(204, 204, 204, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#ccc',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        };
    }

    createEmptyChart(ctx) {
        this.chart = new Chart(ctx, {
            type: 'line',
            data: this.getEmptyChartData(),
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '📊 Commencez votre première session !',
                        font: {
                            size: 16,
                            weight: 'bold'
                        },
                        color: '#34495e',
                        padding: 20
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            lineWidth: 1
                        },
                        ticks: {
                            color: '#333',
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)',
                            lineWidth: 1
                        },
                        ticks: {
                            color: '#333',
                            font: {
                                size: 12,
                                weight: '500'
                            }
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
                this.showResetConfirmation();
            });
        }

        // Refresh dashboard button
        const refreshBtn = document.getElementById('refresh-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshDashboard();
            });
        }

        // Settings button
        const settingsBtn = document.getElementById('dashboard-settings');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => {
                this.showSettings();
            });
        }

        // Chart period selector
        const periodSelector = document.getElementById('chart-period');
        if (periodSelector) {
            periodSelector.addEventListener('change', (e) => {
                this.updateChartPeriod(e.target.value);
            });
        }

        // View all sessions
        const viewAllBtn = document.getElementById('view-all-sessions');
        if (viewAllBtn) {
            viewAllBtn.addEventListener('click', () => {
                // Navigate to full sessions page
                window.location.href = '/sessions';
            });
        }

        // Add hover effects to stat cards
        this.setupStatCardAnimations();
    }

    setupStatCardAnimations() {
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    showResetConfirmation() {
        const confirmed = confirm('⚠️ Attention!\n\nÊtes-vous sûr de vouloir réinitialiser votre progression ?\n\nCette action supprimera :\n• Tous vos scores de quiz\n• Votre historique de sessions\n• Vos statistiques\n• Vos réussites\n\nCette action est irréversible.');
        
        if (confirmed) {
            this.resetProgress();
        }
    }

    async resetProgress() {
        this.showLoading();
        
        try {
            const response = await fetch('/api/quiz/user/reset', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.showNotification('✅ Progression réinitialisée avec succès !', 'success');
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                this.showNotification('❌ Erreur lors de la réinitialisation.', 'error');
            }
        } catch (error) {
            console.error('Error resetting progress:', error);
            this.showNotification('❌ Erreur de connexion.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    refreshDashboard() {
        this.showLoading();
        
        // Refresh all data
        setTimeout(() => {
            this.loadUserInfo();
            this.loadStats();
            this.loadRecentSessions();
            this.loadProgressData();
            
            if (this.chart) {
                this.chart.destroy();
                this.createChart();
            }
            
            this.hideLoading();
            this.showNotification('🔄 Dashboard actualisé !', 'success');
        }, 1000);
    }

    showSettings() {
        alert('⚙️ Paramètres du dashboard\n\nFonctionnalité en développement...\n\nBientôt disponible :\n• Thèmes personnalisés\n• Notifications\n• Préférences d\'affichage\n• Export des données');
    }

    updateChartPeriod(period) {
        if (!this.chart) return;
        
        console.log('🔄 Mise à jour de la période du graphique:', period);
        
        // Show loading
        const loading = document.getElementById('chart-loading');
        if (loading) loading.classList.add('show');
        
        // Map period values to days
        const periodToDays = {
            'week': 7,
            'month': 30,
            'quarter': 90
        };
        
        const days = periodToDays[period] || 30;
        
        // Load new data for the selected period
        fetch(`/api/performance/stats/timeline?days=${days}`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        })
        .then(response => response.json())
        .then(result => {
            if (loading) loading.classList.remove('show');
            
            if (result.success && result.data) {
                console.log(`✅ Données chargées pour ${days} jours:`, result.data.length, 'entrées');
                
                const chartData = result.data.length > 0 ? 
                    this.prepareChartData(result.data) : 
                    this.getEmptyChartData();
                
                // Update chart
                this.chart.data.labels = chartData.labels;
                this.chart.data.datasets = chartData.datasets;
                
                // Update title
                const periodLabels = {
                    'week': '7 derniers jours',
                    'month': '30 derniers jours',
                    'quarter': '3 derniers mois'
                };
                
                this.chart.options.plugins.title.text = 
                    `📊 Performance - ${periodLabels[period]}`;
                
                this.chart.update('active');
                
                this.showNotification(`📊 Graphique mis à jour: ${result.data.length} entrées`, 'success');
            } else {
                console.log('📭 Aucune donnée pour cette période');
                
                const emptyData = this.getEmptyChartData();
                this.chart.data.labels = emptyData.labels;
                this.chart.data.datasets = emptyData.datasets;
                this.chart.options.plugins.title.text = '📊 Aucune donnée pour cette période';
                this.chart.update('active');
                
                this.showNotification('📭 Aucune donnée pour cette période', 'info');
            }
        })
        .catch(error => {
            console.error('❌ Erreur lors de la mise à jour:', error);
            if (loading) loading.classList.remove('show');
            this.showNotification('❌ Erreur lors de la mise à jour du graphique', 'error');
        });
    }

    setupAutoRefresh() {
        // Auto-refresh every 5 minutes
        this.refreshInterval = setInterval(() => {
            this.loadStats();
            this.loadRecentSessions();
        }, 5 * 60 * 1000);
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'AktivGrotesk-Medium', Arial, sans-serif;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }
        }, 3000);
    }

    // Cleanup on page unload
    destroy() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        if (this.chart) {
            this.chart.destroy();
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .notification button {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        margin: 0;
        line-height: 1;
    }
    
    .session-item {
        animation: fadeInUp 0.5s ease forwards;
        opacity: 0;
        transform: translateY(20px);
    }
    
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .session-score.excellent { color: #22c55e; }
    .session-score.good { color: #f59e0b; }
    .session-score.needs-improvement { color: #ef4444; }
`;
document.head.appendChild(style);

// Initialize dashboard when page loads
let dashboardInstance;
document.addEventListener('DOMContentLoaded', () => {
    dashboardInstance = new Dashboard();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (dashboardInstance) {
        dashboardInstance.destroy();
    }
});
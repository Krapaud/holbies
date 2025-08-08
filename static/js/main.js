// Main JavaScript file for Holbies Learning Hub
class HolbiesApp {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.user = null;
        this.init();
    }

    init() {
        this.token = localStorage.getItem('access_token');
        console.log('App initialized. Token from localStorage:', this.token);
        this.checkAuth();
        this.setupEventListeners();
        this.setupNavigation();
        this.setupMatrixBackground();
        this.setupFormValidation(); // Initialize form validation
    }

    checkAuth() {
        if (this.token) {
            this.checkAuthentication();
        }
        this.updateAuthLink();
    }

    setupEventListeners() {
        // Setup global event listeners here
        console.log('Setting up event listeners');
    }

    setupNavigation() {
        const hamburger = document.getElementById('hamburger');
        const navMenu = document.getElementById('nav-menu');
        
        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                hamburger.classList.toggle('active');
            });
        }

        // Update auth link based on login status
        this.updateAuthLink();
    }

    updateAuthLink() {
        const authLink = document.getElementById('auth-link');
        if (!authLink) return;

        if (this.token) {
            authLink.textContent = 'Déconnexion';
            authLink.href = '#';
            authLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        } else {
            authLink.textContent = 'Connexion';
            authLink.href = '/login';
        }
    }

    async checkAuthentication() {
        if (!this.token) return;

        try {
            const response = await fetch('/api/users/me', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.user = await response.json();
                this.updateUserInterface();
            } else {
                this.logout();
            }
        } catch (error) {
            console.error('Error checking authentication:', error);
            this.logout();
        }
    }

    updateUserInterface() {
        // Update user info if element exists
        const userInfo = document.getElementById('user-info');
        const username = document.getElementById('username');
        
        if (username && this.user) {
            username.textContent = this.user.username;
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        this.token = null;
        this.user = null;
        window.location.href = '/';
    }

    setupMatrixBackground() {
        // Matrix background is now handled purely through CSS
        // No dynamic JS needed for this
    }

    // Utility methods
    showMessage(message, type = 'info') {
        const messageEl = document.getElementById('auth-message');
        if (!messageEl) return;

        messageEl.textContent = message;
        messageEl.className = `auth-message ${type}`;
        messageEl.style.display = 'block';

        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }

    showLoading(button) {
        const loading = button.querySelector('.btn-loading');
        const text = button.querySelector('span');
        
        if (loading && text) {
            loading.style.display = 'inline-block';
            text.style.opacity = '0.7';
            button.disabled = true;
        }
    }

    hideLoading(button) {
        const loading = button.querySelector('.btn-loading');
        const text = button.querySelector('span');
        
        if (loading && text) {
            loading.style.display = 'none';
            text.style.opacity = '1';
            button.disabled = false;
        }
    }

    // API helper methods
    async apiRequest(url, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token && !options.skipAuth) {
            headers.Authorization = `Bearer ${this.token}`;
        }

        const finalOptions = {
            ...options,
            headers
        };

        console.log('API Request:', url, finalOptions);
        console.log('Token:', this.token);

        const response = await fetch(url, finalOptions);
        
        console.log('API Response status:', response.status, response.statusText);
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Network error' }));
            console.error('API Error:', error);
            throw new Error(error.detail || 'Request failed');
        }

        const result = await response.json();
        console.log('API Result:', result);
        return result;
    }

    // Form validation
    setupFormValidation() {
        const inputs = document.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', this.validateField);
            input.addEventListener('input', this.clearValidation);
        });

        this.addPasswordStrengthIndicator();
    }

    validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        window.holbiesApp.clearValidation(e); // Use global instance
        
        let isValid = true;
        let message = '';
        
        if (field.type === 'email') {
            const emailRegex = /^[^@]+@[^@]+\.[^@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Adresse email invalide';
            }
        } else if (field.name === 'username') {
            if (value.length < 3) {
                isValid = false;
                message = 'Le nom d\'utilisateur doit faire au moins 3 caractères';
            }
        } else if (field.type === 'password') {
            if (value.length < 6) {
                isValid = false;
                message = 'Le mot de passe doit faire au moins 6 caractères';
            }
        }
        
        if (!isValid) {
            window.holbiesApp.showFieldError(field, message); // Use global instance
        }
        
        return isValid;
    }

    clearValidation(e) {
        const field = e.target;
        const errorElement = field.parentNode.querySelector('.field-error');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        field.style.borderColor = 'var(--primary-green)';
    }

    showFieldError(field, message) {
        field.style.borderColor = 'var(--danger-red)';
        
        const errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.textContent = message;
        errorElement.style.cssText = `
            color: var(--danger-red);
            font-size: 0.8rem;
            margin-top: 0.25rem;
        `;
        
        field.parentNode.appendChild(errorElement);
    }

    addPasswordStrengthIndicator() {
        const passwordField = document.querySelector('input[name="password"]');
        if (!passwordField) return;
        
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill"></div>
            </div>
            <div class="strength-text">Force du mot de passe</div>
        `;
        
        indicator.style.cssText = `
            margin-top: 0.5rem;
        `;
        
        const strengthBar = indicator.querySelector('.strength-fill');
        const strengthText = indicator.querySelector('.strength-text');
        
        passwordField.parentNode.appendChild(indicator);
        
        passwordField.addEventListener('input', (e) => {
            const password = e.target.value;
            const strength = this.calculatePasswordStrength(password); // Use this.calculatePasswordStrength
            
            strengthBar.style.width = `${strength.percentage}%`;
            strengthBar.style.backgroundColor = strength.color;
            strengthText.textContent = strength.text;
        });
    }

    calculatePasswordStrength(password) {
        let score = 0;
        let feedback = 'Très faible';
        let color = 'var(--danger-red)';
        
        if (password.length >= 6) score += 20;
        if (password.length >= 10) score += 20;
        if (/[a-z]/.test(password)) score += 20;
        if (/[A-Z]/.test(password)) score += 20;
        if (/[0-9]/.test(password)) score += 10;
        if (/[^A-Za-z0-9]/.test(password)) score += 10;
        
        if (score >= 80) {
            feedback = 'Très fort';
            color = 'var(--success-green)';
        } else if (score >= 60) {
            feedback = 'Fort';
            color = 'var(--warning-yellow)';
        } else if (score >= 40) {
            feedback = 'Moyen';
            color = 'var(--warning-yellow)';
        } else if (score >= 20) {
            feedback = 'Faible';
            color = 'var(--danger-red)';
        }
        
        return {
            percentage: score,
            text: feedback,
            color: color
        };
    }

    // Function to show welcome video after successful login
    showWelcomeVideo(callback) {
        // Video playback is disabled. Directly call the callback if provided.
        if (callback) {
            callback();
        }
    }

    // Auth visual animation
    animateAuthVisual() {
        const codeStreams = document.querySelectorAll('.code-stream span');
        
        codeStreams.forEach((span, index) => {
            span.style.animationDelay = `${index * 0.2}s`;
            
            setInterval(() => {
                if (Math.random() < 0.1) {
                    span.style.animation = 'glitch 0.3s ease-in-out';
                    setTimeout(() => {
                        span.style.animation = `matrixStream 0.5s forwards`;
                        span.style.animationDelay = `${index * 0.2}s`;
                    }, 300);
                }
            }, 2000);
        });
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holbiesApp = new HolbiesApp();
});

// Export for use in other files
window.HolbiesApp = HolbiesApp;
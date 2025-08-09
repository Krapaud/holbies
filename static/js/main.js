// Main JavaScript file for Holbies Learning Hub
class HolbiesApp {
    constructor() {
        this.token = localStorage.getItem('token') || localStorage.getItem('access_token');
        this.user = null;
        this.init();
    }

    init() {
        this.token = localStorage.getItem('token') || localStorage.getItem('access_token');
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
        const navMenu = document.getElementById('nav-menu');
        if (!navMenu) return;

        // Update token from localStorage in case it changed
        this.token = localStorage.getItem('token') || localStorage.getItem('access_token');

        // Clear existing navigation links
        navMenu.innerHTML = '';

        if (this.token) {
            // User is authenticated - show authenticated navigation
            navMenu.innerHTML = `
                <a href="/learning" class="nav-link">Learning Hub</a>
                <a href="/tutor" class="nav-link">HLH Tutor</a>
                <a href="/dashboard" class="nav-link">Dashboard</a>
                <a href="#" class="nav-link" id="auth-link">Déconnexion</a>
            `;
            
            // Add logout functionality
            const authLink = document.getElementById('auth-link');
            if (authLink) {
                authLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.logout();
                });
            }
        } else {
            // User is not authenticated - show login/register links
            navMenu.innerHTML = `
                <a href="/login" class="nav-link">Connexion</a>
                <a href="/register" class="nav-link">Inscription</a>
            `;
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
                this.updateAuthLink(); // Force update navigation after successful auth check
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
        localStorage.removeItem('token');
        this.token = null;
        this.user = null;
        this.updateAuthLink(); // Update navigation immediately
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
        const passwordField = document.querySelector('#password'); // Cible par ID pour plus de spécificité
        const strengthContainer = document.getElementById('password-strength-container');

        if (!passwordField || !strengthContainer) {
            return; // Ne s'exécute que si les éléments sont sur la page
        }

        const strengthBar = strengthContainer.querySelector('.password-strength-bar');
        const strengthText = strengthContainer.querySelector('.password-strength-text');

        passwordField.addEventListener('input', (e) => {
            const password = e.target.value;

            if (password.length === 0) {
                strengthContainer.classList.add('is-hidden');
                return;
            }
            
            strengthContainer.classList.remove('is-hidden');
            
            const strength = this.calculatePasswordStrength(password);
            
            // Mise à jour des classes pour la couleur et le texte
            strengthBar.className = 'password-strength-bar'; // Reset classes
            strengthText.className = 'password-strength-text'; // Reset classes
            
            strengthBar.classList.add(strength.level);
            strengthText.classList.add(strength.level);

            strengthText.textContent = strength.text;
        });
    }

    calculatePasswordStrength(password) {
        let score = 0;
        if (password.length > 7) score++;    // Longueur
        if (/[A-Z]/.test(password)) score++; // Majuscule
        if (/[a-z]/.test(password)) score++; // Minuscule
        if (/[0-9]/.test(password)) score++; // Chiffre
        if (/[^A-Za-z0-9]/.test(password)) score++; // Symbole

        switch (score) {
            case 5:
            case 4:
                return { level: 'is-strong', text: 'Fort' };
            case 3:
                return { level: 'is-medium', text: 'Moyen' };
            default:
                return { level: 'is-weak', text: 'Faible' };
        }
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
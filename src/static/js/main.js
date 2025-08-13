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
        
        // Setup user menu
        this.setupUserMenu();
    }

    setupUserMenu() {
        const userMenuTrigger = document.getElementById('user-menu-trigger');
        const userDropdown = document.getElementById('user-dropdown');
        const logoutItem = document.getElementById('logout-item');

        if (userMenuTrigger && userDropdown) {
            // Remove existing event listeners to prevent duplicates
            userMenuTrigger.replaceWith(userMenuTrigger.cloneNode(true));
            const newTrigger = document.getElementById('user-menu-trigger');
            
            // Toggle dropdown on click
            newTrigger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                newTrigger.classList.toggle('active');
                userDropdown.classList.toggle('active');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (!newTrigger.contains(e.target) && !userDropdown.contains(e.target)) {
                    newTrigger.classList.remove('active');
                    userDropdown.classList.remove('active');
                }
            });

            // Prevent dropdown from closing when clicking inside
            userDropdown.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }

        // Setup logout functionality
        if (logoutItem) {
            logoutItem.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        }
    }

    updateAuthLink() {
        const navMenu = document.getElementById('nav-menu');
        const userMenuContainer = document.getElementById('user-menu-container');
        if (!navMenu || !userMenuContainer) return;

        // Update token from localStorage in case it changed
        this.token = localStorage.getItem('token') || localStorage.getItem('access_token');

        if (this.token) {
            // User is authenticated - show user menu and authenticated navigation
            navMenu.innerHTML = `
                <a href="/learning" class="nav-link">Learning Hub</a>
            `;
            
            // Show user menu
            userMenuContainer.style.display = 'flex';
            
            // Update user name (default to "Utilisateur" if user data not loaded yet)
            const userNameElement = document.getElementById('user-name');
            if (userNameElement) {
                userNameElement.textContent = this.user ? this.user.username : 'Utilisateur';
            }
            
            // Show/hide admin menu based on user role (hide by default until user data is loaded)
            const adminMenuItem = document.getElementById('admin-menu-item');
            const adminDivider = document.getElementById('admin-divider');
            if (adminMenuItem && adminDivider) {
                if (this.user && this.user.is_admin) {
                    adminMenuItem.style.display = 'flex';
                    adminDivider.style.display = 'block';
                } else {
                    adminMenuItem.style.display = 'none';
                    adminDivider.style.display = 'none';
                }
            }
            
            this.setupUserMenu();
        } else {
            // User is not authenticated - show login/register links and hide user menu
            navMenu.innerHTML = `
                <a href="/login" class="nav-link">Connexion</a>
                <a href="/register" class="nav-link">Inscription</a>
            `;
            userMenuContainer.style.display = 'none';
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
                
                // Synchroniser la session côté serveur
                await this.syncUserSession();
                
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

    async syncUserSession() {
        try {
            // Appeler une route pour synchroniser la session avec l'utilisateur JWT
            const response = await fetch('/api/sync-session', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: this.user.id,
                    username: this.user.username
                })
            });
            
            if (response.ok) {
                console.log('Session synchronized');
            }
        } catch (error) {
            console.error('Error syncing session:', error);
        }
    }

    updateUserInterface() {
        // Update user info if element exists
        const userInfo = document.getElementById('user-info');
        const username = document.getElementById('username');
        
        if (username && this.user) {
            username.textContent = this.user.username;
        }
        
        // Force mise à jour du nom utilisateur dans le menu
        const userNameElement = document.getElementById('user-name');
        if (userNameElement && this.user) {
            userNameElement.textContent = this.user.username;
        }
        
        // Update user menu with actual user data
        this.updateUserMenu();
    }

    updateUserMenu() {
        if (!this.user) return;
        
        // Update user name in menu
        const userNameElement = document.getElementById('user-name');
        if (userNameElement) {
            userNameElement.textContent = this.user.username;
        }
        
        // Show/hide admin menu based on user role
        const adminMenuItem = document.getElementById('admin-menu-item');
        const adminDivider = document.getElementById('admin-divider');
        if (adminMenuItem && adminDivider) {
            if (this.user.is_admin) {
                adminMenuItem.style.display = 'flex';
                adminDivider.style.display = 'block';
            } else {
                adminMenuItem.style.display = 'none';
                adminDivider.style.display = 'none';
            }
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('token');
        this.token = null;
        this.user = null;
        
        // Close user menu if open
        const userMenuTrigger = document.getElementById('user-menu-trigger');
        const userDropdown = document.getElementById('user-dropdown');
        if (userMenuTrigger && userDropdown) {
            userMenuTrigger.classList.remove('active');
            userDropdown.classList.remove('active');
        }
        
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
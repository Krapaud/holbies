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
        this.createMatrixRain();
        this.createAsciiArt();
    }

    createMatrixRain() {
        const matrixBg = document.querySelector('.matrix-bg');
        if (!matrixBg) return;

        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲン';
        const columns = Math.floor(window.innerWidth / 20);
        
        // Create falling characters
        for (let i = 0; i < columns; i++) {
            const column = document.createElement('div');
            column.className = 'matrix-column';
            column.style.cssText = `
                position: absolute;
                left: ${i * 20}px;
                top: -100px;
                color: rgba(0, 255, 65, 0.3);
                font-family: 'Source Code Pro', monospace;
                font-size: 14px;
                animation: matrixFall ${3 + Math.random() * 5}s linear infinite;
                animation-delay: ${Math.random() * 5}s;
            `;
            
            // Add random characters to the column
            for (let j = 0; j < 20; j++) {
                const char = document.createElement('div');
                char.textContent = chars[Math.floor(Math.random() * chars.length)];
                char.style.opacity = Math.random();
                column.appendChild(char);
            }
            
            matrixBg.appendChild(column);
        }

        // Add CSS animation if not already present
        if (!document.getElementById('matrix-animations')) {
            const style = document.createElement('style');
            style.id = 'matrix-animations';
            style.textContent = `
                @keyframes matrixFall {
                    0% { transform: translateY(-100vh); }
                    100% { transform: translateY(100vh); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    createAsciiArt() {
        // ASCII art is now handled purely through CSS ::after pseudo-element
        // No additional dynamic elements needed
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
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holbiesApp = new HolbiesApp();
});

// Export for use in other files
window.HolbiesApp = HolbiesApp;

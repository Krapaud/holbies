// Main JavaScript for Dev Learning Hub
document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash message close buttons
    initFlashMessages();
    
    // Initialize fade-in animations
    initAnimations();
    
    // Initialize keyboard shortcuts
    initKeyboardShortcuts();
    
    // Initialize user menu
    initUserMenu();
});

// Fonction pour gérer le menu utilisateur
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const trigger = document.querySelector('.user-menu-trigger');
    
    if (dropdown && trigger) {
        const isOpen = dropdown.classList.contains('show');
        
        if (isOpen) {
            closeUserMenu();
        } else {
            openUserMenu();
        }
    }
}

function openUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const trigger = document.querySelector('.user-menu-trigger');
    
    if (dropdown && trigger) {
        dropdown.classList.add('show');
        trigger.classList.add('active');
        
        // Animation d'entrée pour les éléments du menu
        const items = dropdown.querySelectorAll('.dropdown-item');
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-10px)';
            setTimeout(() => {
                item.style.transition = 'all 0.2s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 50);
        });
    }
}

function closeUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    const trigger = document.querySelector('.user-menu-trigger');
    
    if (dropdown && trigger) {
        dropdown.classList.remove('show');
        trigger.classList.remove('active');
    }
}

function initUserMenu() {
    // Fermer le menu quand on clique ailleurs
    document.addEventListener('click', function(event) {
        const userMenuContainer = document.querySelector('.user-menu-container');
        
        if (userMenuContainer && !userMenuContainer.contains(event.target)) {
            closeUserMenu();
        }
    });
    
    // Fermer avec la touche Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeUserMenu();
        }
    });
}

// Fonctions pour les éléments du menu
function showSettings() {
    alert('Paramètres - Fonctionnalité à venir !');
}

function showHelp() {
    const helpContent = `
🔧 RACCOURCIS CLAVIER :
• Ctrl+Shift+D : Dashboard
• Ctrl+Shift+A : Administration
• Ctrl+Shift+L : Déconnexion
• Ctrl+Shift+Q : Quiz
• Ctrl+P : Mon Profil
• F1 : Aide
• Échap : Fermer les menus

💡 NAVIGATION :
• Utilisez le terminal interactif dans le dashboard
• Consultez vos badges de progression
• Testez vos connaissances avec les quiz

📊 PROGRESSION :
• Complétez les quiz pour gagner de l'XP
• Débloquez des achievements
• Suivez votre progression avec les badges
    `;
    
    alert(helpContent);
}

function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.animation = 'fadeOut 0.3s ease-out forwards';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
        
        // Auto-hide success messages after 5 seconds
        if (message.classList.contains('flash-success')) {
            setTimeout(() => {
                if (message.parentNode) {
                    message.style.animation = 'fadeOut 0.3s ease-out forwards';
                    setTimeout(() => {
                        message.remove();
                    }, 300);
                }
            }, 5000);
        }
    });
}

function initAnimations() {
    // Add fade-in animation to elements
    const animatedElements = document.querySelectorAll('.fade-in-up, .slide-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(el);
    });
}

function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Global shortcuts
        if (e.ctrlKey && e.shiftKey) {
            switch(e.key) {
                case 'D':
                    e.preventDefault();
                    if (document.querySelector('a[href*="dashboard"]')) {
                        window.location.href = '/dashboard';
                    }
                    break;
                case 'A':
                    e.preventDefault();
                    if (document.querySelector('a[href*="admin"]')) {
                        window.location.href = '/admin';
                    }
                    break;
                case 'L':
                    e.preventDefault();
                    if (document.querySelector('a[href*="logout"]')) {
                        window.location.href = '/logout';
                    }
                    break;
                case 'Q':
                    e.preventDefault();
                    if (document.querySelector('a[href*="quiz"]')) {
                        window.location.href = '/quiz';
                    }
                    break;
            }
        }
        
        // Raccourcis simples avec Ctrl
        if (e.ctrlKey && !e.shiftKey) {
            switch(e.key) {
                case 'p':
                case 'P':
                    e.preventDefault();
                    if (document.querySelector('a[href*="profile"]')) {
                        window.location.href = '/profile';
                    }
                    break;
            }
        }
        
        // Aide avec F1
        if (e.key === 'F1') {
            e.preventDefault();
            showHelp();
        }
        
        // Close modals/dropdowns with Escape
        if (e.key === 'Escape') {
            closeUserMenu();
            
            const openModals = document.querySelectorAll('.modal.active');
            openModals.forEach(modal => {
                modal.classList.remove('active');
            });
            
            const openDropdowns = document.querySelectorAll('.dropdown.active');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });
}

// Utility functions for animations
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `flash-message flash-${type}`;
    notification.innerHTML = `
        <span class="flash-icon">
            ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}
        </span>
        ${message}
        <button class="flash-close">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'fadeOut 0.3s ease-out forwards';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
    
    // Add close functionality
    const closeBtn = notification.querySelector('.flash-close');
    closeBtn.addEventListener('click', function() {
        notification.style.animation = 'fadeOut 0.3s ease-out forwards';
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function validateUsername(username) {
    return username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username);
}

// Loading state helper
function setLoadingState(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = `
            <span class="btn-icon">⏳</span>
            Chargement...
        `;
    } else {
        button.disabled = false;
        // Restore original content (you'd need to store it beforehand)
    }
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showNotification('Copié dans le presse-papiers !', 'success');
    }).catch(function() {
        showNotification('Erreur lors de la copie', 'error');
    });
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format time for display
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Random number between min and max
function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Debounce function for search/input
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Console easter eggs exposure
window.konami = function() {
    if (typeof konami === 'function') {
        konami();
    }
};

window.matrix = function() {
    if (typeof matrix === 'function') {
        matrix();
    }
};

window.glitch = function() {
    if (typeof glitch === 'function') {
        glitch();
    }
};

window.hack = function() {
    if (typeof hack === 'function') {
        hack();
    }
};

// Show available console commands
console.log(`
🎮 Console Commands Available:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
konami()  - Rotation animation
matrix()  - Toggle Matrix rain
glitch()  - Glitch effect on titles
hack()    - Toggle hack mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`);

// Matrix background setup
document.addEventListener('DOMContentLoaded', function() {
    // Create matrix background if it doesn't exist
    if (!document.getElementById('matrix-bg')) {
        const matrixBg = document.createElement('div');
        matrixBg.id = 'matrix-bg';
        matrixBg.className = 'matrix-bg';
        document.body.insertBefore(matrixBg, document.body.firstChild);
    }
});

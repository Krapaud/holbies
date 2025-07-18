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
    
    // Initialize dashboard enhancements
    initDashboardEnhancements();
    
    // Initialize particles background
    initParticles();
    
    // Initialize counters animation
    initCounters();
    
    // Initialize progress bars animation
    initProgressBars();
});

// Nouvelles fonctions pour les améliorations du dashboard
function initDashboardEnhancements() {
    // Animation des cartes au scroll
    observeCards();
    
    // Effet de hover pour les cartes
    addCardHoverEffects();
    
    // Animation de typing pour les textes
    initTypingEffect();
}

function initParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    // S'assurer que le container couvre tout l'écran
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100vw';
    particlesContainer.style.height = '100vh';
    particlesContainer.style.zIndex = '-1';
    particlesContainer.style.pointerEvents = 'none';
    
    // Créer plus de particules pour couvrir tout l'écran
    const particleCount = Math.floor((window.innerWidth * window.innerHeight) / 15000);
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer);
    }
    
    // Recréer les particules quand la fenêtre change de taille
    window.addEventListener('resize', () => {
        particlesContainer.innerHTML = '';
        const newParticleCount = Math.floor((window.innerWidth * window.innerHeight) / 15000);
        for (let i = 0; i < newParticleCount; i++) {
            createParticle(particlesContainer);
        }
    });
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Position aléatoire
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    
    // Animation delay aléatoire
    particle.style.animationDelay = Math.random() * 6 + 's';
    particle.style.animationDuration = (3 + Math.random() * 6) + 's';
    
    // Taille aléatoire
    const size = 1 + Math.random() * 3;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    
    // Opacité aléatoire
    particle.style.opacity = 0.3 + Math.random() * 0.7;
    
    container.appendChild(particle);
    
    // Recréer la particule après l'animation
    setTimeout(() => {
        if (container.contains(particle)) {
            container.removeChild(particle);
            createParticle(container);
        }
    }, (3 + Math.random() * 6) * 1000);
}

function initCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.getAttribute('data-target')) || parseFloat(counter.textContent);
        const isDecimal = counter.textContent.includes('.');
        
        animateCounter(counter, target, isDecimal);
    });
}

function animateCounter(element, target, isDecimal = false) {
    const duration = 2000; // 2 secondes
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        
        if (isDecimal) {
            element.textContent = current.toFixed(1) + (element.textContent.includes('%') ? '%' : '');
        } else {
            element.textContent = Math.floor(current);
        }
    }, duration / steps);
}

function initProgressBars() {
    const progressFills = document.querySelectorAll('.progress-fill[data-width]');
    
    progressFills.forEach(fill => {
        const targetWidth = fill.getAttribute('data-width');
        
        // Démarrer l'animation après un court délai
        setTimeout(() => {
            fill.style.width = targetWidth + '%';
        }, 500);
    });
}

function observeCards() {
    const cards = document.querySelectorAll('.floating-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'cardSlideIn 0.8s ease-out forwards';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        observer.observe(card);
    });
}

function addCardHoverEffects() {
    const cards = document.querySelectorAll('.floating-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            // Ajouter un effet de pulse aux icônes
            const icons = card.querySelectorAll('.card-icon, .stat-icon');
            icons.forEach(icon => {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            });
        });
        
        card.addEventListener('mouseleave', () => {
            const icons = card.querySelectorAll('.card-icon, .stat-icon');
            icons.forEach(icon => {
                icon.style.transform = 'scale(1) rotate(0deg)';
            });
        });
    });
}

function initTypingEffect() {
    const typingElements = document.querySelectorAll('.username-highlight');
    
    typingElements.forEach(element => {
        const originalText = element.textContent;
        element.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < originalText.length) {
                element.textContent += originalText.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        setTimeout(typeWriter, 1000);
    });
}

// Ajouter les keyframes CSS dynamiquement
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes cardSlideIn {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card-icon, .stat-icon {
            transition: all 0.3s ease;
        }
        
        .progress-fill {
            transition: width 1.5s ease-in-out;
        }
    `;
    document.head.appendChild(style);
}

// Initialiser les styles dynamiques
addDynamicStyles();

// Fonction Matrix Rain pour le terminal
function matrixRain() {
    const terminal = document.getElementById('terminal');
    if (!terminal) return;
    
    // Créer ou enlever l'effet Matrix Rain
    let matrixContainer = terminal.querySelector('.matrix-rain');
    
    if (matrixContainer) {
        // Enlever l'effet
        matrixContainer.remove();
        return;
    }
    
    // Créer l'effet
    matrixContainer = document.createElement('div');
    matrixContainer.className = 'matrix-rain';
    terminal.appendChild(matrixContainer);
    
    // Caractères Matrix
    const matrixChars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    
    // Créer les colonnes de pluie
    const columns = Math.floor(terminal.offsetWidth / 20);
    
    for (let i = 0; i < columns; i++) {
        createMatrixColumn(matrixContainer, i * 20, matrixChars);
    }
    
    // Arrêter automatiquement après 10 secondes
    setTimeout(() => {
        if (matrixContainer && terminal.contains(matrixContainer)) {
            matrixContainer.remove();
        }
    }, 10000);
}

function createMatrixColumn(container, x, chars) {
    const columnHeight = Math.random() * 20 + 10;
    
    for (let i = 0; i < columnHeight; i++) {
        setTimeout(() => {
            const char = document.createElement('div');
            char.className = 'matrix-char';
            char.textContent = chars[Math.floor(Math.random() * chars.length)];
            char.style.left = x + 'px';
            char.style.animationDelay = Math.random() * 2 + 's';
            char.style.animationDuration = (2 + Math.random() * 4) + 's';
            
            container.appendChild(char);
            
            // Supprimer le caractère après l'animation
            setTimeout(() => {
                if (container.contains(char)) {
                    container.removeChild(char);
                }
            }, 6000);
        }, i * 100);
    }
}

// Améliorer les stats en temps réel
function updateTerminalStats() {
    const cpuValue = document.querySelector('.cpu-usage .stat-value');
    const memValue = document.querySelector('.mem-usage .stat-value');
    
    if (cpuValue && memValue) {
        setInterval(() => {
            const cpu = Math.floor(Math.random() * 40) + 30; // 30-70%
            const mem = Math.floor(Math.random() * 30) + 50; // 50-80%
            
            cpuValue.textContent = cpu + '%';
            memValue.textContent = mem + '%';
            
            // Changer la couleur selon l'utilisation
            if (cpu > 60) {
                cpuValue.style.color = '#ff6b35';
            } else {
                cpuValue.style.color = 'var(--primary-green)';
            }
            
            if (mem > 75) {
                memValue.style.color = '#ff6b35';
            } else {
                memValue.style.color = 'var(--primary-green)';
            }
        }, 2000);
    }
}

// Initialiser les stats du terminal
setTimeout(updateTerminalStats, 1000);

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

// Script for learning.html - Simplified version
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script de learning.html chargé');
    
    // Add initial animations
    initializeAnimations();
    
    const modeCards = document.querySelectorAll('.mode-card');
    console.log('Mode cards trouvées:', modeCards.length);
    
    modeCards.forEach((card, index) => {
        console.log(`Ajout d'event listener à la carte ${index}:`, card);
        
        // Add staggered entrance animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 200);
        
        card.style.cursor = 'pointer';
        
        // Add click event listener (en plus de l'onclick HTML)
        card.addEventListener('click', function() {
            const mode = this.getAttribute('data-mode');
            console.log('Click détecté sur carte avec mode:', mode);
            redirectToQuiz(mode);
        });
        
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.mode-icon');
            if (icon) {
                icon.style.animation = 'pulse 1s ease-in-out infinite';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.mode-icon');
            if (icon) {
                icon.style.animation = 'float 3s ease-in-out infinite';
            }
        });
    });
    
    // Initialize floating animation for icons
    setTimeout(addFloatingAnimation, 1000);
    
    // Add parallax effect to header
    addParallaxEffect();
});

// Function to redirect to quiz pages
function redirectToQuiz(mode) {
    console.log('Redirection vers:', mode);
    
    // Add loading indicator
    const card = document.querySelector(`[data-mode="${mode}"]`);
    if (card) {
        addLoadingIndicator(card);
        
        // Add click animation
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);
    }
    
    // Redirect after animation
    setTimeout(() => {
        if (mode === 'quiz') {
            console.log('Redirection vers /quiz');
            window.location.href = '/quiz';
        } else if (mode === 'pld') {
            console.log('Redirection vers /pld');
            window.location.href = '/pld';
        }
    }, 500);
}

function initializeAnimations() {
    // Add animation to info items
    const infoItems = document.querySelectorAll('.info-item');
    infoItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-spinner {
            width: 20px;
            height: 20px;
            border: 2px solid #ffffff;
            border-top: 2px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
            margin-top: 1rem;
        }
    `;
    document.head.appendChild(style);
}

function addFloatingAnimation() {
    const modeIcons = document.querySelectorAll('.mode-icon');
    
    modeIcons.forEach(icon => {
        icon.style.animation = 'float 3s ease-in-out infinite';
    });
}

function addParallaxEffect() {
    const learningHeader = document.querySelector('.learning-header');
    if (learningHeader) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.3;
            learningHeader.style.transform = `translateY(${rate}px)`;
        });
    }
}

function addLoadingIndicator(card) {
    const existingSpinner = card.querySelector('.loading-spinner');
    if (!existingSpinner) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        card.appendChild(spinner);
        
        // Remove spinner after redirect
        setTimeout(() => {
            if (spinner.parentNode) {
                spinner.parentNode.removeChild(spinner);
            }
        }, 2000);
    }
}

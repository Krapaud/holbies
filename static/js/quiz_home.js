/**
 * Quiz Home Page JavaScript Functions
 * Animations et interactions pour la page d'accueil des quiz
 */

// =============================================================================
// Initialisation
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    initAnimations();
    initHoverEffects();
    initProgressBars();
    initTipAnimations();
    initTypingEffect();
    initParallax();
    initScrollAnimations();
    addCustomStyles();
});

// =============================================================================
// Animations d'entrée
// =============================================================================

function initAnimations() {
    // Animation d'entrée pour les cartes de catégories
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Animation d'entrée pour les cartes d'information
    const infoCards = document.querySelectorAll('.info-card.enhanced');
    infoCards.forEach((card, index) => {
        card.style.animationDelay = `${(index + categoryCards.length) * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Animation d'entrée pour les cartes de conseils
    const tipCards = document.querySelectorAll('.tip-card');
    tipCards.forEach((card, index) => {
        card.style.animationDelay = `${(index + categoryCards.length + infoCards.length) * 0.1}s`;
        card.classList.add('fade-in-up');
    });
}

// =============================================================================
// Effets hover
// =============================================================================

function initHoverEffects() {
    const categoryCards = document.querySelectorAll('.category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            
            // Effet sur les tags de sujets
            const tags = this.querySelectorAll('.topic-tag');
            tags.forEach((tag, index) => {
                setTimeout(() => {
                    tag.style.transform = 'scale(1.1)';
                    tag.style.background = 'rgba(0, 255, 65, 0.2)';
                }, index * 50);
            });
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            
            // Remettre les tags à l'état normal
            const tags = this.querySelectorAll('.topic-tag');
            tags.forEach(tag => {
                tag.style.transform = 'scale(1)';
                tag.style.background = 'rgba(0, 255, 65, 0.1)';
            });
        });
    });
}

// =============================================================================
// Barres de progression
// =============================================================================

function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';
                
                setTimeout(() => {
                    progressBar.style.transition = 'width 1.5s ease-out';
                    progressBar.style.width = width;
                }, 200);
                
                progressObserver.unobserve(progressBar);
            }
        });
    }, observerOptions);
    
    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
}

// =============================================================================
// Animations des conseils
// =============================================================================

function initTipAnimations() {
    const tipNumbers = document.querySelectorAll('.tip-number');
    tipNumbers.forEach((number, index) => {
        setTimeout(() => {
            number.style.animation = 'bounce 0.6s ease-out';
        }, (index + 1) * 200);
    });
}

// =============================================================================
// Effet de typing
// =============================================================================

function initTypingEffect() {
    const bonusTitle = document.querySelector('.bonus-title');
    if (bonusTitle) {
        const text = bonusTitle.textContent;
        bonusTitle.textContent = '';
        
        setTimeout(() => {
            let i = 0;
            const typeWriter = setInterval(() => {
                bonusTitle.textContent += text.charAt(i);
                i++;
                if (i > text.length - 1) {
                    clearInterval(typeWriter);
                    bonusTitle.style.borderRight = 'none';
                }
            }, 100);
            bonusTitle.style.borderRight = '2px solid var(--primary-green)';
        }, 2000);
    }
}

// =============================================================================
// Effet parallax
// =============================================================================

function initParallax() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.section-icon, .hero-icon');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

// =============================================================================
// Animations au scroll
// =============================================================================

function initScrollAnimations() {
    const sections = document.querySelectorAll('.quiz-info-section, .quiz-tips-section');
    const sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInFromLeft 0.8s ease-out';
            }
        });
    }, { threshold: 0.3 });
    
    sections.forEach(section => {
        sectionObserver.observe(section);
    });
}

// =============================================================================
// Styles personnalisés
// =============================================================================

function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fade-in-up {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 60%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            80% {
                transform: translateY(-5px);
            }
        }
        
        @keyframes slideInFromLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .fade-in-up {
            animation: fade-in-up 0.6s ease-out both;
        }
    `;
    document.head.appendChild(style);
}

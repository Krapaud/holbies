// Home page specific JavaScript
document.addEventListener('DOMContentLoaded', () => {
    animateHeroText();
    setupFeatureCards();
    animateStats();
    createCodeAnimation();
});

function animateHeroText() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;

    // Add typewriter effect to subtitle
    const subtitle = document.querySelector('.hero-subtitle');
    if (subtitle) {
        const text = subtitle.textContent;
        subtitle.textContent = '';
        subtitle.style.borderRight = '2px solid var(--primary-green)';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                setTimeout(() => {
                    subtitle.style.borderRight = 'none';
                }, 1000);
            }
        };
        
        // Start typing after a delay
        setTimeout(typeWriter, 1000);
    }
}

function setupFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    
    featureCards.forEach((card, index) => {
        // Add staggered animation
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 * index);

        // Add hover sound effect (visual feedback)
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
        });
    });
}

function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumber(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });

    statNumbers.forEach(stat => observer.observe(stat));
}

function animateNumber(element) {
    const text = element.textContent;
    const isInfinity = text === '∞';
    const hasPlus = text.includes('+');
    const number = isInfinity ? 0 : parseInt(text.replace(/\D/g, ''));
    
    if (isInfinity) {
        element.textContent = '∞';
        element.style.animation = 'pulse 2s infinite';
        return;
    }

    let current = 0;
    const increment = number / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= number) {
            current = number;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current) + (hasPlus ? '+' : '');
    }, 50);
}

function createCodeAnimation() {
    const codeLines = document.querySelectorAll('.code-line');
    
    codeLines.forEach((line, index) => {
        // Add cursor effect
        line.addEventListener('animationend', () => {
            if (index === codeLines.length - 1) {
                // Add blinking cursor to last line
                const cursor = document.createElement('span');
                cursor.textContent = '_';
                cursor.style.animation = 'blink 1s infinite';
                cursor.style.color = 'var(--primary-green)';
                line.appendChild(cursor);
                
                // Add blink animation if not present
                if (!document.getElementById('blink-animation')) {
                    const style = document.createElement('style');
                    style.id = 'blink-animation';
                    style.textContent = `
                        @keyframes blink {
                            0%, 50% { opacity: 1; }
                            51%, 100% { opacity: 0; }
                        }
                    `;
                    document.head.appendChild(style);
                }
            }
        });
    });
}

// Create floating particles effect
function createParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particles-container';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;
    
    document.body.appendChild(particleContainer);

    for (let i = 0; i < 20; i++) {
        createParticle(particleContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.cssText = `
        position: absolute;
        width: 2px;
        height: 2px;
        background: var(--primary-green);
        border-radius: 50%;
        animation: float ${10 + Math.random() * 20}s linear infinite;
        left: ${Math.random() * 100}%;
        top: 100%;
        opacity: ${0.2 + Math.random() * 0.3};
    `;
    
    container.appendChild(particle);
    
    // Remove particle after animation
    setTimeout(() => {
        if (particle.parentNode) {
            particle.parentNode.removeChild(particle);
        }
    }, 30000);
}

// Add CSS for particles
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes float {
        0% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 0.5;
        }
        90% {
            opacity: 0.5;
        }
        100% {
            transform: translateY(-100vh) translateX(${Math.random() * 200 - 100}px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(particleStyle);

// Initialize particles
setTimeout(createParticles, 2000);

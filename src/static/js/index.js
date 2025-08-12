// Script for index.html
document.addEventListener('DOMContentLoaded', () => {
    const heroTitleElement = document.querySelector('.hero-title');
    const heroSubtitleElement = document.querySelector('.hero-subtitle');
    const featuresButton = document.querySelector('a[href="#features"]');

    const originalTitleText = "HOLBIES";
    const originalSubtitleText = "Learning Hub";

    // Affichage direct du titre sans animation typewriter
    if (heroTitleElement) {
        heroTitleElement.textContent = originalTitleText;
    }

    // Typewriter effect for hero subtitle only
    if (heroSubtitleElement) {
        heroSubtitleElement.textContent = ''; // Clear content
        typeWriter(heroSubtitleElement, originalSubtitleText, null, true); // With blinking cursor
    }

    // Smooth scroll for "Découvrir les fonctionnalités" button
    if (featuresButton) {
        featuresButton.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor jump
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                console.log('Scrolling to:', targetId);
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    }

    // Dynamically fetch and update stats
    fetch('/quiz/stats')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const statNumbers = document.querySelectorAll('.stat-number');
            if (statNumbers.length >= 3) {
                if (data && data.questions !== undefined) {
                    statNumbers[0].textContent = data.questions;
                }
                if (data && data.users !== undefined) {
                    statNumbers[1].textContent = data.users;
                }
                if (data && data.satisfaction !== undefined) {
                    statNumbers[2].textContent = data.satisfaction + '%';
                }
            }
        })
        .catch(err => {
            console.error('Erreur lors de la récupération des stats:', err);
        });

    // --- Hero Terminal Animation ---
    try {
        const heroCodeLines = [
            "// Système d'apprentissage HOLBIES",
            "class LearningPlatform {",
            "  constructor() {",
            "    this.modules = ['Python', 'JavaScript', 'DevOps', 'Algorithms'];",
            "    this.users = 1250;",
            "    this.quizzes = 847;",
            "    this.aiEnabled = true;",
            "    this.adaptiveLearning = true;",
            "  }",
            "",
            "  async startLearning(student) {",
            "    console.log(`Bienvenue ${student.name}!`);",
            "    const course = this.recommendCourse(student.level);",
            "    const progress = await this.trackProgress(student.id);",
            "    return await this.generatePersonalizedQuiz(course);",
            "  }",
            "",
            "  generatePersonalizedQuiz(course) {",
            "    return {",
            "      difficulty: 'adaptive',",
            "      aiCorrection: true,",
            "      realTimeFeedback: true,",
            "      interactiveElements: true,",
            "      progressTracking: true",
            "    };",
            "  }",
            "",
            "  recommendCourse(level) {",
            "    const courses = {",
            "      beginner: 'Python Fundamentals',",
            "      intermediate: 'Web Development',",
            "      advanced: 'System Architecture'",
            "    };",
            "    return courses[level] || courses.beginner;",
            "  }",
            "}",
            "",
            "// Démarrage de votre parcours d'apprentissage...",
            "const holbies = new LearningPlatform();",
            "holbies.startLearning({ name: 'Étudiant', level: 'intermediate', id: 1001 });"
        ];

        // Utiliser la nouvelle fonction universelle
        if (window.createAdaptiveTerminalAnimation) {
            const heroAnimation = window.createAdaptiveTerminalAnimation(
                'hero-code-animation-container',
                heroCodeLines,
                {
                    typingSpeed: 35,
                    lineDelay: 400,
                    restartDelay: 4000,
                    scrollOffset: 20
                }
            );
            
            if (heroAnimation) {
                heroAnimation.start();
            }
        }

    } catch (e) {
        console.error('Erreur animation terminal héros:', e);
    }
});

function typeWriter(element, text, callback = null, withCursor = false) {
    let i = 0;
    let cursor = null;

    if (withCursor) {
        cursor = document.createElement('span');
        cursor.textContent = '|';
        cursor.className = 'typewriter-cursor';
        element.appendChild(cursor);
    }

    const speed = 100; // typing speed in ms

    function type() {
        if (i < text.length) {
            element.textContent = text.substring(0, i + 1);
            if (withCursor) {
                element.appendChild(cursor);
            }
            i++;
            setTimeout(type, speed);
        } else {
            if (withCursor && cursor) {
                // Keep cursor blinking for a short while, then remove
                cursor.style.animation = 'blink-animation 0.75s step-end infinite';
                setTimeout(() => {
                    cursor.remove();
                }, 1500); // Remove cursor after 1.5 seconds
            }
            if (callback) {
                callback();
            }
        }
    }
    type();
}

// Add CSS for blinking cursor animation (if not already in main.css)
// This ensures the animation is defined even if main.css is not fully loaded or overridden
(function() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes blink-animation {
            from, to { opacity: 0 }
            50% { opacity: 1 }
        }
        .typewriter-cursor {
            display: inline-block;
            margin-left: 2px;
            color: var(--holberton-primary); /* Use Holberton primary for cursor */
            vertical-align: bottom;
        }
    `;
    document.head.appendChild(style);
})();
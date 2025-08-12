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
        const heroCodeContainer = document.getElementById('hero-code-animation-container');
        if (!heroCodeContainer) {
            return; // Skip if container doesn't exist
        }

        const heroCodeElement = heroCodeContainer.querySelector('code');
        if (!heroCodeElement) {
            return;
        }

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
        
        const heroCursorElement = document.createElement('span');
        heroCursorElement.classList.add('cursor');
        
        heroCodeElement.innerHTML = '';
        heroCodeElement.appendChild(heroCursorElement);

        let heroCurrentContent = '';
        let heroLineIndex = 0;
        let heroCharIndex = 0;

        function typeHeroCode() {
            try {
                if (heroLineIndex >= heroCodeLines.length) {
                    setTimeout(() => {
                        heroLineIndex = 0;
                        heroCharIndex = 0;
                        heroCurrentContent = '';
                        heroCodeElement.textContent = '';
                        heroCodeElement.appendChild(heroCursorElement);
                        // Force scroll to top - seulement le conteneur terminal
                        if (heroCodeContainer) {
                            heroCodeContainer.scrollTop = 0;
                        }
                        typeHeroCode();
                    }, 4000);
                    return;
                }

                const currentLine = heroCodeLines[heroLineIndex];
                if (heroCharIndex < currentLine.length) {
                    heroCurrentContent += currentLine[heroCharIndex];
                    heroCodeElement.textContent = heroCurrentContent;
                    heroCodeElement.appendChild(heroCursorElement);
                heroCharIndex++;
                
                // Scroll UNIQUEMENT dans le conteneur terminal, pas la page entière
                if (heroCodeContainer && heroCursorElement) {
                    setTimeout(() => {
                        // Calculer la position du curseur dans le conteneur seulement
                        const containerRect = heroCodeContainer.getBoundingClientRect();
                        const cursorRect = heroCursorElement.getBoundingClientRect();
                        
                        // Scroll seulement si le curseur sort du conteneur visible
                        if (cursorRect.bottom > containerRect.bottom) {
                            heroCodeContainer.scrollTop += (cursorRect.bottom - containerRect.bottom + 10);
                        }
                    }, 10);
                }                    setTimeout(typeHeroCode, 45);
                } else {
                    heroCurrentContent += '\n';
                    heroCodeElement.textContent = heroCurrentContent;
                    heroCodeElement.appendChild(heroCursorElement);
                heroLineIndex++;
                heroCharIndex = 0;
                
                // Scroll UNIQUEMENT dans le conteneur terminal, pas la page entière
                if (heroCodeContainer && heroCursorElement) {
                    setTimeout(() => {
                        // Calculer la position du curseur dans le conteneur seulement
                        const containerRect = heroCodeContainer.getBoundingClientRect();
                        const cursorRect = heroCursorElement.getBoundingClientRect();
                        
                        // Scroll seulement si le curseur sort du conteneur visible
                        if (cursorRect.bottom > containerRect.bottom) {
                            heroCodeContainer.scrollTop += (cursorRect.bottom - containerRect.bottom + 10);
                        }
                    }, 10);
                }                    setTimeout(typeHeroCode, 600);
                }
            } catch (error) {
                console.error('Erreur dans typeHeroCode:', error);
                // Redémarrer l'animation en cas d'erreur
                setTimeout(() => {
                    heroLineIndex = 0;
                    heroCharIndex = 0;
                    heroCurrentContent = '';
                    typeHeroCode();
                }, 2000);
            }
        }        // Start the animation after a short delay
        setTimeout(typeHeroCode, 1000);

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
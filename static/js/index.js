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
// quiz_results.js - Fonctionnalités pour la page de résultats de quiz

document.addEventListener('DOMContentLoaded', function() {
    // Animation d'entrée
    const resultsContainer = document.querySelector('.quiz-results-container');
    resultsContainer.classList.add('fade-in');
    
    // Animation du score circle
    const scoreCircle = document.querySelector('.score-circle');
    setTimeout(() => {
        scoreCircle.classList.add('animate-score');
    }, 500);
    
    // Animation des cartes de réponses
    const answerCards = document.querySelectorAll('.answer-card');
    answerCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('slide-in-left');
    });
    
    // Animation du badge de performance
    const badge = document.querySelector('.performance-badge .badge');
    setTimeout(() => {
        badge.classList.add('bounce-in');
    }, 1000);
    
    // Confetti pour les bons scores
    const percentageElement = document.querySelector('.score-percentage');
    if (percentageElement) {
        const percentage = parseInt(percentageElement.textContent.replace('%', ''));
        if (percentage >= 80) {
            setTimeout(() => {
                createConfetti();
            }, 1500);
        }
    }
});

function createConfetti() {
    const colors = ['#00ff41', '#00cc33', '#ff6b35', '#00ccff'];
    const confettiContainer = document.createElement('div');
    confettiContainer.className = 'confetti-container';
    document.body.appendChild(confettiContainer);
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
        confettiContainer.appendChild(confetti);
    }
    
    setTimeout(() => {
        confettiContainer.remove();
    }, 6000);
}

// Partage des résultats (simulation)
function shareResults() {
    const scoreElement = document.querySelector('.score-number');
    const categoryElement = document.querySelector('.results-subtitle');
    
    if (scoreElement && categoryElement) {
        const score = scoreElement.textContent;
        const category = categoryElement.textContent;
        const text = `Je viens de faire ${score} au quiz ${category} sur Dev Learning Hub ! 🎯`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Mes résultats de quiz C',
                text: text,
                url: window.location.href
            });
        } else {
            // Copier dans le presse-papiers
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Résultats copiés dans le presse-papiers !', 'success');
            });
        }
    }
}

// Fonction utilitaire pour afficher des notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background: var(--background-dark);
        color: var(--primary-green);
        border: 1px solid var(--primary-green);
        border-radius: 8px;
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

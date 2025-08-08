// Script for learning.html
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script de learning.html chargé');
    
    const modeCards = document.querySelectorAll('.mode-card');
    console.log('Mode cards trouvées:', modeCards.length);
    
    modeCards.forEach((card, index) => {
        console.log(`Ajout d'event listener à la carte ${index}:`, card);
        
        card.addEventListener('click', function() {
            const mode = this.getAttribute('data-mode');
            console.log('Carte cliquée, mode:', mode);
            
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
            
            setTimeout(() => {
                if (mode === 'quiz') {
                    console.log('Redirection vers /quiz');
                    window.location.href = '/quiz';
                } else if (mode === 'ai-quiz') {
                    console.log('Redirection vers /ai-quiz');
                    window.location.href = '/ai-quiz';
                }
            }, 200);
        });
        
        card.style.cursor = 'pointer';
    });
});

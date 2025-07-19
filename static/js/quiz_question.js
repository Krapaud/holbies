// quiz_question.js - Fonctionnalités pour la page de question de quiz

document.addEventListener('DOMContentLoaded', function() {
    // Animation d'entrée
    const questionCard = document.querySelector('.question-card');
    questionCard.classList.add('slide-in');
    
    // Focus automatique sur le textarea
    const textarea = document.getElementById('answer');
    textarea.focus();
    
    // Animation de la barre de progression
    const progressFill = document.querySelector('.progress-fill');
    const progressValue = progressFill.getAttribute('data-progress');
    progressFill.style.width = progressValue + '%';
    setTimeout(() => {
        progressFill.style.transition = 'width 1s ease-out';
    }, 500);
    
    // Effet de focus sur le textarea
    textarea.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    textarea.addEventListener('blur', function() {
        if (!this.value) {
            this.parentElement.classList.remove('focused');
        }
    });
    
    // Compteur de caractères
    textarea.addEventListener('input', function() {
        const length = this.value.length;
        const hint = this.parentElement.querySelector('.form-hint');
        
        if (length < 10) {
            hint.textContent = `💡 Conseil : Votre réponse est un peu courte (${length} caractères). Essayez d'être plus détaillé.`;
            hint.style.color = '#ff6b35';
        } else if (length < 50) {
            hint.textContent = `💡 Bien ! Votre réponse prend forme (${length} caractères). Continuez...`;
            hint.style.color = '#00cc33';
        } else {
            hint.textContent = `💡 Excellent ! Réponse détaillée (${length} caractères). Vous êtes sur la bonne voie !`;
            hint.style.color = '#00ff41';
        }
    });
    
    // Animation des cercles de progression
    const circles = document.querySelectorAll('.counter-circle');
    circles.forEach((circle, index) => {
        circle.style.animationDelay = `${index * 0.1}s`;
        circle.classList.add('fade-in');
    });
    
    // Sauvegarde automatique (localStorage)
    textarea.addEventListener('input', function() {
        localStorage.setItem('quiz_answer_draft', this.value);
    });
    
    // Restaurer le brouillon
    const draft = localStorage.getItem('quiz_answer_draft');
    if (draft && textarea.value === '') {
        textarea.value = draft;
        textarea.dispatchEvent(new Event('input'));
    }
    
    // Nettoyer le brouillon à la soumission
    document.querySelector('.answer-form').addEventListener('submit', function() {
        localStorage.removeItem('quiz_answer_draft');
    });
});

// Raccourci clavier Ctrl+Enter pour soumettre
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        document.querySelector('.answer-form').submit();
    }
});

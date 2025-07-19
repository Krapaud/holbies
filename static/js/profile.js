/**
 * Profile Page JavaScript Functions
 * Gestion des animations et modals du profil utilisateur
 */

// =============================================================================
// Initialisation et animations
// =============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Animation d'entrée
    const profileCard = document.querySelector('.profile-card');
    if (profileCard) {
        profileCard.classList.add('slide-in');
    }
    
    // Animation des badges
    const badges = document.querySelectorAll('.badge-item');
    badges.forEach((badge, index) => {
        badge.style.animationDelay = `${index * 0.1}s`;
        badge.classList.add('fade-in-up');
    });
    
    // Initialiser les événements des modals
    initModalEvents();
});

// =============================================================================
// Fonctions des modals
// =============================================================================

function editProfile() {
    const modal = document.getElementById('editModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function changePassword() {
    const modal = document.getElementById('passwordModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

function initModalEvents() {
    // Fermer les modals en cliquant à l'extérieur
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal();
        }
    });

    // Fermer les modals avec les boutons de fermeture
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    // Fermer avec Échap
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}

// =============================================================================
// Fonctions globales
// =============================================================================

// Exporter les fonctions pour l'accès global
window.editProfile = editProfile;
window.changePassword = changePassword;
window.closeModal = closeModal;

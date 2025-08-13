/**
 * Système de notifications toast
 * Permet d'afficher des messages informatifs, d'erreur, de succès ou d'avertissement
 */

class ToastManager {
    constructor() {
        this.container = null;
        this.toasts = new Map();
        this.toastCounter = 0;
        this.init();
    }

    init() {
        // Créer le conteneur de toast s'il n'existe pas
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    /**
     * Affiche une notification toast
     * @param {string} message - Le message à afficher
     * @param {string} type - Le type de toast (success, error, warning, info)
     * @param {Object} options - Options additionnelles
     */
    show(message, type = 'info', options = {}) {
        const defaultOptions = {
            title: null,
            duration: 5000, // 5 secondes par défaut
            autoDismiss: true,
            closable: true,
            position: 'top-right'
        };

        const opts = { ...defaultOptions, ...options };
        const toastId = ++this.toastCounter;

        // Créer l'élément toast
        const toast = this.createToastElement(message, type, opts, toastId);
        
        // Ajouter au conteneur
        this.container.appendChild(toast);
        this.toasts.set(toastId, toast);

        // Animer l'entrée
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        // Auto-dismiss si activé
        if (opts.autoDismiss && opts.duration > 0) {
            setTimeout(() => {
                this.dismiss(toastId);
            }, opts.duration);
        }

        return toastId;
    }

    createToastElement(message, type, options, toastId) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.dataset.toastId = toastId;

        // Ajouter la classe pour l'auto-dismiss si nécessaire
        if (options.autoDismiss) {
            toast.classList.add('auto-dismiss');
        }

        // Contenu du toast
        let content = `
            <div class="toast-icon"></div>
            <div class="toast-content">
        `;

        if (options.title) {
            content += `<div class="toast-title">${this.escapeHtml(options.title)}</div>`;
        }

        content += `<div class="toast-message">${this.escapeHtml(message)}</div>`;
        content += `</div>`;

        // Bouton de fermeture si activé
        if (options.closable) {
            content += `<button class="toast-close" onclick="window.toastManager.dismiss(${toastId})"></button>`;
        }

        // Barre de progression si auto-dismiss
        if (options.autoDismiss && options.duration > 0) {
            content += `<div class="toast-progress"></div>`;
        }

        toast.innerHTML = content;

        return toast;
    }

    /**
     * Ferme une notification toast
     * @param {number} toastId - L'ID du toast à fermer
     */
    dismiss(toastId) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;

        toast.classList.remove('show');
        toast.classList.add('hide');

        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
            this.toasts.delete(toastId);
        }, 300);
    }

    /**
     * Ferme tous les toasts
     */
    dismissAll() {
        this.toasts.forEach((toast, id) => {
            this.dismiss(id);
        });
    }

    /**
     * Méthodes de convenance pour les différents types
     */
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }

    error(message, options = {}) {
        return this.show(message, 'error', { ...options, duration: 7000 });
    }

    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }

    info(message, options = {}) {
        return this.show(message, 'info', options);
    }

    /**
     * Escape HTML pour éviter les injections XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialiser le gestionnaire de toast globalement
window.toastManager = new ToastManager();

// Méthodes globales pour faciliter l'utilisation
window.showToast = (message, type, options) => window.toastManager.show(message, type, options);
window.showSuccess = (message, options) => window.toastManager.success(message, options);
window.showError = (message, options) => window.toastManager.error(message, options);
window.showWarning = (message, options) => window.toastManager.warning(message, options);
window.showInfo = (message, options) => window.toastManager.info(message, options);

// Export pour modules ES6 si nécessaire
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ToastManager;
}

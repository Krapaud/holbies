// Générateur de vidéo de bienvenue de test
// Ce script génère une vidéo de bienvenue animée si aucune vidéo n'est trouvée

class WelcomeVideoGenerator {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.animationId = null;
        this.startTime = null;
        this.duration = 5000; // 5 secondes
    }

    generateTestVideo() {
        return new Promise((resolve) => {
            // Créer un canvas pour l'animation
            this.canvas = document.createElement('canvas');
            this.canvas.width = 800;
            this.canvas.height = 600;
            this.ctx = this.canvas.getContext('2d');

            // Créer une modal temporaire pour afficher l'animation
            const modal = document.createElement('div');
            modal.className = 'video-modal';
            modal.style.background = 'rgba(0, 0, 0, 0.95)';

            const container = document.createElement('div');
            container.className = 'video-container';
            container.style.background = '#0d1117';
            container.style.border = '2px solid #00ff41';
            container.style.borderRadius = '8px';
            container.style.padding = '20px';
            container.style.textAlign = 'center';

            // Bouton de fermeture
            const closeBtn = document.createElement('button');
            closeBtn.className = 'video-close';
            closeBtn.innerHTML = '×';
            closeBtn.onclick = () => this.closeTestVideo(modal, resolve);

            // Style du canvas
            this.canvas.style.maxWidth = '100%';
            this.canvas.style.maxHeight = '100%';
            this.canvas.style.border = '1px solid #00ff41';
            this.canvas.style.borderRadius = '4px';

            container.appendChild(closeBtn);
            container.appendChild(this.canvas);
            modal.appendChild(container);
            document.body.appendChild(modal);

            // Démarrer l'animation
            this.startTime = Date.now();
            this.animate();

            // Auto-fermeture après la durée
            setTimeout(() => {
                this.closeTestVideo(modal, resolve);
            }, this.duration);

            // Empêcher le scroll
            document.body.style.overflow = 'hidden';
        });
    }

    animate() {
        const currentTime = Date.now();
        const elapsed = currentTime - this.startTime;
        const progress = Math.min(elapsed / this.duration, 1);

        // Nettoyer le canvas
        this.ctx.fillStyle = '#0d1117';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Effet Matrix en arrière-plan
        this.drawMatrixRain(elapsed);

        // Texte principal
        this.drawWelcomeText(progress);

        // Logo/animation centrale
        this.drawCentralAnimation(elapsed);

        if (progress < 1) {
            this.animationId = requestAnimationFrame(() => this.animate());
        }
    }

    drawMatrixRain(elapsed) {
        const cols = Math.floor(this.canvas.width / 20);
        const drops = [];

        // Initialiser les gouttes si nécessaire
        if (!this.drops) {
            this.drops = [];
            for (let i = 0; i < cols; i++) {
                this.drops[i] = Math.random() * this.canvas.height;
            }
        }

        this.ctx.fillStyle = 'rgba(0, 255, 65, 0.1)';
        this.ctx.font = '12px monospace';

        for (let i = 0; i < this.drops.length; i++) {
            const text = String.fromCharCode(0x30A0 + Math.random() * 96);
            this.ctx.fillText(text, i * 20, this.drops[i]);

            if (this.drops[i] > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            this.drops[i] += 2;
        }
    }

    drawWelcomeText(progress) {
        // Titre principal
        this.ctx.fillStyle = '#00ff41';
        this.ctx.font = 'bold 48px Orbitron, monospace';
        this.ctx.textAlign = 'center';
        
        const welcomeOpacity = Math.min(progress * 2, 1);
        this.ctx.globalAlpha = welcomeOpacity;
        
        const titleY = this.canvas.height / 2 - 50;
        this.ctx.fillText('BIENVENUE', this.canvas.width / 2, titleY);

        // Sous-titre
        this.ctx.font = '24px Source Code Pro, monospace';
        this.ctx.fillStyle = '#8b949e';
        
        const subtitleOpacity = Math.max(0, (progress - 0.3) * 2);
        this.ctx.globalAlpha = subtitleOpacity;
        
        this.ctx.fillText('HOLBIES LEARNING HUB', this.canvas.width / 2, titleY + 50);

        // Message d'accès
        this.ctx.font = '16px Source Code Pro, monospace';
        const messageOpacity = Math.max(0, (progress - 0.6) * 2);
        this.ctx.globalAlpha = messageOpacity;
        
        this.ctx.fillText('Accès accordé. Initialisation du système...', this.canvas.width / 2, titleY + 100);

        this.ctx.globalAlpha = 1;
    }

    drawCentralAnimation(elapsed) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Cercle pulsant
        const pulseRadius = 30 + Math.sin(elapsed * 0.005) * 10;
        
        this.ctx.strokeStyle = '#00ff41';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY - 150, pulseRadius, 0, Math.PI * 2);
        this.ctx.stroke();

        // Particules orbitales
        for (let i = 0; i < 8; i++) {
            const angle = (elapsed * 0.002) + (i * Math.PI / 4);
            const orbitRadius = 60;
            const x = centerX + Math.cos(angle) * orbitRadius;
            const y = centerY - 150 + Math.sin(angle) * orbitRadius;
            
            this.ctx.fillStyle = '#00ff41';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }

    closeTestVideo(modal, resolve) {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        if (modal && modal.parentNode) {
            modal.parentNode.removeChild(modal);
        }
        
        document.body.style.overflow = '';
        resolve();
    }
}

// Fonction d'aide pour utiliser la vidéo de test
window.showTestWelcomeVideo = function() {
    const generator = new WelcomeVideoGenerator();
    return generator.generateTestVideo();
};

// Générateur de vidéo de bienvenue de test
// Ce script génère une vidéo de bienvenue animée si aucune vidéo n'est trouvée

class WelcomeVideoGenerator {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.animationId = null;
        this.startTime = null;
        this.duration = 5000; // 5 secondes
    }

    generateTestVideo() {
        return new Promise((resolve) => {
            // Créer un canvas pour l'animation
            this.canvas = document.createElement('canvas');
            this.canvas.width = 800;
            this.canvas.height = 600;
            this.ctx = this.canvas.getContext('2d');

            // Créer une modal temporaire pour afficher l'animation
            const modal = document.createElement('div');
            modal.className = 'video-modal';
            modal.style.background = 'rgba(0, 0, 0, 0.95)';

            const container = document.createElement('div');
            container.className = 'video-container';
            container.style.background = '#0d1117';
            container.style.border = '2px solid #00ff41';
            container.style.borderRadius = '8px';
            container.style.padding = '20px';
            container.style.textAlign = 'center';

            // Bouton de fermeture
            const closeBtn = document.createElement('button');
            closeBtn.className = 'video-close';
            closeBtn.innerHTML = '×';
            closeBtn.onclick = () => this.closeTestVideo(modal, resolve);

            // Style du canvas
            this.canvas.style.maxWidth = '100%';
            this.canvas.style.maxHeight = '100%';
            this.canvas.style.border = '1px solid #00ff41';
            this.canvas.style.borderRadius = '4px';

            container.appendChild(closeBtn);
            container.appendChild(this.canvas);
            modal.appendChild(container);
            document.body.appendChild(modal);

            // Démarrer l'animation
            this.startTime = Date.now();
            this.animate();

            // Auto-fermeture après la durée
            setTimeout(() => {
                this.closeTestVideo(modal, resolve);
            }, this.duration);

            // Empêcher le scroll
            document.body.style.overflow = 'hidden';
        });
    }

    animate() {
        const currentTime = Date.now();
        const elapsed = currentTime - this.startTime;
        const progress = Math.min(elapsed / this.duration, 1);

        // Nettoyer le canvas
        this.ctx.fillStyle = '#0d1117';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // Effet Matrix en arrière-plan
        this.drawMatrixRain(elapsed);

        // Texte principal
        this.drawWelcomeText(progress);

        // Logo/animation centrale
        this.drawCentralAnimation(elapsed);

        if (progress < 1) {
            this.animationId = requestAnimationFrame(() => this.animate());
        }
    }

    drawMatrixRain(elapsed) {
        const cols = Math.floor(this.canvas.width / 20);
        const drops = [];

        // Initialiser les gouttes si nécessaire
        if (!this.drops) {
            this.drops = [];
            for (let i = 0; i < cols; i++) {
                this.drops[i] = Math.random() * this.canvas.height;
            }
        }

        this.ctx.fillStyle = 'rgba(0, 255, 65, 0.1)';
        this.ctx.font = '12px monospace';

        for (let i = 0; i < this.drops.length; i++) {
            const text = String.fromCharCode(0x30A0 + Math.random() * 96);
            this.ctx.fillText(text, i * 20, this.drops[i]);

            if (this.drops[i] > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            this.drops[i] += 2;
        }
    }

    drawWelcomeText(progress) {
        // Titre principal
        this.ctx.fillStyle = '#00ff41';
        this.ctx.font = 'bold 48px Orbitron, monospace';
        this.ctx.textAlign = 'center';
        
        const welcomeOpacity = Math.min(progress * 2, 1);
        this.ctx.globalAlpha = welcomeOpacity;
        
        const titleY = this.canvas.height / 2 - 50;
        this.ctx.fillText('BIENVENUE', this.canvas.width / 2, titleY);

        // Sous-titre
        this.ctx.font = '24px Source Code Pro, monospace';
        this.ctx.fillStyle = '#8b949e';
        
        const subtitleOpacity = Math.max(0, (progress - 0.3) * 2);
        this.ctx.globalAlpha = subtitleOpacity;
        
        this.ctx.fillText('HOLBIES LEARNING HUB', this.canvas.width / 2, titleY + 50);

        // Message d'accès
        this.ctx.font = '16px Source Code Pro, monospace';
        const messageOpacity = Math.max(0, (progress - 0.6) * 2);
        this.ctx.globalAlpha = messageOpacity;
        
        this.ctx.fillText('Accès accordé. Initialisation du système...', this.canvas.width / 2, titleY + 100);

        this.ctx.globalAlpha = 1;
    }

    drawCentralAnimation(elapsed) {
        const centerX = this.canvas.width / 2;
        const centerY = this.canvas.height / 2;
        
        // Cercle pulsant
        const pulseRadius = 30 + Math.sin(elapsed * 0.005) * 10;
        
        this.ctx.strokeStyle = '#00ff41';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(centerX, centerY - 150, pulseRadius, 0, Math.PI * 2);
        this.ctx.stroke();

        // Particules orbitales
        for (let i = 0; i < 8; i++) {
            const angle = (elapsed * 0.002) + (i * Math.PI / 4);
            const orbitRadius = 60;
            const x = centerX + Math.cos(angle) * orbitRadius;
            const y = centerY - 150 + Math.sin(angle) * orbitRadius;
            
            this.ctx.fillStyle = '#00ff41';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 3, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }

    closeTestVideo(modal, resolve) {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        if (modal && modal.parentNode) {
            modal.parentNode.removeChild(modal);
        }
        
        document.body.style.overflow = '';
        resolve();
    }
}

// Fonction d'aide pour utiliser la vidéo de test
window.showTestWelcomeVideo = function() {
    const generator = new WelcomeVideoGenerator();
    return generator.generateTestVideo();
};

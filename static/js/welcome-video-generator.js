

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



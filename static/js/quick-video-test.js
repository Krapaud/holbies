// Test simple et direct de la vidéo
function quickVideoTest() {
    console.log('🎬 Test rapide de la vidéo...');
    
    // Créer une modal simple directement
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.background = 'rgba(0, 0, 0, 0.95)';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.zIndex = '9999';
    modal.style.backdropFilter = 'blur(10px)';
    
    const container = document.createElement('div');
    container.style.background = '#0d1117';
    container.style.border = '2px solid #00ff41';
    container.style.borderRadius = '8px';
    container.style.padding = '3rem';
    container.style.textAlign = 'center';
    container.style.maxWidth = '600px';
    container.style.position = 'relative';
    container.style.animation = 'borderGlow 2s ease-in-out infinite alternate';
    
    // Bouton de fermeture
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '×';
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '10px';
    closeBtn.style.right = '10px';
    closeBtn.style.background = 'rgba(0, 0, 0, 0.8)';
    closeBtn.style.border = '2px solid #00ff41';
    closeBtn.style.borderRadius = '50%';
    closeBtn.style.width = '40px';
    closeBtn.style.height = '40px';
    closeBtn.style.color = '#00ff41';
    closeBtn.style.fontSize = '20px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.onclick = () => document.body.removeChild(modal);
    
    // Contenu
    const content = document.createElement('div');
    content.innerHTML = `
        <h2 style="color: #00ff41; font-family: Orbitron, monospace; margin-bottom: 2rem; text-shadow: 0 0 10px #00ff41;">
            🎬 BIENVENUE
        </h2>
        <p style="color: #c9d1d9; font-family: 'Source Code Pro', monospace; font-size: 1.2rem; margin-bottom: 2rem;">
            HOLBIES LEARNING HUB
        </p>
        <p style="color: #8b949e; font-family: 'Source Code Pro', monospace; margin-bottom: 2rem;">
            Accès accordé. Initialisation du système...
        </p>
        <div style="width: 100%; height: 4px; background: #21262d; border-radius: 2px; margin: 2rem 0;">
            <div id="progress-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #00ff41, #008f11); border-radius: 2px; transition: width 0.3s ease;"></div>
        </div>
        <p style="color: #00ff41; font-size: 0.9rem;">
            Animation de test - Votre vidéo s'affichera ici
        </p>
    `;
    
    container.appendChild(closeBtn);
    container.appendChild(content);
    modal.appendChild(container);
    document.body.appendChild(modal);
    
    // Animation de la barre de progression
    const progressBar = container.querySelector('#progress-bar');
    let progress = 0;
    const interval = setInterval(() => {
        progress += 2;
        progressBar.style.width = progress + '%';
        
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                if (modal.parentNode) {
                    document.body.removeChild(modal);
                }
                console.log('✅ Test vidéo terminé !');
            }, 1000);
        }
    }, 100);
    
    // Fermeture automatique après 6 secondes
    setTimeout(() => {
        if (modal.parentNode) {
            clearInterval(interval);
            document.body.removeChild(modal);
        }
    }, 6000);
    
    console.log('✅ Modal de test créée et lancée !');
}

// Rendre la fonction globale
window.quickVideoTest = quickVideoTest;

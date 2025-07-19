// Script de débogage pour vérifier le système vidéo
console.log('🔍 === DÉBOGAGE SYSTÈME VIDÉO ===');

// 1. Vérifier les objets globaux
console.log('📋 Vérification des objets globaux:');
console.log('- VideoModal:', typeof window.VideoModal);
console.log('- videoModal:', typeof window.videoModal);
console.log('- showTestWelcomeVideo:', typeof window.showTestWelcomeVideo);
console.log('- showWelcomeVideo:', typeof window.showWelcomeVideo);
console.log('- testVideoModal:', typeof window.testVideoModal);
console.log('- quickVideoTest:', typeof window.quickVideoTest);

// 2. Tester la création d'une modal simple
function testSimpleModal() {
    console.log('🧪 Test de modal simple...');
    
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        font-family: monospace;
        color: #00ff41;
    `;
    
    modal.innerHTML = `
        <div style="
            background: #0d1117;
            border: 2px solid #00ff41;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            max-width: 400px;
        ">
            <h2 style="margin: 0 0 1rem 0;">🎬 TEST RÉUSSI !</h2>
            <p>Le système de modal fonctionne</p>
            <button onclick="this.closest('div').parentNode.remove()" 
                    style="
                        background: none;
                        border: 1px solid #00ff41;
                        color: #00ff41;
                        padding: 0.5rem 1rem;
                        border-radius: 4px;
                        cursor: pointer;
                        margin-top: 1rem;
                    ">
                Fermer
            </button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Auto-fermeture après 5 secondes
    setTimeout(() => {
        if (modal.parentNode) {
            modal.remove();
        }
    }, 5000);
    
    console.log('✅ Modal simple créée !');
}

// 3. Fonction de test universelle
function universalVideoTest() {
    console.log('🚀 Test universel...');
    
    // Essayer dans l'ordre de préférence
    if (window.testVideoModal) {
        console.log('Utilisation de testVideoModal');
        window.testVideoModal();
    } else if (window.quickVideoTest) {
        console.log('Utilisation de quickVideoTest');
        window.quickVideoTest();
    } else if (window.showTestWelcomeVideo) {
        console.log('Utilisation de showTestWelcomeVideo');
        window.showTestWelcomeVideo();
    } else {
        console.log('Utilisation de testSimpleModal');
        testSimpleModal();
    }
}

// 4. Exporter les fonctions
window.testSimpleModal = testSimpleModal;
window.universalVideoTest = universalVideoTest;

// 5. Test automatique au chargement
setTimeout(() => {
    console.log('🔄 Test automatique dans 2 secondes...');
    console.log('Vous pouvez taper universalVideoTest() dans la console pour tester manuellement.');
}, 2000);

console.log('🛠 Débogage prêt ! Utilisez universalVideoTest() pour tester.');

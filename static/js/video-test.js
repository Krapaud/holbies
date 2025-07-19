// Test du système de vidéo de bienvenue
// Ce script peut être exécuté dans la console du navigateur pour tester

// Attendre que tout soit chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎬 Scripts de test vidéo chargés');
    
    // Attendre un peu pour s'assurer que tous les scripts sont initialisés
    setTimeout(initializeVideoTests, 500);
});

function initializeVideoTests() {
    console.log('🔧 Initialisation des tests vidéo...');
    
    // Vérifier que les scripts sont chargés
    const checks = {
        'VideoModal class': typeof window.VideoModal !== 'undefined',
        'videoModal instance': typeof window.videoModal !== 'undefined',
        'showTestWelcomeVideo': typeof window.showTestWelcomeVideo !== 'undefined'
    };
    
    console.log('📋 Vérifications des dépendances:');
    Object.entries(checks).forEach(([name, status]) => {
        console.log(`${status ? '✅' : '❌'} ${name}`);
    });
    
    // Si videoModal n'est pas prêt, le créer
    if (!window.videoModal && window.VideoModal) {
        console.log('🔧 Création de videoModal...');
        window.videoModal = new window.VideoModal();
    }
    
    // Rendre les fonctions globales disponibles
    window.testVideoSystem = testVideoSystem;
    window.testVideoModal = testVideoModal;
    window.testRealVideo = testRealVideo;
    
    console.log('✅ Tests vidéo prêts !');
}

function testVideoSystem() {
    console.log('🎬 Test du système de vidéo de bienvenue');
    
    // Vérifier que les scripts sont chargés
    const checks = {
        'VideoModal': typeof window.VideoModal !== 'undefined',
        'videoModal instance': typeof window.videoModal !== 'undefined',
        'showTestWelcomeVideo': typeof window.showTestWelcomeVideo !== 'undefined',
        'showWelcomeVideo function': typeof window.showWelcomeVideo !== 'undefined'
    };
    
    console.log('📋 Vérifications des dépendances:');
    Object.entries(checks).forEach(([name, status]) => {
        console.log(`${status ? '✅' : '❌'} ${name}`);
    });
    
    if (Object.values(checks).every(Boolean)) {
        console.log('🚀 Tous les composants sont chargés !');
        
        // Test de la vidéo de bienvenue
        console.log('🎯 Test de la vidéo de bienvenue...');
        
        if (typeof showWelcomeVideo === 'function') {
            showWelcomeVideo(() => {
                console.log('✅ Vidéo de bienvenue terminée avec succès !');
                console.log('➡️  Redirection simulée vers le dashboard');
            });
        } else {
            console.error('❌ Fonction showWelcomeVideo non trouvée');
        }
        
    } else {
        console.error('❌ Certains composants ne sont pas chargés');
        // Essayer le fallback
        testVideoModal();
    }
}

// Test de la modal vidéo directement
function testVideoModal() {
    console.log('🎥 Test de la modal vidéo...');
    
    if (window.videoModal && window.videoModal.showTestVideo) {
        console.log('📺 Lancement de la vidéo de test via videoModal...');
        window.videoModal.showTestVideo();
    } else if (window.showTestWelcomeVideo) {
        console.log('🎨 Lancement de l\'animation de test...');
        window.showTestWelcomeVideo().then(() => {
            console.log('✅ Animation de test terminée !');
        });
    } else {
        console.error('❌ Aucun système de test disponible');
        console.log('🔍 Objets disponibles:', {
            VideoModal: typeof window.VideoModal,
            videoModal: typeof window.videoModal,
            showTestWelcomeVideo: typeof window.showTestWelcomeVideo
        });
    }
}

// Test avec une vraie vidéo (si disponible)
function testRealVideo(videoUrl = '/static/video/welcome.mp4') {
    if (window.videoModal) {
        console.log(`🎥 Test avec vraie vidéo: ${videoUrl}`);
        window.videoModal.show(videoUrl);
    } else {
        console.error('❌ videoModal non disponible');
    }
}

console.log('🧪 Tests de vidéo en cours de chargement...');

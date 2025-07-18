/* Matrix Rain Effect Functions - v2.0 */
console.log('🎬 Matrix.js v2.0 loading...');

let matrixActive = false;
let matrixInterval;

function initMatrix() {
    const matrixBg = document.getElementById('matrix-bg');
    if (!matrixBg) {
        console.error('❌ Matrix background element not found!');
        return;
    }
    
    console.log('✅ Matrix background element found');
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    
    function createMatrixChar() {
        const char = document.createElement('div');
        char.className = 'matrix-char';
        char.textContent = chars[Math.floor(Math.random() * chars.length)];
        char.style.left = Math.random() * 100 + '%';
        char.style.animationDuration = (Math.random() * 3 + 2) + 's';
        matrixBg.appendChild(char);
        
        setTimeout(() => {
            if (char.parentNode) {
                char.parentNode.removeChild(char);
            }
        }, 5000);
    }
    
    if (matrixActive) {
        matrixInterval = setInterval(createMatrixChar, 100);
        console.log('🌧️ Matrix rain interval started');
    }
}

function matrix() {
    console.log('🎯 Matrix function called');
    matrixActive = !matrixActive;
    const matrixBg = document.getElementById('matrix-bg');
    
    if (!matrixBg) {
        console.error('❌ Matrix background element not found in matrix() function!');
        return;
    }
    
    if (matrixActive) {
        matrixBg.style.opacity = '0.15';
        initMatrix();
        console.log('🌧️ Matrix rain activated');
    } else {
        matrixBg.style.opacity = '0.05';
        clearInterval(matrixInterval);
        matrixBg.innerHTML = '';
        console.log('🌧️ Matrix rain deactivated');
    }
}

// Auto-start matrix with low intensity
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, initializing Matrix effects...');
    
    // Vérifier la présence de l'élément matrix-bg
    const matrixBg = document.getElementById('matrix-bg');
    if (matrixBg) {
        console.log('✅ Matrix background element found on page load');
    } else {
        console.error('❌ Matrix background element NOT found on page load');
    }
    
    setTimeout(() => {
        if (!matrixActive) {
            console.log('🎬 Starting auto-matrix effect...');
            matrix();
            setTimeout(() => {
                console.log('🛑 Stopping auto-matrix effect...');
                matrix();
            }, 1000); // Stop after 1 second for subtle effect
        }
    }, 1000);
});

// Konami code effect
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

document.addEventListener('keydown', function(e) {
    konamiCode.push(e.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (JSON.stringify(konamiCode) === JSON.stringify(konamiSequence)) {
        konami();
        konamiCode = [];
    }
});

function konami() {
    document.body.style.animation = 'konami-spin 2s ease-in-out';
    setTimeout(() => {
        document.body.style.animation = '';
    }, 2000);
    console.log('🎮 Konami code activated!');
}

// Glitch effect
function glitch() {
    console.log('⚡ Glitch function called');
    const titles = document.querySelectorAll('h1, h2, .title-glitch');
    console.log(`📝 Found ${titles.length} titles to glitch`);
    
    titles.forEach((title, index) => {
        title.classList.add('glitch-active');
        console.log(`✨ Adding glitch to element ${index + 1}`);
        setTimeout(() => {
            title.classList.remove('glitch-active');
        }, 1000);
    });
    console.log('⚡ Glitch effect activated');
}

// Hack mode
function hack() {
    document.body.classList.toggle('hack-mode');
    const isHackMode = document.body.classList.contains('hack-mode');
    console.log(isHackMode ? '🔴 Hack mode ON' : '🟢 Hack mode OFF');
}

// Enhanced Matrix Rain with multiple effects
function matrixIntensity(level = 1) {
    const matrixBg = document.getElementById('matrix-bg');
    if (!matrixBg) return;
    
    clearInterval(matrixInterval);
    matrixBg.innerHTML = '';
    
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    const intensities = {
        1: { opacity: '0.1', interval: 200, duration: 4 },
        2: { opacity: '0.15', interval: 150, duration: 3 },
        3: { opacity: '0.25', interval: 100, duration: 2.5 },
        4: { opacity: '0.35', interval: 75, duration: 2 },
        5: { opacity: '0.5', interval: 50, duration: 1.5 }
    };
    
    const config = intensities[level] || intensities[1];
    matrixBg.style.opacity = config.opacity;
    
    function createIntenseMatrixChar() {
        const char = document.createElement('div');
        char.className = 'matrix-char';
        char.textContent = chars[Math.floor(Math.random() * chars.length)];
        char.style.left = Math.random() * 100 + '%';
        char.style.animationDuration = (Math.random() * config.duration + 1) + 's';
        char.style.fontSize = (Math.random() * 8 + 12) + 'px';
        matrixBg.appendChild(char);
        
        setTimeout(() => {
            if (char.parentNode) {
                char.parentNode.removeChild(char);
            }
        }, config.duration * 1000);
    }
    
    matrixInterval = setInterval(createIntenseMatrixChar, config.interval);
    matrixActive = true;
    
    console.log(`🌧️ Matrix intensity set to level ${level}`);
}

// Exposer les fonctions globalement
console.log('🔧 Exposing functions globally...');
window.matrix = matrix;
window.glitch = glitch;
window.hack = hack;
window.matrixIntensity = matrixIntensity;
window.konami = konami;

// Test immédiat
console.log('🧪 Testing function exposure:');
console.log('window.matrix:', typeof window.matrix);
console.log('window.glitch:', typeof window.glitch);
console.log('window.hack:', typeof window.hack);

// Test d'un appel simple
console.log('🚀 Matrix.js fully loaded and ready!');

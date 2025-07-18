/* Matrix Rain Effect Functions */
let matrixActive = false;
let matrixInterval;

function initMatrix() {
    const matrixBg = document.getElementById('matrix-bg');
    if (!matrixBg) return;
    
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
    }
}

function matrix() {
    matrixActive = !matrixActive;
    const matrixBg = document.getElementById('matrix-bg');
    
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
    setTimeout(() => {
        if (!matrixActive) {
            matrix();
            setTimeout(() => matrix(), 1000); // Stop after 1 second for subtle effect
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

@keyframes konami-spin {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(360deg); }
}

// Glitch effect
function glitch() {
    const titles = document.querySelectorAll('h1, h2, .title-glitch');
    titles.forEach(title => {
        title.classList.add('glitch-active');
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

// Add CSS for glitch and hack effects
const style = document.createElement('style');
style.textContent = `
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.1;
        pointer-events: none;
    }

    .matrix-char {
        position: absolute;
        color: #00ff41;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        animation: matrix-fall linear infinite;
    }

    @keyframes matrix-fall {
        0% {
            transform: translateY(-100vh);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh);
            opacity: 0;
        }
    }
    
    @keyframes konami-spin {
        0%, 100% { transform: rotate(0deg); }
        50% { transform: rotate(360deg); }
    }
    
    .glitch-active {
        animation: glitch 1s linear infinite;
    }
    
    @keyframes glitch {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-2px); }
        40% { transform: translateX(2px); }
        60% { transform: translateX(-1px); }
        80% { transform: translateX(1px); }
    }
    
    .hack-mode {
        filter: hue-rotate(180deg) contrast(1.2);
    }
    
    .hack-mode .matrix-bg {
        opacity: 0.3 !important;
    }
`;
document.head.appendChild(style);

/**
 * Dashboard Terminal JavaScript Functions
 * Gestion du terminal interactif avec commandes Matrix
 */

// =============================================================================
// Variables globales
// =============================================================================

let isFullscreen = false;

// =============================================================================
// Fonctions du terminal
// =============================================================================

function clearTerminal() {
    const terminal = document.getElementById('terminal-content');
    terminal.innerHTML = `
        <div class="terminal-line">
            <span class="prompt">matrix@dlh:~$</span>
            <span class="command">Terminal cleared</span>
        </div>
        <div class="terminal-line">
            <span class="prompt">matrix@dlh:~$</span>
            <input type="text" id="terminal-input" class="terminal-input" autofocus>
        </div>
    `;
    setupTerminalInput();
}

function showHelp() {
    const terminal = document.getElementById('terminal-content');
    const helpText = `
        <div class="terminal-line">
            <span class="output">Available commands:</span>
        </div>
        <div class="terminal-line">
            <span class="output">  help - Show this help</span>
        </div>
        <div class="terminal-line">
            <span class="output">  clear - Clear terminal</span>
        </div>
        <div class="terminal-line">
            <span class="output">  whoami - Show current user</span>
        </div>
        <div class="terminal-line">
            <span class="output">  date - Show current date</span>
        </div>
        <div class="terminal-line">
            <span class="output">  matrix - Enable Matrix rain</span>
        </div>
        <div class="terminal-line">
            <span class="output">  neo - Enter the Matrix</span>
        </div>
    `;
    terminal.insertAdjacentHTML('beforeend', helpText);
    
    // Add new input line
    const newLine = document.createElement('div');
    newLine.className = 'terminal-line';
    newLine.innerHTML = `
        <span class="prompt">matrix@dlh:~$</span>
        <input type="text" id="terminal-input" class="terminal-input" autofocus>
    `;
    terminal.appendChild(newLine);
    
    // Focus on new input
    document.getElementById('terminal-input').focus();
    setupTerminalInput();
}

function matrixRain() {
    const terminal = document.getElementById('terminal-content');
    let rainActive = terminal.classList.contains('matrix-rain-active');
    
    if (rainActive) {
        terminal.classList.remove('matrix-rain-active');
        const rainElements = terminal.querySelectorAll('.matrix-rain-char');
        rainElements.forEach(el => el.remove());
        return;
    }
    
    terminal.classList.add('matrix-rain-active');
    
    const matrixChars = '日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗﾈﾄﾖﾀﾇｿﾍﾞﾌｺｴﾁ';
    const numColumns = Math.floor(terminal.offsetWidth / 15);
    
    for (let i = 0; i < numColumns; i++) {
        setTimeout(() => {
            createMatrixColumn(i * 15, matrixChars);
        }, i * 100);
    }
    
    setTimeout(() => {
        if (terminal.classList.contains('matrix-rain-active')) {
            matrixRain();
        }
    }, 10000);
}

function createMatrixColumn(x, chars) {
    const terminal = document.getElementById('terminal-content');
    const column = document.createElement('div');
    column.className = 'matrix-rain-char';
    column.style.cssText = `
        position: absolute;
        left: ${x}px;
        top: -20px;
        color: #00ff41;
        font-family: monospace;
        font-size: 14px;
        opacity: 0.7;
        z-index: 1000;
        pointer-events: none;
        animation: matrix-fall 3s linear infinite;
    `;
    
    let charStr = '';
    for (let i = 0; i < 20; i++) {
        charStr += chars[Math.floor(Math.random() * chars.length)] + '<br>';
    }
    column.innerHTML = charStr;
    
    terminal.appendChild(column);
    
    setTimeout(() => {
        if (column.parentNode) {
            column.remove();
        }
    }, 3000);
}

function setupTerminalInput() {
    const input = document.getElementById('terminal-input');
    if (input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const command = this.value.trim();
                processCommand(command);
                this.value = '';
            }
        });
    }
}

function processCommand(command) {
    const terminal = document.getElementById('terminal-content');
    const currentInput = document.getElementById('terminal-input');
    
    // Show the command that was typed
    if (currentInput && currentInput.parentElement) {
        currentInput.parentElement.innerHTML = `
            <span class="prompt">matrix@dlh:~$</span>
            <span class="command">${command}</span>
        `;
    }
    
    let response = '';
    switch(command.toLowerCase()) {
        case 'help':
            showHelp();
            return;
        case 'clear':
            clearTerminal();
            return;
        case 'whoami':
            response = window.currentUser || 'anonymous';
            break;
        case 'date':
            response = new Date().toLocaleString();
            break;
        case 'matrix':
            response = 'Entering the Matrix...';
            setTimeout(() => matrixRain(), 1000);
            break;
        case 'neo':
            response = 'Wake up, Neo... The Matrix has you...';
            break;
        case 'red pill':
            response = 'Welcome to the real world.';
            break;
        case 'blue pill':
            response = 'The story ends, you wake up in your bed and believe whatever you want to believe.';
            break;
        case '':
            response = '';
            break;
        default:
            response = `Command not found: ${command}. Type 'help' for available commands.`;
    }
    
    // Add response
    if (response) {
        const responseLine = document.createElement('div');
        responseLine.className = 'terminal-line';
        responseLine.innerHTML = `<span class="output">${response}</span>`;
        terminal.appendChild(responseLine);
    }
    
    // Add new input line
    const newLine = document.createElement('div');
    newLine.className = 'terminal-line';
    newLine.innerHTML = `
        <span class="prompt">matrix@dlh:~$</span>
        <input type="text" id="terminal-input" class="terminal-input" autofocus>
    `;
    terminal.appendChild(newLine);
    
    // Setup event listener for new input
    setupTerminalInput();
    
    // Scroll to bottom
    terminal.scrollTop = terminal.scrollHeight;
}

function toggleFullscreen() {
    const terminal = document.getElementById('terminal');
    isFullscreen = !isFullscreen;
    
    if (isFullscreen) {
        terminal.classList.add('fullscreen');
    } else {
        terminal.classList.remove('fullscreen');
    }
}

// =============================================================================
// Initialisation
// =============================================================================

// Initialize terminal when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupTerminalInput();
    
    // CSS pour la pluie Matrix
    if (!document.querySelector('#matrix-rain-styles')) {
        const style = document.createElement('style');
        style.id = 'matrix-rain-styles';
        style.textContent = `
            @keyframes matrix-fall {
                0% { transform: translateY(-20px); opacity: 1; }
                100% { transform: translateY(400px); opacity: 0; }
            }
            .matrix-rain-active {
                position: relative;
                overflow: hidden;
            }
        `;
        document.head.appendChild(style);
    }
});

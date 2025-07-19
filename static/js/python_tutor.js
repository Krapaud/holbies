/**
 * Python Tutor JavaScript Functions
 * Intégration Matrix avec le système de visualisation de code
 */

// =============================================================================
// Classe principale du Python Tutor Matrix
// =============================================================================

class MatrixPythonTutor {
    constructor() {
        this.currentLanguage = 'python';
        this.trace = [];
        this.currentStep = 0;
        this.examples = {
            'python-basic': {
                code: `x = 5\ny = 10\nz = x + y\nprint(f'La somme est: {z}')\n\nfor i in range(3):\n    print(f'Iteration {i}')\n\nnumbers = [1, 2, 3, 4, 5]\ntotal = sum(numbers)\nprint(f'Total: {total}')`,
                language: 'python'
            },
            'python-advanced': {
                code: `def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nresult = fibonacci(5)\nprint(f'Fibonacci(5) = {result}')\n\nnumbers = [1, 2, 3, 4, 5]\nsquares = [x**2 for x in numbers]\nprint(f'Carrés: {squares}')`,
                language: 'python'
            },
            'javascript-basic': {
                code: `let x = 5;\nlet y = 10;\nlet z = x + y;\nconsole.log(\`La somme est: \${z}\`);\n\nfor(let i = 0; i < 3; i++) {\n    console.log(\`Iteration \${i}\`);\n}\n\nconst numbers = [1, 2, 3, 4, 5];\nconst total = numbers.reduce((sum, num) => sum + num, 0);\nconsole.log(\`Total: \${total}\`);`,
                language: 'javascript'
            },
            'c-basic': {
                code: `int x = 5;\nint y = 10;\nint z = x + y;\nprintf("La somme est: %d\\n", z);\n\nfor(int i = 0; i < 3; i++) {\n    printf("Iteration %d\\n", i);\n}\n\nint numbers[] = {1, 2, 3, 4, 5};\nint total = 0;\nfor(int i = 0; i < 5; i++) {\n    total += numbers[i];\n}\nprintf("Total: %d\\n", total);`,
                language: 'c'
            }
        };
        
        this.initializeUI();
    }
    
    initializeUI() {
        // Éléments DOM
        this.codeInput = document.getElementById('code-input');
        this.languageSelect = document.getElementById('language-select');
        this.runButton = document.getElementById('run-button');
        this.clearButton = document.getElementById('clear-button');
        this.exampleButton = document.getElementById('example-button');
        this.traceOutput = document.getElementById('trace-output');
        this.errorOutput = document.getElementById('error-output');
        this.languageIndicator = document.getElementById('language-indicator');
        this.linesCounter = document.getElementById('lines-counter');
        this.stepPrev = document.getElementById('step-prev');
        this.stepNext = document.getElementById('step-next');
        this.stepCounter = document.getElementById('step-counter');
        
        // Événements
        this.runButton.addEventListener('click', () => this.runCode());
        this.clearButton.addEventListener('click', () => this.clearCode());
        this.exampleButton.addEventListener('click', () => this.loadRandomExample());
        this.languageSelect.addEventListener('change', (e) => this.changeLanguage(e.target.value));
        this.codeInput.addEventListener('input', () => this.updateLinesCounter());
        this.stepPrev.addEventListener('click', () => this.previousStep());
        this.stepNext.addEventListener('click', () => this.nextStep());
        
        // Initialisation
        this.updatePlaceholder();
        this.updateLinesCounter();
    }
    
    changeLanguage(language) {
        this.currentLanguage = language;
        this.languageIndicator.textContent = this.getLanguageName(language);
        this.updatePlaceholder();
    }
    
    getLanguageName(language) {
        const names = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'c': 'C'
        };
        return names[language] || language;
    }
    
    updatePlaceholder() {
        const placeholders = {
            'python': '# Entrez votre code Python ici...\\nx = 5\\ny = 10\\nprint(f"Somme: {x + y}")',
            'javascript': '// Entrez votre code JavaScript ici...\\nlet x = 5;\\nlet y = 10;\\nconsole.log(`Somme: ${x + y}`);',
            'c': '// Entrez votre code C ici...\\nint x = 5;\\nint y = 10;\\nprintf("Somme: %d\\\\n", x + y);'
        };
        this.codeInput.placeholder = placeholders[this.currentLanguage];
    }
    
    updateLinesCounter() {
        const lines = this.codeInput.value.split('\\n').length;
        this.linesCounter.textContent = `${lines} ligne${lines > 1 ? 's' : ''}`;
    }
    
    clearCode() {
        this.codeInput.value = '';
        this.traceOutput.innerHTML = this.getWelcomeMessage();
        this.hideError();
        this.updateLinesCounter();
        this.resetSteps();
    }
    
    loadRandomExample() {
        const currentLangExamples = Object.keys(this.examples).filter(key => 
            this.examples[key].language === this.currentLanguage
        );
        
        if (currentLangExamples.length > 0) {
            const randomExample = currentLangExamples[Math.floor(Math.random() * currentLangExamples.length)];
            this.loadExample(randomExample);
        }
    }
    
    loadExample(exampleKey) {
        if (this.examples[exampleKey]) {
            const example = this.examples[exampleKey];
            this.languageSelect.value = example.language;
            this.changeLanguage(example.language);
            this.codeInput.value = example.code;
            this.updateLinesCounter();
        }
    }
    
    async runCode() {
        const code = this.codeInput.value.trim();
        if (!code) {
            this.showError('Veuillez entrer du code à exécuter');
            return;
        }
        
        this.runButton.disabled = true;
        this.runButton.innerHTML = '<span class="btn-icon">⏳</span> Exécution...';
        this.hideError();
        this.traceOutput.innerHTML = '<div class="loading">🔄 Compilation et exécution en cours...</div>';
        
        try {
            // Simulation pour le moment - à remplacer par l'appel au serveur Python
            await this.simulateExecution(code);
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.runButton.disabled = false;
            this.runButton.innerHTML = '<span class="btn-icon">▶️</span> Exécuter';
        }
    }
    
    async simulateExecution(code) {
        // Appel réel au serveur DLH Tutor via l'API proxy Flask
        try {
            const response = await fetch("/api/tutor/run", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    code: code,
                    language: this.currentLanguage 
                }),
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            this.trace = data.trace || [];
            this.currentStep = 0;
            this.displayTrace();
            
        } catch (error) {
            console.error('Erreur lors de l\'exécution:', error);
            throw error;
        }
    }
    
    displayTrace() {
        if (this.trace.length === 0) {
            this.traceOutput.innerHTML = this.getWelcomeMessage();
            return;
        }
        
        this.updateStepControls();
        this.displayCurrentStep();
    }
    
    displayCurrentStep() {
        if (this.currentStep >= this.trace.length) return;
        
        const step = this.trace[this.currentStep];
        const stepNumber = this.currentStep + 1;
        
        let html = `
            <div class="trace-step">
                <div class="step-header">
                    <span class="step-number">Étape ${stepNumber}</span>
                    <span class="step-line">Ligne ${step.line}</span>
                </div>
        `;
        
        if (Object.keys(step.locals).length > 0 || Object.keys(step.globals).length > 0) {
            html += `
                <div class="variables-section">
                    <div class="variable-group">
                        <div class="variable-title">🔧 Variables Locales</div>
                        ${this.formatVariables(step.locals)}
                    </div>
                    <div class="variable-group">
                        <div class="variable-title">🌐 Variables Globales</div>
                        ${this.formatVariables(step.globals)}
                    </div>
                </div>
            `;
        }
        
        if (step.output) {
            html += `
                <div class="output-section">
                    <div class="output-title">📺 Sortie</div>
                    <div class="output-content">${step.output}</div>
                </div>
            `;
        }
        
        if (step.error) {
            html += `
                <div class="error-section">
                    <strong>❌ Erreur:</strong> ${step.error}
                </div>
            `;
        }
        
        html += `</div>`;
        this.traceOutput.innerHTML = html;
    }
    
    formatVariables(variables) {
        if (!variables || Object.keys(variables).length === 0) {
            return '<div style="color: var(--text-muted); font-style: italic;">Aucune variable</div>';
        }
        
        let html = '';
        Object.entries(variables).forEach(([key, value]) => {
            html += `
                <div class="variable-item">
                    <span class="variable-name">${key}</span>
                    <span class="variable-value">${JSON.stringify(value)}</span>
                </div>
            `;
        });
        
        return html;
    }
    
    updateStepControls() {
        this.stepCounter.textContent = `Étape ${this.currentStep + 1}/${this.trace.length}`;
        this.stepPrev.disabled = this.currentStep <= 0;
        this.stepNext.disabled = this.currentStep >= this.trace.length - 1;
    }
    
    previousStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.displayCurrentStep();
            this.updateStepControls();
        }
    }
    
    nextStep() {
        if (this.currentStep < this.trace.length - 1) {
            this.currentStep++;
            this.displayCurrentStep();
            this.updateStepControls();
        }
    }
    
    resetSteps() {
        this.currentStep = 0;
        this.trace = [];
        this.updateStepControls();
    }
    
    showError(message) {
        this.errorOutput.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span>❌</span>
                <span><strong>Erreur:</strong> ${message}</span>
            </div>
        `;
        this.errorOutput.style.display = 'block';
    }
    
    hideError() {
        this.errorOutput.style.display = 'none';
    }
    
    getWelcomeMessage() {
        return `
            <div class="welcome-message">
                <div class="welcome-icon">🚀</div>
                <h3>Bienvenue dans le DLH Tutor Matrix</h3>
                <p>Écrivez du code et cliquez sur <strong>Exécuter</strong> pour voir la visualisation</p>
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🐍</span>
                        <span>Python avec traçage complet</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">📜</span>
                        <span>JavaScript avec variables</span>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">⚙️</span>
                        <span>C avec compilation</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// =============================================================================
// Fonctions globales
// =============================================================================

// Fonctions globales pour les exemples
function loadExample(exampleKey) {
    if (window.pythonTutor) {
        window.pythonTutor.loadExample(exampleKey);
    }
}

// =============================================================================
// Initialisation
// =============================================================================

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    window.pythonTutor = new MatrixPythonTutor();
});

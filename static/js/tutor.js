class HLHTutor {
    constructor() {
        this.currentLanguage = 'python';
        this.initializeUI();
    }
    
    initializeUI() {
        this.attachEvents();
        this.updatePlaceholder();
    }
    
    attachEvents() {
        const runButton = document.getElementById('run-button');
        const clearButton = document.getElementById('clear-button');
        const languageSelect = document.getElementById('language-select');
        
        runButton.addEventListener('click', () => this.runCode());
        clearButton.addEventListener('click', () => this.clearCode());
        languageSelect.addEventListener('change', (e) => {
            this.currentLanguage = e.target.value;
            this.updatePlaceholder();
        });
    }
    
    updatePlaceholder() {
        const codeInput = document.getElementById('code-input');
        const placeholders = {
            python: `# Code Python
x = 5
y = 10
result = x + y
print(f"La somme de {x} et {y} est {result}")

# Boucle simple
for i in range(3):
    print(f"Iteration {i}")`,
            javascript: `// Code JavaScript
let x = 5;
let y = 10;
let result = x + y;
console.log(`La somme de ${x} et ${y} est ${result}`);

// Boucle simple
for(let i = 0; i < 3; i++) {
    console.log(`Iteration ${i}`);
}`,
            c: `// Code C
#include <stdio.h>

int main() {
    int x = 5;
    int y = 10;
    int result = x + y;
    printf("La somme de %d et %d est %d\n", x, y, result);
    
    // Boucle simple
    for(int i = 0; i < 3; i++) {
        printf("Iteration %d\n", i);
    }
    
    return 0;
}`
        };
        codeInput.placeholder = placeholders[this.currentLanguage];
        if (!codeInput.value.trim()) {
            codeInput.value = placeholders[this.currentLanguage];
        }
    }
    
    clearCode() {
        document.getElementById('code-input').value = '';
        document.getElementById('trace-output').innerHTML = '';
        document.getElementById('error-output').style.display = 'none';
    }
    
    async runCode() {
        const codeInput = document.getElementById('code-input');
        const runButton = document.getElementById('run-button');
        const outputDiv = document.getElementById('trace-output');
        const errorDiv = document.getElementById('error-output');
        
        const code = codeInput.value.trim();
        if (!code) {
            this.showError('Veuillez entrer du code à exécuter');
            return;
        }
        
        runButton.disabled = true;
        runButton.innerHTML = '<span>⏳</span> Exécution...';
        errorDiv.style.display = 'none';
        outputDiv.innerHTML = '<div class="loading">🔄 Exécution en cours...</div>';
        
        try {
            if (!window.holbiesApp || !window.holbiesApp.token) {
                throw new Error('Vous devez être connecté pour utiliser le tuteur');
            }
            
            const response = await fetch('/api/tutor/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${window.holbiesApp.token}`
                },
                body: JSON.stringify({ 
                    code: code, 
                    language: this.currentLanguage 
                })
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Session expirée. Veuillez vous reconnecter.');
                }
                const errorData = await response.json().catch(() => ({ detail: 'Erreur réseau' }));
                throw new Error(errorData.detail || 'Erreur lors de l\'exécution');
            }
            
            const result = await response.json();
            
            if (result.error) {
                throw new Error(result.error);
            }
            
            this.displayResults(result);
            
        } catch (err) {
            console.error('Erreur détaillée:', err);
            this.showError(err.message);
        } finally {
            runButton.disabled = false;
            runButton.innerHTML = '<span>▶️</span> Exécuter';
        }
    }
    
    showError(message) {
        const errorDiv = document.getElementById('error-output');
        errorDiv.innerHTML = `❌ <strong>Erreur:</strong> ${message}`;
        errorDiv.style.display = 'block';
    }
    
    displayResults(result) {
        const outputDiv = document.getElementById('trace-output');
        
        let html = `<h3>📊 Résultats d'exécution (${this.currentLanguage.toUpperCase()})</h3>`;
        
        if (result.output) {
            html += `
                <div class="trace-step">
                    <h4>📤 Sortie du programme</h4>
                    <pre class="output-pre success-output">${result.output}</pre>
                </div>
            `;
        }
        
        if (result.error) {
            html += `
                <div class="trace-step">
                    <h4>❌ Erreur d'exécution</h4>
                    <pre class="output-pre error-output">${result.error}</pre>
                </div>
            `;
        }
        
        if (result.trace && result.trace.length > 0) {
            html += `
                <div class="trace-step">
                    <h4>🔍 Trace d'exécution</h4>
                    <div style="max-height: 300px; overflow-y: auto;">
            `;
            result.trace.forEach((step, index) => {
                html += `
                    <div style="border: 1px solid #e2e8f0; margin: 0.5rem 0; padding: 0.5rem; border-radius: 4px;">
                        <strong>Étape ${index + 1}:</strong>
                        <pre class="output-pre" style="margin: 0.25rem 0; font-size: 0.9rem;">${JSON.stringify(step, null, 2)}</pre>
                    </div>
                `;
            });
            html += `
                    </div>
                </div>
            `;
        }
        
        if (!result.output && !result.error && (!result.trace || result.trace.length === 0)) {
            html += '<div class="loading">🤔 Aucun résultat disponible</div>';
        }
        
        outputDiv.innerHTML = html;
    }
    
    setLanguage(language) {
        this.currentLanguage = language;
        document.getElementById('language-select').value = language;
        this.updatePlaceholder();
    }
    
    setCode(code) {
        document.getElementById('code-input').value = code;
    }
}

function loadPythonExample() {
    const code = `# Exemple Python - Calculs et structures de données
x = 5
y = 10
z = x + y
print(f'La somme est: {z}')

# Boucle avec liste
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total += num
    print(f'Ajout de {num}, total: {total}')

print(f'Somme totale: {total}')

# Fonction récursive
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(6)
print(f'Fibonacci(6) = {result}')`;
    
    window.hlhTutor.setLanguage('python');
    window.hlhTutor.setCode(code);
}

function loadJavaScriptExample() {
    const code = `// Exemple JavaScript - Manipulation de tableaux
let x = 5;
let y = 10;
let z = x + y;
console.log(`La somme est: ${z}`);

// Boucle avec tableau
const numbers = [1, 2, 3, 4, 5];
let total = 0;
for(let i = 0; i < numbers.length; i++) {
    total += numbers[i];
    console.log(`Ajout de ${numbers[i]}, total: ${total}`);
}

console.log(`Somme totale: ${total}`);

// Fonction récursive
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

const result = fibonacci(6);
console.log(`Fibonacci(6) = ${result}`);`;
    
    window.hlhTutor.setLanguage('javascript');
    window.hlhTutor.setCode(code);
}

function loadCExample() {
    const code = `// Exemple C - Structures de contrôle et tableaux
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    int x = 5;
    int y = 10;
    int z = x + y;
    printf("La somme est: %d\n", z);
    
    // Tableau et boucle
    int numbers[] = {1, 2, 3, 4, 5};
    int total = 0;
    int size = sizeof(numbers) / sizeof(numbers[0]);
    
    for(int i = 0; i < size; i++) {
        total += numbers[i];
        printf("Ajout de %d, total: %d\n", numbers[i], total);
    }
    
    printf("Somme totale: %d\n", total);
    
    // Fonction récursive
    int result = fibonacci(6);
    printf("Fibonacci(6) = %d\n", result);
    
    return 0;
}`;
    
    window.hlhTutor.setLanguage('c');
    window.hlhTutor.setCode(code);
}

document.addEventListener('DOMContentLoaded', () => {
    window.hlhTutor = new HLHTutor();
});

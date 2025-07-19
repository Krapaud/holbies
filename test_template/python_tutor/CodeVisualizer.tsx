// CodeVisualizer.ts - Visualiseur de code Multi-Langages
// Supporte Python, JavaScript et C

interface TraceStep {
  line: number;
  locals: Record<string, any>;
  globals: Record<string, any>;
  output: string;
  error?: string;
}

interface ApiResponse {
  trace: TraceStep[];
  error?: string;
}

interface LanguageConfig {
  name: string;
  extension: string;
  placeholder: string;
  example: string;
}

class CodeVisualizer {
  private trace: TraceStep[] = [];
  private container: HTMLElement | null = null;
  private codeInput: HTMLTextAreaElement | null = null;
  private languageSelect: HTMLSelectElement | null = null;
  private runButton: HTMLButtonElement | null = null;
  private outputDiv: HTMLElement | null = null;
  private errorDiv: HTMLElement | null = null;
  private currentLanguage: string = 'python';

  private languages: Record<string, LanguageConfig> = {
    python: {
      name: 'Python',
      extension: '.py',
      placeholder: '# Entrez votre code Python ici...\nx = 5\ny = 10\nprint(f"Somme: {x + y}")',
      example: 'x = 5\ny = 10\nz = x + y\nprint(f"La somme est: {z}")'
    },
    javascript: {
      name: 'JavaScript',
      extension: '.js',
      placeholder: '// Entrez votre code JavaScript ici...\nlet x = 5;\nlet y = 10;\nconsole.log(`Somme: ${x + y}`);',
      example: 'let x = 5;\nlet y = 10;\nlet z = x + y;\nconsole.log(`La somme est: ${z}`);\n\nfor(let i = 0; i < 3; i++) {\n    console.log(`Iteration: ${i}`);\n}'
    },
    c: {
      name: 'C',
      extension: '.c',
      placeholder: '// Entrez votre code C ici...\nint x = 5;\nint y = 10;\nprintf("Somme: %d\\n", x + y);',
      example: 'int x = 5;\nint y = 10;\nint z = x + y;\nprintf("La somme est: %d\\n", z);\n\nfor(int i = 0; i < 3; i++) {\n    printf("Iteration: %d\\n", i);\n}'
    }
  };

  constructor(containerId: string) {
    this.container = document.getElementById(containerId);
    if (this.container) {
      this.initializeUI();
    }
  }

  private initializeUI(): void {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="code-visualizer">
        <div class="toolbar">
          <div class="language-selector">
            <label for="language-select">🔧 Langage:</label>
            <select id="language-select">
              <option value="python">🐍 Python</option>
              <option value="javascript">📜 JavaScript</option>
              <option value="c">⚙️ C</option>
            </select>
          </div>
          <button id="run-button" class="run-btn">▶️ Exécuter</button>
          <button id="clear-button" class="clear-btn">🗑️ Effacer</button>
        </div>
        
        <div class="input-section">
          <textarea id="code-input" rows="12" cols="80"></textarea>
        </div>
        
        <div id="error-output" class="error-message" style="display: none;"></div>
        <div id="trace-output" class="trace-visualization"></div>
      </div>
    `;

    this.codeInput = document.getElementById('code-input') as HTMLTextAreaElement;
    this.languageSelect = document.getElementById('language-select') as HTMLSelectElement;
    this.runButton = document.getElementById('run-button') as HTMLButtonElement;
    this.outputDiv = document.getElementById('trace-output') as HTMLElement;
    this.errorDiv = document.getElementById('error-output') as HTMLElement;

    // Événements
    if (this.runButton) {
      this.runButton.addEventListener('click', () => this.runCode());
    }

    if (this.languageSelect) {
      this.languageSelect.addEventListener('change', (e) => {
        this.currentLanguage = (e.target as HTMLSelectElement).value;
        this.updatePlaceholder();
      });
    }

    const clearButton = document.getElementById('clear-button');
    if (clearButton) {
      clearButton.addEventListener('click', () => this.clearCode());
    }

    // Initialiser avec Python
    this.updatePlaceholder();
  }

  private updatePlaceholder(): void {
    if (this.codeInput && this.languages[this.currentLanguage]) {
      this.codeInput.placeholder = this.languages[this.currentLanguage].placeholder;
      
      // Si le textarea est vide, charger l'exemple
      if (!this.codeInput.value.trim()) {
        this.codeInput.value = this.languages[this.currentLanguage].example;
      }
    }
  }

  private clearCode(): void {
    if (this.codeInput) {
      this.codeInput.value = '';
    }
    if (this.outputDiv) {
      this.outputDiv.innerHTML = '';
    }
    this.hideError();
  }

  private async runCode(): Promise<void> {
    if (!this.codeInput || !this.runButton || !this.outputDiv || !this.errorDiv) return;

    const userCode = this.codeInput.value.trim();
    if (!userCode) {
      this.showError('Veuillez entrer du code à exécuter');
      return;
    }

    this.runButton.disabled = true;
    this.runButton.textContent = '⏳ Exécution...';
    this.hideError();
    this.outputDiv.innerHTML = '<div class="loading">🔄 Compilation et exécution en cours...</div>';

    try {
      const res = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          code: userCode,
          language: this.currentLanguage 
        }),
      });

      if (!res.ok) {
        throw new Error(`Erreur HTTP: ${res.status}`);
      }

      const data: ApiResponse = await res.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      this.trace = data.trace || [];
      this.displayTrace();

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Une erreur est survenue';
      this.showError(errorMessage);
      console.error('Erreur lors de l\'exécution du code:', err);
    } finally {
      this.runButton.disabled = false;
      this.runButton.textContent = '▶️ Exécuter';
    }
  }

  private showError(message: string): void {
    if (this.errorDiv) {
      this.errorDiv.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
          <span>❌</span>
          <span><strong>Erreur:</strong> ${message}</span>
        </div>
      `;
      this.errorDiv.style.display = 'block';
    }
  }

  private hideError(): void {
    if (this.errorDiv) {
      this.errorDiv.style.display = 'none';
    }
  }

  private displayTrace(): void {
    if (!this.outputDiv) return;

    if (this.trace.length === 0) {
      this.outputDiv.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: #718096;">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🤔</div>
          <p>Aucune trace d'exécution disponible.</p>
        </div>
      `;
      return;
    }

    const languageName = this.languages[this.currentLanguage]?.name || this.currentLanguage;
    let html = `
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1.5rem;">
        <span style="font-size: 1.5rem;">📊</span>
        <h3 style="margin: 0;">Résultat d'exécution ${languageName}</h3>
      </div>
    `;
    
    this.trace.forEach((step, index) => {
      const stepNumber = index + 1;
      const hasError = step.error && step.error.trim();
      const hasOutput = step.output && step.output.trim();
      const hasLocals = step.locals && Object.keys(step.locals).length > 0;

      html += `
        <div class="trace-step" style="border: 1px solid #e2e8f0; border-radius: 8px; margin: 1rem 0; padding: 1rem; background: #f7fafc;">
          <h4 style="margin: 0 0 1rem 0; color: #4a5568; border-left: 4px solid #667eea; padding-left: 0.5rem;">
            ${this.currentLanguage === 'python' ? `Étape ${stepNumber} - Ligne ${step.line}` : `Résultat d'exécution`}
          </h4>
          
          ${hasError ? `
            <div style="background: #fed7d7; color: #c53030; padding: 1rem; border-radius: 6px; margin: 0.5rem 0; border-left: 4px solid #e53e3e;">
              <strong>❌ Erreur:</strong>
              <pre style="margin-top: 0.5rem; background: none; color: inherit; padding: 0; white-space: pre-wrap;">${step.error}</pre>
            </div>
          ` : ''}
          
          ${hasOutput ? `
            <div style="margin: 0.5rem 0;">
              <strong style="color: #38a169;">📤 Sortie:</strong>
              <pre style="background: #f0fff4; color: #2f855a; border: 1px solid #9ae6b4; padding: 1rem; border-radius: 6px; margin-top: 0.5rem; white-space: pre-wrap;">${step.output}</pre>
            </div>
          ` : ''}
          
          ${hasLocals && this.currentLanguage === 'python' ? `
            <details style="margin-top: 1rem;">
              <summary style="cursor: pointer; font-weight: 600; color: #4a5568; padding: 0.5rem; background: #edf2f7; border-radius: 6px;">
                🔍 Variables (${Object.keys(step.locals).length})
              </summary>
              <div style="margin-top: 0.5rem;">
                ${this.formatVariables(step.locals)}
              </div>
            </details>
          ` : ''}
        </div>
      `;
    });

    this.outputDiv.innerHTML = html;
  }

  private formatVariables(variables: Record<string, any>): string {
    if (!variables || Object.keys(variables).length === 0) {
      return '<p style="color: #718096; font-style: italic;">Aucune variable</p>';
    }

    let html = '<div style="display: grid; gap: 0.5rem;">';
    
    Object.entries(variables).forEach(([key, value]) => {
      // Filtrer les variables internes
      if (key.startsWith('__') || key === 'trace' || key === 'output') return;
      
      let displayValue: string;
      let valueType: string;
      
      if (value === null || value === undefined) {
        displayValue = 'None';
        valueType = 'null';
      } else if (typeof value === 'string') {
        displayValue = `"${value}"`;
        valueType = 'string';
      } else if (typeof value === 'number') {
        displayValue = String(value);
        valueType = 'number';
      } else if (typeof value === 'boolean') {
        displayValue = String(value);
        valueType = 'boolean';
      } else if (Array.isArray(value)) {
        displayValue = JSON.stringify(value, null, 2);
        valueType = 'list';
      } else if (typeof value === 'object') {
        displayValue = JSON.stringify(value, null, 2);
        valueType = 'object';
      } else {
        displayValue = String(value);
        valueType = 'unknown';
      }

      const typeColors: Record<string, string> = {
        'string': '#d69e2e',
        'number': '#3182ce',
        'boolean': '#805ad5',
        'null': '#718096',
        'list': '#38a169',
        'object': '#d53f8c',
        'unknown': '#4a5568'
      };

      const typeColor = typeColors[valueType] || '#4a5568';

      html += `
        <div style="background: #f7fafc; padding: 0.75rem; border-radius: 6px; border-left: 3px solid ${typeColor};">
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
            <span style="font-weight: 600; color: #2d3748;">${key}</span>
            <span style="background: ${typeColor}; color: white; padding: 0.125rem 0.375rem; border-radius: 3px; font-size: 0.75rem;">
              ${valueType}
            </span>
          </div>
          <pre style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #4a5568; background: none; padding: 0; white-space: pre-wrap;">${displayValue}</pre>
        </div>
      `;
    });
    
    html += '</div>';
    return html;
  }

  // Méthode pour usage direct sans interface
  public async executeCode(code: string, language: string = 'python'): Promise<TraceStep[]> {
    try {
      const res = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
      });

      if (!res.ok) {
        throw new Error(`Erreur HTTP: ${res.status}`);
      }

      const data: ApiResponse = await res.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      return data.trace || [];
    } catch (err) {
      console.error('Erreur lors de l\'exécution du code:', err);
      throw err;
    }
  }

  // Méthode pour changer de langage par programmation
  public setLanguage(language: string): void {
    if (this.languages[language] && this.languageSelect) {
      this.currentLanguage = language;
      this.languageSelect.value = language;
      this.updatePlaceholder();
    }
  }

  // Méthode pour obtenir le langage actuel
  public getCurrentLanguage(): string {
    return this.currentLanguage;
  }
}

// Export pour utilisation en module
export default CodeVisualizer;

// Si utilisé dans un contexte global
if (typeof window !== 'undefined') {
  (window as any).CodeVisualizer = CodeVisualizer;
}

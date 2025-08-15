// Amélioration de l'éditeur de code pour le Coding Lab
class SimpleCodeEditor {
    constructor(textareaId) {
        this.textarea = document.getElementById(textareaId);
        this.init();
    }

    init() {
        if (!this.textarea) return;

        // Configuration de base
        this.textarea.addEventListener('input', this.handleInput.bind(this));
        this.textarea.addEventListener('keydown', this.handleKeyDown.bind(this));
        this.textarea.addEventListener('scroll', this.handleScroll.bind(this));

        // Appliquer la coloration initiale
        this.updateSyntaxHighlighting();

        // Créer l'overlay pour la coloration syntaxique
        this.createSyntaxOverlay();
    }

    createSyntaxOverlay() {
        const container = this.textarea.parentNode;
        container.style.position = 'relative';

        // Créer l'overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'syntax-overlay';
        this.overlay.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.5;
            padding: 1.5rem;
            overflow: hidden;
            z-index: 1;
            background: transparent;
            color: transparent;
        `;

        container.insertBefore(this.overlay, this.textarea);

        // Mettre le textarea au premier plan
        this.textarea.style.position = 'relative';
        this.textarea.style.zIndex = '2';
        this.textarea.style.background = 'transparent';
    }

    handleInput(event) {
        this.updateSyntaxHighlighting();
    }

    handleKeyDown(event) {
        // Support des tabulations
        if (event.key === 'Tab') {
            event.preventDefault();
            const start = this.textarea.selectionStart;
            const end = this.textarea.selectionEnd;
            
            // Ajouter 4 espaces
            const value = this.textarea.value;
            this.textarea.value = value.substring(0, start) + '    ' + value.substring(end);
            
            // Replacer le curseur
            this.textarea.selectionStart = this.textarea.selectionEnd = start + 4;
            
            this.updateSyntaxHighlighting();
        }

        // Auto-indentation sur Entrée
        if (event.key === 'Enter') {
            setTimeout(() => {
                const lines = this.textarea.value.split('\n');
                const currentLineIndex = this.textarea.value.substring(0, this.textarea.selectionStart).split('\n').length - 1;
                const previousLine = lines[currentLineIndex - 1];
                
                if (previousLine) {
                    // Calculer l'indentation de la ligne précédente
                    const indent = previousLine.match(/^\s*/)[0];
                    let newIndent = indent;
                    
                    // Ajouter une indentation supplémentaire après :
                    if (previousLine.trim().endsWith(':')) {
                        newIndent += '    ';
                    }
                    
                    if (newIndent) {
                        const start = this.textarea.selectionStart;
                        const value = this.textarea.value;
                        this.textarea.value = value.substring(0, start) + newIndent + value.substring(start);
                        this.textarea.selectionStart = this.textarea.selectionEnd = start + newIndent.length;
                    }
                }
                
                this.updateSyntaxHighlighting();
            }, 10);
        }
    }

    handleScroll() {
        if (this.overlay) {
            this.overlay.scrollTop = this.textarea.scrollTop;
            this.overlay.scrollLeft = this.textarea.scrollLeft;
        }
    }

    updateSyntaxHighlighting() {
        if (!this.overlay) return;

        const code = this.textarea.value;
        const highlighted = this.highlightPython(code);
        this.overlay.innerHTML = highlighted;
    }

    highlightPython(code) {
        // Mots-clés Python
        const keywords = [
            'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally',
            'import', 'from', 'as', 'return', 'yield', 'pass', 'break', 'continue',
            'and', 'or', 'not', 'in', 'is', 'lambda', 'with', 'assert', 'del', 'global', 'nonlocal'
        ];

        const builtins = [
            'print', 'len', 'range', 'list', 'dict', 'set', 'tuple', 'str', 'int', 'float',
            'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr', 'max', 'min', 'sum'
        ];

        let highlighted = code;

        // Échapper le HTML
        highlighted = highlighted.replace(/[<>&]/g, function(match) {
            return {
                '<': '&lt;',
                '>': '&gt;',
                '&': '&amp;'
            }[match];
        });

        // Commentaires
        highlighted = highlighted.replace(/(#.*$)/gm, '<span style="color: #6A9955; font-style: italic;">$1</span>');

        // Chaînes de caractères
        highlighted = highlighted.replace(/("([^"\\]|\\.)*"|'([^'\\]|\\.)*')/g, '<span style="color: #CE9178;">$1</span>');

        // F-strings
        highlighted = highlighted.replace(/(f"([^"\\]|\\.)*"|f'([^'\\]|\\.)*')/g, '<span style="color: #D7BA7D;">$1</span>');

        // Nombres
        highlighted = highlighted.replace(/\b(\d+\.?\d*)\b/g, '<span style="color: #B5CEA8;">$1</span>');

        // Mots-clés
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            highlighted = highlighted.replace(regex, `<span style="color: #569CD6; font-weight: bold;">${keyword}</span>`);
        });

        // Fonctions built-in
        builtins.forEach(builtin => {
            const regex = new RegExp(`\\b${builtin}\\b(?=\\s*\\()`, 'g');
            highlighted = highlighted.replace(regex, `<span style="color: #DCDCAA;">${builtin}</span>`);
        });

        // Opérateurs
        highlighted = highlighted.replace(/(\+|\-|\*|\/|\/\/|%|\*\*|==|!=|<=|>=|<|>|=)/g, '<span style="color: #D4D4D4;">$1</span>');

        return highlighted;
    }
}

// Simulateur d'exécution Python amélioré
class PythonSimulator {
    constructor() {
        this.variables = {};
        this.output = [];
        this.errors = [];
    }

    reset() {
        this.variables = {};
        this.output = [];
        this.errors = [];
    }

    execute(code) {
        this.reset();
        
        try {
            const lines = code.split('\n');
            
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i].trim();
                if (!line || line.startsWith('#')) continue;
                
                this.executeLine(line, i + 1);
            }
            
            return {
                success: true,
                output: this.output.join('\n'),
                variables: this.variables,
                errors: this.errors
            };
        } catch (error) {
            return {
                success: false,
                output: this.output.join('\n'),
                error: error.message,
                variables: this.variables,
                errors: this.errors
            };
        }
    }

    executeLine(line, lineNumber) {
        try {
            // Assignation de variables
            if (line.includes(' = ') && !line.startsWith('print(')) {
                this.handleAssignment(line);
            }
            
            // Print statements
            else if (line.startsWith('print(')) {
                this.handlePrint(line);
            }
            
            // Structures de contrôle (simplifié)
            else if (line.startsWith('if ') || line.startsWith('for ') || line.startsWith('while ')) {
                this.output.push(`# Structure de contrôle détectée: ${line}`);
            }
            
        } catch (error) {
            this.errors.push(`Ligne ${lineNumber}: ${error.message}`);
        }
    }

    handleAssignment(line) {
        const [varName, value] = line.split(' = ').map(s => s.trim());
        
        // Évaluer la valeur
        let evaluatedValue;
        
        if (value.startsWith('"') && value.endsWith('"')) {
            // String
            evaluatedValue = value.slice(1, -1);
        } else if (value.startsWith("'") && value.endsWith("'")) {
            // String
            evaluatedValue = value.slice(1, -1);
        } else if (!isNaN(value)) {
            // Number
            evaluatedValue = value.includes('.') ? parseFloat(value) : parseInt(value);
        } else if (value === 'True' || value === 'False') {
            // Boolean
            evaluatedValue = value === 'True';
        } else if (this.variables.hasOwnProperty(value)) {
            // Variable existante
            evaluatedValue = this.variables[value];
        } else {
            // Expression (simplifié)
            evaluatedValue = this.evaluateExpression(value);
        }
        
        this.variables[varName] = evaluatedValue;
    }

    handlePrint(line) {
        const content = line.match(/print\((.*)\)/)[1].trim();
        
        if (content.startsWith('f"') || content.startsWith("f'")) {
            // F-string
            let text = content.slice(2, -1);
            
            // Remplacer les variables dans les {}
            text = text.replace(/\{([^}]+)\}/g, (match, varName) => {
                if (this.variables.hasOwnProperty(varName.trim())) {
                    return this.variables[varName.trim()];
                }
                return match;
            });
            
            this.output.push(text);
        } else if ((content.startsWith('"') && content.endsWith('"')) || 
                   (content.startsWith("'") && content.endsWith("'"))) {
            // String simple
            this.output.push(content.slice(1, -1));
        } else if (this.variables.hasOwnProperty(content)) {
            // Variable
            this.output.push(String(this.variables[content]));
        } else {
            // Expression
            const result = this.evaluateExpression(content);
            this.output.push(String(result));
        }
    }

    evaluateExpression(expr) {
        // Remplacer les variables par leurs valeurs
        let processedExpr = expr;
        
        for (let [varName, value] of Object.entries(this.variables)) {
            const regex = new RegExp(`\\b${varName}\\b`, 'g');
            processedExpr = processedExpr.replace(regex, String(value));
        }
        
        // Évaluation sécurisée (très basique)
        try {
            // Seulement pour les opérations arithmétiques simples
            if (/^[\d\s+\-*/().]+$/.test(processedExpr)) {
                return eval(processedExpr);
            }
        } catch (error) {
            // Retourner l'expression telle quelle si l'évaluation échoue
        }
        
        return processedExpr;
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('code-editor')) {
        window.codeEditor = new SimpleCodeEditor('code-editor');
        window.pythonSimulator = new PythonSimulator();
        console.log('🎯 Éditeur de code initialisé');
    }
});

// Exposer les classes globalement
window.SimpleCodeEditor = SimpleCodeEditor;
window.PythonSimulator = PythonSimulator;

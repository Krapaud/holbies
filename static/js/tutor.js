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
            this.updatePlaceholder(true);
        });
    }
    
    updatePlaceholder(force = false) {
        const codeInput = document.getElementById('code-input');
        const placeholders = {
            python: `# Code Python\nx = 5\ny = 10\nresult = x + y\nprint(f"La somme de {x} et {y} est {result}")\n\n# Boucle simple\nfor i in range(3):\n    print(f"Iteration {i}")`,
            javascript: `// Code JavaScript\nlet x = 5;\nlet y = 10;\nlet result = x + y;\nconsole.log('La somme de ' + x + ' et ' + y + ' est ' + result);\n\n// Boucle simple\nfor(let i = 0; i < 3; i++) {\n    console.log('Iteration ' + i);\n}`,
            c: `// Code C\n#include <stdio.h>\n\nint main() {\n    int x = 5;\n    int y = 10;\n    int result = x + y;\n    printf("La somme de %d et %d est %d\\n", x, y, result);\n    // Boucle simple\n    for(int i = 0; i < 3; i++) {\n        printf("Iteration %d\\n", i);\n    }\n    return 0;\n}`
        };
        codeInput.placeholder = placeholders[this.currentLanguage];
        if (!codeInput.value.trim() || force) {
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
        this.resultTrace = result.trace || [];
        this.resultOutput = result.output || '';
        this.resultError = result.error || '';
        this.currentStep = 0;
        let html = '';
        if (this.resultError) {
            html += `<div class="tutor-error"><h5>❌ Erreur d'exécution</h5><pre>${this.resultError}</pre></div>`;
        }
        let isJSCStepper = false;
        let jsSteps = [];
        if (this.resultTrace && this.resultTrace.length > 0) {
            // Python avancé : stepper complet
            html += `
                <div class="tutor-stepper-controls">
                    <button id="step-first">⏮️ Début</button>
                    <button id="step-prev">◀️ Précédent</button>
                    <button id="step-play">▶️ Lecture</button>
                    <button id="step-pause" style="display:none;">⏸️ Pause</button>
                    <span class="tutor-stepper-indicator" id="step-indicator">Étape 1/${this.resultTrace.length}</span>
                    <button id="step-next">Suivant ▶️</button>
                    <button id="step-last">Fin ⏭️</button>
                    <label style="margin-left:1.5rem;font-size:0.98em;">Vitesse <input id="step-speed" type="range" min="200" max="2000" value="800" step="100" style="vertical-align:middle;"> <span id="step-speed-val">800ms</span></label>
                </div>
                <div class="tutor-stepper-visual" id="stepper-visual"></div>
            `;
        } else if (this.resultOutput && this.resultOutput.includes('JS_TRACE_STEP:')) {
            // JS/C pseudo-stepper : découpe la sortie en étapes
            jsSteps = this.resultOutput.split('JS_TRACE_STEP:').filter(s => s.trim() !== '');
            html += `
                <div class="tutor-stepper-controls">
                    <button id="step-first">⏮️ Début</button>
                    <button id="step-prev">◀️ Précédent</button>
                    <span class="tutor-stepper-indicator" id="step-indicator">Étape 1/${jsSteps.length}</span>
                    <button id="step-next">Suivant ▶️</button>
                    <button id="step-last">Fin ⏭️</button>
                </div>
                <div class="tutor-stepper-visual" id="stepper-visual"></div>
            `;
            isJSCStepper = true;
        } else if (this.resultOutput) {
            html += `<div class="tutor-output"><h5>📤 Sortie du programme</h5><pre>${this.resultOutput}</pre></div>`;
        } else {
            html += '<div class="loading">🤔 Aucun résultat disponible</div>';
        }
        outputDiv.innerHTML = html;
        if (isJSCStepper) {
            this.resultTrace = jsSteps.map((s, i) => ({output: s, step: i+1}));
            this.renderStep(0);
            document.getElementById('step-first').onclick = () => this.gotoStep(0);
            document.getElementById('step-prev').onclick = () => this.gotoStep(this.currentStep - 1);
            document.getElementById('step-next').onclick = () => this.gotoStep(this.currentStep + 1);
            document.getElementById('step-last').onclick = () => this.gotoStep(this.resultTrace.length - 1);
        } else if (this.resultTrace && this.resultTrace.length > 0 && (!this.resultTrace[0].heap || this.resultTrace[0].step)) {
            // Pseudo-stepper JS/C : simple affichage de la sortie étape par étape (legacy fallback)
            this.renderStep(0);
            document.getElementById('step-first').onclick = () => this.gotoStep(0);
            document.getElementById('step-prev').onclick = () => this.gotoStep(this.currentStep - 1);
            document.getElementById('step-next').onclick = () => this.gotoStep(this.currentStep + 1);
            document.getElementById('step-last').onclick = () => this.gotoStep(this.resultTrace.length - 1);
        } else if (this.resultTrace && this.resultTrace.length > 0) {
            // Python : déjà géré plus haut
        }
    }

    gotoStep(idx) {
        if (!this.resultTrace) return;
        if (idx < 0) idx = 0;
        if (idx >= this.resultTrace.length) idx = this.resultTrace.length - 1;
        this.currentStep = idx;
        this.renderStep(idx);
        // Met à jour l'indicateur
        const indicator = document.getElementById('step-indicator');
        if (indicator) indicator.textContent = `Étape ${idx + 1}/${this.resultTrace.length}`;
    }

    renderStep(idx) {
        const step = this.resultTrace[idx];
        const visualDiv = document.getElementById('stepper-visual');
        if (!step || !visualDiv) return;
        const codeInput = document.getElementById('code-input');
        const codeLines = codeInput.value.split('\n');
        let codeHtml = '<div class="tutor-codeview"><pre>';
        // Mode Python avancé (trace avec heap/stack)
        if (step.heap || step.stack || step.locals || step.globals) {
            if (step.heap || step.stack || step.locals || step.globals) {
            let codeHtml = '<div class="tutor-codeview"><pre>';
            codeLines.forEach((line, i) => {
                const isActive = i + 1 === step.lineno;
                codeHtml += `<span class=\"code-line${isActive ? ' active' : ''}\">${(i+1).toString().padStart(3)} | ${line.replace(/</g, '&lt;')}</span>\n`;
            });
            codeHtml += '</pre></div>';

            let varsHtml = '<div class="tutor-vars"><h5>Variables Locales</h5><table>';
            for (const key in step.locals) {
                let value = step.locals[key];
                if (typeof value === 'object' && value !== null && value.ref) {
                    varsHtml += `<tr><td>${key}</td><td><span class=\"ref-link\" data-ref=\"${value.ref}\">${value.ref}</span></td></tr>`;
                } else {
                    varsHtml += `<tr><td>${key}</td><td>${JSON.stringify(value)}</td></tr>`;
                }
            }
            varsHtml += '</table></div>';

            let globalsHtml = '<div class="tutor-globals"><h5>Variables Globales</h5><table>';
            for (const key in step.globals) {
                // Filter out built-in and internal globals for clarity
                if (!key.startsWith('__') && key !== 'sys' && key !== 'os' && key !== 'subprocess' && key !== 'tempfile' && key !== 'json' && key !== 'traceback' && key !== 'io' && key !== 'linecache' && key !== 'redirect_stdout' && key !== 'redirect_stderr' && key !== 'builtins' && key !== 'get_obj_id' && key !== 'extract_heap' && key !== 'tracer' && key !== 'traced_print' && key !== 'safe_globals') {
                    let value = step.globals[key];
                    if (typeof value === 'object' && value !== null && value.ref) {
                        globalsHtml += `<tr><td>${key}</td><td><span class=\"ref-link\" data-ref=\"${value.ref}\">${value.ref}</span></td></tr>`;
                    } else {
                        globalsHtml += `<tr><td>${key}</td><td>${JSON.stringify(value)}</td></tr>`;
                    }
                }
            }
            globalsHtml += '</table></div>';

            let stackHtml = '<div class="tutor-stack"><h5>Pile d\'appels</h5>';
            step.stack.forEach(frame => {
                stackHtml += `<div class=\"tutor-stack-frame\"><strong>${frame.function}</strong> (ligne ${frame.lineno})<br/>`;
                for (const key in frame.locals) {
                    let value = frame.locals[key];
                    if (typeof value === 'object' && value !== null && value.ref) {
                        stackHtml += `&nbsp;&nbsp;${key}: <span class=\"ref-link\" data-ref=\"${value.ref}\">${value.ref}</span><br/>`;
                    } else {
                        stackHtml += `&nbsp;&nbsp;${key}: ${JSON.stringify(value)}<br/>`;
                    }
                }
                stackHtml += '</div>';
            });
            stackHtml += '</div>';

            let heapHtml = '<div class="tutor-heap"><h5>Heap</h5><table>';
            for (const objId in step.heap) {
                const obj = step.heap[objId];
                heapHtml += `<tr id=\"${objId}\"><td><strong>${objId}</strong> (${obj.type})</td><td>`;
                if (typeof obj.value === 'object' && obj.value !== null) {
                    heapHtml += JSON.stringify(obj.value, (k, v) => {
                        if (v && v.ref) return v.ref; // Display ref for linked objects
                        return v;
                    }, 2).replace(/\n/g, '<br>').replace(/ /g, '&nbsp;');
                } else {
                    heapHtml += JSON.stringify(obj.value);
                }
                heapHtml += '</td></tr>';
            }
            heapHtml += '</table></div>';

            let outputHtml = '';
            if (step.output) {
                outputHtml = `<div class="tutor-output"><h5>Sortie</h5><pre>${step.output.replace(/</g, '&lt;')}</pre></div>`;
            }

            visualDiv.innerHTML = codeHtml + `<div class=\"tutor-right-panel\">${varsHtml}${globalsHtml}${stackHtml}${heapHtml}</div>` + outputHtml;

            // Add click listeners for ref links
            visualDiv.querySelectorAll('.ref-link').forEach(link => {
                link.addEventListener('click', (e) => {
                    const refId = e.target.dataset.ref;
                    const targetElement = document.getElementById(refId);
                    if (targetElement) {
                        targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        targetElement.classList.add('highlight');
                        setTimeout(() => {
                            targetElement.classList.remove('highlight');
                        }, 1500);
                    }
                });
            });

        } else {
            // Mode JS/C pseudo-stepper : surligne la ligne contenant la sortie de l'étape
            let highlightLine = -1;
            if (step.output && step.output.length < 120) {
                for (let i = 0; i < codeLines.length; i++) {
                    if (codeLines[i].includes(step.output.replace('JS_TRACE_STEP: ','').trim())) {
                        highlightLine = i;
                        break;
                    }
                }
            }
            codeLines.forEach((line, i) => {
                const isActive = i === highlightLine;
                codeHtml += `<span class=\"code-line${isActive ? ' active' : ''}\">${(i+1).toString().padStart(3)} | ${line.replace(/</g, '&lt;')}</span>\n`;
            });
            codeHtml += '</pre></div>';
            let outputHtml = '<div class="tutor-output"><h5>Sortie étape</h5><pre>';
            if (step.output) {
                outputHtml += step.output.replace(/</g, '&lt;');
            }
            outputHtml += '</pre></div>';
            visualDiv.innerHTML = codeHtml + outputHtml;
        }

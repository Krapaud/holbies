/**
 * CODING LAB - JavaScript principal
 * Inspiré de Coddy.tech pour une expérience d'apprentissage moderne
 */

class CodingLabPlatform {
    constructor() {
        this.currentExercise = 1;
        this.exercises = [];
        this.userProgress = {
            completedExercises: [],
            points: 0,
            streak: 0,
            level: 1
        };
        this.codeEditor = null;
        this.isInitialized = false;
        
        // Configuration des langages
        this.languages = {
            python: {
                name: 'Python',
                mode: 'python',
                template: '# Écrivez votre code Python ici\n\n',
                runner: this.runPython.bind(this)
            },
            javascript: {
                name: 'JavaScript',
                mode: 'javascript',
                template: '// Écrivez votre code JavaScript ici\n\n',
                runner: this.runJavaScript.bind(this)
            },
            html: {
                name: 'HTML',
                mode: 'xml',
                template: '<!DOCTYPE html>\n<html>\n<head>\n    <title>Mon exercice</title>\n</head>\n<body>\n    <!-- Votre code HTML ici -->\n</body>\n</html>',
                runner: this.runHTML.bind(this)
            }
        };
        
        this.currentLanguage = 'python';
        this.loadExercises();
    }

    async init() {
        if (this.isInitialized) return;
        
        console.log('🚀 Initialisation du Coding Lab...');
        
        try {
            await this.setupCodeEditor();
            this.setupEventListeners();
            this.loadUserProgress();
            this.renderExerciseList();
            this.loadExercise(this.currentExercise);
            this.updateProgressDisplay();
            
            this.isInitialized = true;
            console.log('✅ Coding Lab initialisé avec succès');
            
            // Afficher un message de bienvenue
            this.showNotification('success', 'Bienvenue dans le Coding Lab !', 'Commencez votre apprentissage interactif de la programmation.');
            
        } catch (error) {
            console.error('❌ Erreur lors de l\'initialisation:', error);
            this.showNotification('error', 'Erreur d\'initialisation', 'Impossible de charger le Coding Lab. Rechargez la page.');
        }
    }

    loadExercises() {
        this.exercises = [
            {
                id: 1,
                title: 'Variables et Types',
                difficulty: 'easy',
                timeEstimate: '5 min',
                points: 50,
                language: 'python',
                description: `
                    <h4>🎯 Objectif</h4>
                    <p>Apprendre à créer et utiliser des variables en Python.</p>
                    
                    <h4>📋 Instructions</h4>
                    <ol>
                        <li>Créez une variable <code>nom</code> avec votre nom</li>
                        <li>Créez une variable <code>age</code> avec votre âge</li>
                        <li>Créez une variable <code>ville</code> avec votre ville</li>
                        <li>Affichez ces informations avec des messages formatés</li>
                    </ol>
                `,
                requirements: [
                    'Utiliser au moins 3 variables',
                    'Utiliser print() pour afficher',
                    'Utiliser des f-strings pour le formatage'
                ],
                starter: `# Exercice 1: Variables et Types
# Créez vos variables ici

nom = "Votre nom"
age = 25
ville = "Votre ville"

# Affichez vos informations
print(f"Bonjour, je m'appelle {nom}")
print(f"J'ai {age} ans")
print(f"J'habite à {ville}")

# Bonus: Calculez votre année de naissance
annee_actuelle = 2025
annee_naissance = annee_actuelle - age
print(f"Je suis né(e) en {annee_naissance}")`,
                solution: `nom = "Alice Dupont"
age = 25
ville = "Paris"

print(f"Bonjour, je m'appelle {nom}")
print(f"J'ai {age} ans")
print(f"J'habite à {ville}")

annee_actuelle = 2025
annee_naissance = annee_actuelle - age
print(f"Je suis né(e) en {annee_naissance}")`,
                tests: [
                    { name: 'Variable nom définie', test: (code) => code.includes('nom =') },
                    { name: 'Variable age définie', test: (code) => code.includes('age =') },
                    { name: 'Variable ville définie', test: (code) => code.includes('ville =') },
                    { name: 'Utilisation de print()', test: (code) => code.includes('print(') },
                    { name: 'Utilisation de f-strings', test: (code) => code.includes('f"') || code.includes("f'") }
                ],
                hints: [
                    "💡 Utilisez des guillemets pour les chaînes de caractères",
                    "💡 Les f-strings permettent d'insérer des variables: f'Bonjour {nom}'",
                    "💡 Vous pouvez faire des calculs avec les variables numériques"
                ]
            },
            {
                id: 2,
                title: 'Conditions et Logique',
                difficulty: 'easy',
                timeEstimate: '8 min',
                points: 75,
                language: 'python',
                description: `
                    <h4>🎯 Objectif</h4>
                    <p>Apprendre les structures conditionnelles if/elif/else.</p>
                    
                    <h4>📋 Instructions</h4>
                    <ol>
                        <li>Demandez l'âge de l'utilisateur</li>
                        <li>Affichez un message selon l'âge (enfant, ado, adulte, senior)</li>
                        <li>Gérez les cas d'erreur (âge négatif)</li>
                    </ol>
                `,
                requirements: [
                    'Utiliser if/elif/else',
                    'Gérer plusieurs conditions',
                    'Afficher des messages appropriés'
                ],
                starter: `# Exercice 2: Conditions et Logique
# Demandez l'âge et affichez une catégorie

age = int(input("Quel est votre âge ? "))

# Ajoutez vos conditions ici
if age < 0:
    print("L'âge ne peut pas être négatif!")
elif age < 13:
    print("Vous êtes un enfant")
# Continuez avec d'autres conditions...`,
                solution: `age = int(input("Quel est votre âge ? "))

if age < 0:
    print("L'âge ne peut pas être négatif!")
elif age < 13:
    print("Vous êtes un enfant")
elif age < 18:
    print("Vous êtes un adolescent")
elif age < 65:
    print("Vous êtes un adulte")
else:
    print("Vous êtes un senior")`,
                tests: [
                    { name: 'Structure if présente', test: (code) => code.includes('if ') },
                    { name: 'Structure elif présente', test: (code) => code.includes('elif ') },
                    { name: 'Structure else présente', test: (code) => code.includes('else:') },
                    { name: 'Gestion âge négatif', test: (code) => code.includes('< 0') },
                    { name: 'Plusieurs conditions', test: (code) => (code.match(/elif/g) || []).length >= 2 }
                ],
                hints: [
                    "💡 Utilisez elif pour plusieurs conditions",
                    "💡 Pensez à gérer les cas d'erreur",
                    "💡 L'ordre des conditions est important"
                ]
            },
            {
                id: 3,
                title: 'Boucles et Répétitions',
                difficulty: 'medium',
                timeEstimate: '10 min',
                points: 100,
                language: 'python',
                description: `
                    <h4>🎯 Objectif</h4>
                    <p>Maîtriser les boucles for et while.</p>
                    
                    <h4>📋 Instructions</h4>
                    <ol>
                        <li>Créez une boucle qui affiche les nombres de 1 à 10</li>
                        <li>Créez une boucle qui calcule la somme des nombres pairs de 1 à 20</li>
                        <li>Utilisez break et continue dans vos boucles</li>
                    </ol>
                `,
                requirements: [
                    'Utiliser une boucle for',
                    'Utiliser une boucle while',
                    'Calculer une somme',
                    'Utiliser break ou continue'
                ],
                starter: `# Exercice 3: Boucles et Répétitions

# 1. Afficher les nombres de 1 à 10
print("Nombres de 1 à 10:")
for i in range(1, 11):
    print(i)

# 2. Calculer la somme des nombres pairs de 1 à 20
somme_pairs = 0
# Votre code ici

print(f"Somme des nombres pairs: {somme_pairs}")

# 3. Boucle avec break/continue
# Votre code ici`,
                solution: `# 1. Afficher les nombres de 1 à 10
print("Nombres de 1 à 10:")
for i in range(1, 11):
    print(i)

# 2. Calculer la somme des nombres pairs de 1 à 20
somme_pairs = 0
for i in range(1, 21):
    if i % 2 == 0:
        somme_pairs += i

print(f"Somme des nombres pairs: {somme_pairs}")

# 3. Boucle avec break/continue
print("Nombres de 1 à 20, sauf multiples de 3:")
for i in range(1, 21):
    if i % 3 == 0:
        continue
    if i > 15:
        break
    print(i)`,
                tests: [
                    { name: 'Boucle for présente', test: (code) => code.includes('for ') },
                    { name: 'Utilisation de range()', test: (code) => code.includes('range(') },
                    { name: 'Calcul avec modulo', test: (code) => code.includes('% ') },
                    { name: 'Variable de somme', test: (code) => code.includes('somme') },
                    { name: 'Continue ou break', test: (code) => code.includes('continue') || code.includes('break') }
                ],
                hints: [
                    "💡 Utilisez range(1, 11) pour les nombres de 1 à 10",
                    "💡 Le modulo (%) vous aide à trouver les nombres pairs",
                    "💡 continue passe à l'itération suivante, break sort de la boucle"
                ]
            }
        ];
    }

    async setupCodeEditor() {
        const editorElement = document.getElementById('code-editor');
        if (!editorElement) {
            throw new Error('Élément code-editor non trouvé');
        }

        // Pour cette version, on utilise un textarea simple avec coloration syntaxique basique
        // Dans une version plus avancée, on pourrait intégrer CodeMirror ou Monaco Editor
        editorElement.style.fontFamily = "'Fira Code', 'Monaco', 'Menlo', monospace";
        editorElement.style.fontSize = '14px';
        editorElement.style.lineHeight = '1.6';
        
        // Ajout de la coloration syntaxique basique et de l'auto-indentation
        this.addCodeEditorFeatures(editorElement);
        
        this.codeEditor = editorElement;
        console.log('✅ Éditeur de code configuré');
    }

    addCodeEditorFeatures(editor) {
        // Auto-indentation
        editor.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                
                editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
                editor.selectionStart = editor.selectionEnd = start + 4;
            }
            
            // Auto-indentation sur Enter
            if (e.key === 'Enter') {
                const lines = editor.value.substring(0, editor.selectionStart).split('\n');
                const currentLine = lines[lines.length - 1];
                const indentMatch = currentLine.match(/^(\s*)/);
                const currentIndent = indentMatch ? indentMatch[1] : '';
                
                // Ajouter une indentation supplémentaire après :
                const extraIndent = currentLine.trim().endsWith(':') ? '    ' : '';
                
                setTimeout(() => {
                    const start = editor.selectionStart;
                    editor.value = editor.value.substring(0, start) + currentIndent + extraIndent + editor.value.substring(start);
                    editor.selectionStart = editor.selectionEnd = start + currentIndent.length + extraIndent.length;
                }, 0);
            }
        });

        // Coloration syntaxique basique en temps réel
        editor.addEventListener('input', () => {
            this.highlightSyntax(editor);
        });
    }

    highlightSyntax(editor) {
        // Cette fonction ajoute une coloration syntaxique basique
        // Note: Pour une vraie coloration, il faudrait utiliser une bibliothèque comme CodeMirror
        const code = editor.value;
        
        // Vérification de la syntaxe Python basique
        const pythonKeywords = ['def', 'class', 'if', 'elif', 'else', 'for', 'while', 'import', 'from', 'return', 'try', 'except', 'finally', 'with', 'as', 'and', 'or', 'not', 'in', 'is'];
        const hasKeywords = pythonKeywords.some(keyword => code.includes(keyword));
        
        if (hasKeywords) {
            editor.style.color = '#d4d4d4'; // Couleur de base
        }
    }

    setupEventListeners() {
        // Boutons principaux
        const runBtn = document.getElementById('run-code');
        const submitBtn = document.getElementById('submit-code');
        const formatBtn = document.getElementById('format-code');
        const hintBtn = document.getElementById('hint-btn');
        const solutionBtn = document.getElementById('solution-btn');

        if (runBtn) runBtn.addEventListener('click', () => this.runCode());
        if (submitBtn) submitBtn.addEventListener('click', () => this.submitCode());
        if (formatBtn) formatBtn.addEventListener('click', () => this.formatCode());
        if (hintBtn) hintBtn.addEventListener('click', () => this.showHint());
        if (solutionBtn) solutionBtn.addEventListener('click', () => this.showSolution());

        // Changement de langage
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.switchLanguage(e.target.value);
            });
        }

        // Onglets des résultats
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Fermeture des modals
        const modalCloses = document.querySelectorAll('.modal-close');
        modalCloses.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.closeModal(e.target.closest('.modal'));
            });
        });

        // Bouton de réinitialisation
        const resetBtn = document.getElementById('reset-progress');
        if (resetBtn) resetBtn.addEventListener('click', () => this.resetProgress());

        console.log('✅ Event listeners configurés');
    }

    renderExerciseList() {
        const exerciseList = document.getElementById('exercise-list');
        if (!exerciseList) return;

        exerciseList.innerHTML = '';

        this.exercises.forEach(exercise => {
            const item = document.createElement('div');
            item.className = 'exercise-item';
            
            if (exercise.id === this.currentExercise) {
                item.classList.add('active');
            }
            
            if (this.userProgress.completedExercises.includes(exercise.id)) {
                item.classList.add('completed');
            }

            item.innerHTML = `
                <div class="exercise-title">${exercise.title}</div>
                <div class="exercise-meta">
                    <span class="difficulty ${exercise.difficulty}">${exercise.difficulty}</span>
                    <span class="time-estimate">
                        <i class="fas fa-clock"></i> ${exercise.timeEstimate}
                    </span>
                    <span class="points">
                        <i class="fas fa-star"></i> ${exercise.points}
                    </span>
                </div>
            `;

            item.addEventListener('click', () => {
                this.loadExercise(exercise.id);
            });

            exerciseList.appendChild(item);
        });

        console.log('✅ Liste des exercices rendue');
    }

    loadExercise(exerciseId) {
        const exercise = this.exercises.find(ex => ex.id === exerciseId);
        if (!exercise) {
            console.error(`Exercice ${exerciseId} non trouvé`);
            return;
        }

        this.currentExercise = exerciseId;

        // Mettre à jour l'interface
        this.updateExerciseHeader(exercise);
        this.updateInstructions(exercise);
        this.loadStarterCode(exercise);
        this.updateLanguage(exercise.language);
        this.clearResults();
        this.renderExerciseList(); // Re-render pour mettre à jour l'exercice actif

        console.log(`📚 Exercice ${exerciseId} chargé: ${exercise.title}`);
    }

    updateExerciseHeader(exercise) {
        const title = document.getElementById('exercise-title');
        const difficulty = document.getElementById('exercise-difficulty');
        const timeEstimate = document.getElementById('time-estimate');
        const points = document.getElementById('exercise-points');

        if (title) title.textContent = exercise.title;
        if (difficulty) {
            difficulty.textContent = exercise.difficulty;
            difficulty.className = `difficulty ${exercise.difficulty}`;
        }
        if (timeEstimate) timeEstimate.innerHTML = `<i class="fas fa-clock"></i> ${exercise.timeEstimate}`;
        if (points) points.innerHTML = `<i class="fas fa-star"></i> ${exercise.points} pts`;
    }

    updateInstructions(exercise) {
        const description = document.getElementById('exercise-description');
        const requirements = document.getElementById('requirements');

        if (description) {
            description.innerHTML = exercise.description;
        }

        if (requirements && exercise.requirements) {
            requirements.innerHTML = `
                <h4><i class="fas fa-check-circle"></i> Exigences</h4>
                <ul>
                    ${exercise.requirements.map(req => `<li>${req}</li>`).join('')}
                </ul>
            `;
        }
    }

    loadStarterCode(exercise) {
        if (this.codeEditor && exercise.starter) {
            this.codeEditor.value = exercise.starter;
        }
    }

    updateLanguage(language) {
        this.currentLanguage = language;
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.value = language;
        }
    }

    switchLanguage(language) {
        this.currentLanguage = language;
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (exercise) {
            // Recharger le code de départ pour le nouveau langage
            this.loadStarterCode(exercise);
        }
        console.log(`🔄 Langage changé pour: ${language}`);
    }

    async runCode() {
        const code = this.codeEditor?.value;
        if (!code) {
            this.showNotification('warning', 'Code vide', 'Veuillez écrire du code avant de l\'exécuter.');
            return;
        }

        this.showLoadingState();

        try {
            const language = this.languages[this.currentLanguage];
            if (language && language.runner) {
                const result = await language.runner(code);
                this.displayResults(result);
            } else {
                throw new Error(`Langage ${this.currentLanguage} non supporté`);
            }
        } catch (error) {
            this.displayError(error.message);
        }
    }

    async runPython(code) {
        // Simulateur Python simplifié
        try {
            // Remplacer les input() par des valeurs par défaut pour la démo
            let processedCode = code.replace(/input\([^)]*\)/g, '"25"'); // Âge par défaut
            
            // Variables pour capturer les print()
            let output = '';
            const originalLog = console.log;
            
            // Fonction print simulée
            const print = (text) => {
                output += text + '\n';
            };

            // Fonctions Python simulées
            const pythonFunctions = {
                print,
                int: (x) => parseInt(x),
                str: (x) => String(x),
                len: (x) => x.length,
                range: function(start, stop, step = 1) {
                    const result = [];
                    if (arguments.length === 1) {
                        stop = start;
                        start = 0;
                    }
                    for (let i = start; i < stop; i += step) {
                        result.push(i);
                    }
                    return result;
                }
            };

            // Évaluer le code dans un contexte sécurisé
            const safeEval = new Function(
                'print', 'int', 'str', 'len', 'range',
                `
                try {
                    ${processedCode}
                    return { success: true, output: arguments[5] };
                } catch (error) {
                    return { success: false, error: error.message };
                }
                `
            );

            // Capture de l'output
            let capturedOutput = '';
            const captureOutput = (text) => capturedOutput += text + '\n';

            const result = safeEval(
                captureOutput,
                pythonFunctions.int,
                pythonFunctions.str,
                pythonFunctions.len,
                pythonFunctions.range,
                capturedOutput
            );

            return {
                success: result.success !== false,
                output: capturedOutput || output || 'Code exécuté avec succès',
                error: result.error || null
            };

        } catch (error) {
            return {
                success: false,
                output: '',
                error: error.message
            };
        }
    }

    async runJavaScript(code) {
        try {
            let output = '';
            const originalLog = console.log;
            
            // Rediriger console.log
            console.log = (...args) => {
                output += args.join(' ') + '\n';
            };

            // Exécuter le code
            eval(code);
            
            // Restaurer console.log
            console.log = originalLog;

            return {
                success: true,
                output: output || 'Code exécuté avec succès',
                error: null
            };
        } catch (error) {
            return {
                success: false,
                output: '',
                error: error.message
            };
        }
    }

    async runHTML(code) {
        // Pour HTML, on pourrait ouvrir dans un iframe ou une nouvelle fenêtre
        return {
            success: true,
            output: 'HTML code ready to render. Check the preview.',
            error: null
        };
    }

    displayResults(result) {
        const outputElement = document.getElementById('code-output');
        const testsElement = document.getElementById('test-results');
        const consoleElement = document.getElementById('console-output');

        if (outputElement) {
            if (result.success) {
                outputElement.innerHTML = `<pre class="text-success">${result.output}</pre>`;
            } else {
                outputElement.innerHTML = `<pre class="text-error">❌ Erreur: ${result.error}</pre>`;
            }
        }

        // Afficher les résultats des tests
        this.runTests();
        
        // Switch to output tab
        this.switchTab('output');

        if (result.success) {
            this.showNotification('success', 'Code exécuté !', 'Votre code fonctionne correctement.');
        }
    }

    displayError(error) {
        const outputElement = document.getElementById('code-output');
        if (outputElement) {
            outputElement.innerHTML = `<pre class="text-error">❌ Erreur: ${error}</pre>`;
        }
        this.switchTab('output');
    }

    runTests() {
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (!exercise || !exercise.tests) return;

        const code = this.codeEditor?.value || '';
        const testsElement = document.getElementById('test-results');
        
        if (!testsElement) return;

        let allPassed = true;
        const testResults = exercise.tests.map(test => {
            const passed = test.test(code);
            if (!passed) allPassed = false;
            
            return {
                name: test.name,
                passed: passed
            };
        });

        testsElement.innerHTML = testResults.map(result => `
            <div class="test-case ${result.passed ? 'passed' : 'failed'}">
                <span>${result.name}</span>
                <span class="test-status ${result.passed ? 'passed' : 'failed'}">
                    ${result.passed ? '✅ Réussi' : '❌ Échoué'}
                </span>
            </div>
        `).join('');

        if (allPassed) {
            this.completeExercise();
        }
    }

    submitCode() {
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (!exercise) return;

        const code = this.codeEditor?.value || '';
        
        // Vérifier que le code n'est pas vide
        if (!code.trim()) {
            this.showNotification('warning', 'Code vide', 'Veuillez écrire du code avant de le soumettre.');
            return;
        }

        // Exécuter les tests
        this.runTests();
        
        // Vérifier si tous les tests passent
        const allTestsPassed = this.checkAllTests(code, exercise);
        
        if (allTestsPassed) {
            this.completeExercise();
        } else {
            this.showNotification('warning', 'Tests non réussis', 'Certains tests échouent encore. Vérifiez votre code.');
        }
    }

    checkAllTests(code, exercise) {
        if (!exercise.tests) return true;
        return exercise.tests.every(test => test.test(code));
    }

    completeExercise() {
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (!exercise) return;

        // Marquer comme complété
        if (!this.userProgress.completedExercises.includes(exercise.id)) {
            this.userProgress.completedExercises.push(exercise.id);
            this.userProgress.points += exercise.points;
            this.saveUserProgress();
        }

        // Afficher la notification de succès
        this.showSuccessNotification(exercise);
        
        // Mettre à jour l'affichage
        this.updateProgressDisplay();
        this.renderExerciseList();

        console.log(`🎉 Exercice ${exercise.id} complété!`);
    }

    showSuccessNotification(exercise) {
        const notification = document.getElementById('success-notification');
        const earnedPoints = document.getElementById('earned-points');
        const nextButton = document.getElementById('next-exercise');

        if (notification) {
            if (earnedPoints) earnedPoints.textContent = exercise.points;
            
            if (nextButton) {
                nextButton.onclick = () => {
                    this.hideSuccessNotification();
                    this.loadNextExercise();
                };
            }

            notification.classList.remove('hidden');
        }
    }

    hideSuccessNotification() {
        const notification = document.getElementById('success-notification');
        if (notification) {
            notification.classList.add('hidden');
        }
    }

    loadNextExercise() {
        const nextExerciseId = this.currentExercise + 1;
        if (nextExerciseId <= this.exercises.length) {
            this.loadExercise(nextExerciseId);
        } else {
            this.showNotification('success', 'Félicitations !', 'Vous avez terminé tous les exercices du Coding Lab !');
        }
    }

    showHint() {
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (!exercise || !exercise.hints) return;

        const randomHint = exercise.hints[Math.floor(Math.random() * exercise.hints.length)];
        
        const modal = document.getElementById('hint-modal');
        const content = document.getElementById('hint-content');
        
        if (modal && content) {
            content.innerHTML = `<p>${randomHint}</p>`;
            this.showModal(modal);
        }
    }

    showSolution() {
        const exercise = this.exercises.find(ex => ex.id === this.currentExercise);
        if (!exercise || !exercise.solution) return;

        const modal = document.getElementById('solution-modal');
        const content = document.getElementById('solution-content');
        const showBtn = document.getElementById('show-solution');
        
        if (modal && content && showBtn) {
            showBtn.onclick = () => {
                content.innerHTML = `<pre><code>${exercise.solution}</code></pre>`;
                showBtn.style.display = 'none';
                
                // Réduire les points pour avoir consulté la solution
                this.userProgress.points = Math.max(0, this.userProgress.points - 10);
                this.updateProgressDisplay();
            };
            
            this.showModal(modal);
        }
    }

    formatCode() {
        if (!this.codeEditor) return;
        
        let code = this.codeEditor.value;
        
        // Formatage basique pour Python
        if (this.currentLanguage === 'python') {
            // Corriger l'indentation
            const lines = code.split('\n');
            let indentLevel = 0;
            
            const formattedLines = lines.map(line => {
                const trimmed = line.trim();
                if (!trimmed) return '';
                
                // Réduire l'indentation pour les mots-clés qui ferment des blocs
                if (trimmed.startsWith('elif ') || trimmed.startsWith('else:') || trimmed.startsWith('except ') || trimmed.startsWith('finally:')) {
                    indentLevel = Math.max(0, indentLevel - 1);
                }
                
                const formatted = '    '.repeat(indentLevel) + trimmed;
                
                // Augmenter l'indentation après les deux-points
                if (trimmed.endsWith(':')) {
                    indentLevel++;
                }
                
                return formatted;
            });
            
            this.codeEditor.value = formattedLines.join('\n');
        }
        
        this.showNotification('success', 'Code formaté', 'L\'indentation de votre code a été corrigée.');
    }

    showModal(modal) {
        if (modal) {
            modal.classList.remove('hidden');
        }
    }

    closeModal(modal) {
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    switchTab(tabName) {
        // Désactiver tous les onglets
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        
        // Activer l'onglet sélectionné
        const selectedTab = document.querySelector(`[data-tab="${tabName}"]`);
        const selectedPane = document.getElementById(tabName);
        
        if (selectedTab) selectedTab.classList.add('active');
        if (selectedPane) selectedPane.classList.add('active');
    }

    showLoadingState() {
        const outputElement = document.getElementById('code-output');
        if (outputElement) {
            outputElement.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Exécution du code...</div>';
        }
    }

    clearResults() {
        const outputElement = document.getElementById('code-output');
        const testsElement = document.getElementById('test-results');
        const consoleElement = document.getElementById('console-output');

        if (outputElement) outputElement.innerHTML = 'Cliquez sur "Exécuter" pour voir la sortie de votre code.';
        if (testsElement) testsElement.innerHTML = '';
        if (consoleElement) consoleElement.innerHTML = '';
    }

    updateProgressDisplay() {
        const currentExerciseEl = document.getElementById('current-exercise');
        const totalExercisesEl = document.getElementById('total-exercises');
        
        if (currentExerciseEl) currentExerciseEl.textContent = this.currentExercise;
        if (totalExercisesEl) totalExercisesEl.textContent = this.exercises.length;

        // Mettre à jour les indicateurs de progression dans l'en-tête
        const pointsCounter = document.getElementById('points-counter');
        if (pointsCounter) {
            pointsCounter.textContent = `${this.userProgress.points} pts`;
        }
    }

    loadUserProgress() {
        const saved = localStorage.getItem('codinglab_progress');
        if (saved) {
            try {
                this.userProgress = { ...this.userProgress, ...JSON.parse(saved) };
                console.log('📊 Progression utilisateur chargée');
            } catch (error) {
                console.error('Erreur lors du chargement de la progression:', error);
            }
        }
    }

    saveUserProgress() {
        try {
            localStorage.setItem('codinglab_progress', JSON.stringify(this.userProgress));
            console.log('💾 Progression sauvegardée');
        } catch (error) {
            console.error('Erreur lors de la sauvegarde:', error);
        }
    }

    resetProgress() {
        if (confirm('Êtes-vous sûr de vouloir réinitialiser votre progression ?')) {
            this.userProgress = {
                completedExercises: [],
                points: 0,
                streak: 0,
                level: 1
            };
            this.saveUserProgress();
            this.updateProgressDisplay();
            this.renderExerciseList();
            this.loadExercise(1);
            
            this.showNotification('success', 'Progression réinitialisée', 'Vous pouvez recommencer depuis le début.');
        }
    }

    showNotification(type, title, message) {
        // Créer une notification toast
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--background-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            max-width: 350px;
            z-index: 1200;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.2rem;">${icons[type] || icons.info}</span>
                <div>
                    <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.25rem;">${title}</div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">${message}</div>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Suppression automatique
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }
}

// Initialisation globale
let codingLab = null;

// Fonctions globales pour la compatibilité
window.runCode = () => codingLab?.runCode();
window.submitCode = () => codingLab?.submitCode();
window.formatCode = () => codingLab?.formatCode();
window.showHint = () => codingLab?.showHint();
window.showSolution = () => codingLab?.showSolution();
window.hideSuccessNotification = () => codingLab?.hideSuccessNotification();

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Démarrage du Coding Lab...');
    
    codingLab = new CodingLabPlatform();
    
    // Petite attente pour s'assurer que tous les éléments sont chargés
    setTimeout(() => {
        codingLab.init().catch(error => {
            console.error('❌ Erreur lors de l\'initialisation du Coding Lab:', error);
        });
    }, 500);
});

// Export pour utilisation externe
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CodingLabPlatform;
}

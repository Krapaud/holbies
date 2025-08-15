/**
 * CODING LAB - Configuration et personnalisation
 * Interface inspirée de Coddy.tech
 */

// Configuration des thèmes de couleurs
const THEMES = {
    matrix: {
        name: 'Matrix',
        primary: '#00ff41',
        secondary: '#0066cc',
        accent: '#ff6b35',
        background: '#0a0a0f',
        card: '#1a1a25',
        panel: '#2a2a35',
        text: '#ffffff',
        textSecondary: '#b0b0b0',
        success: '#00ff41',
        error: '#ff4757',
        warning: '#ffa502'
    },
    cyberpunk: {
        name: 'Cyberpunk',
        primary: '#ff0080',
        secondary: '#00ffff',
        accent: '#ffff00',
        background: '#0d0d1a',
        card: '#1a1a2e',
        panel: '#2d2d3f',
        text: '#ffffff',
        textSecondary: '#b0b0b0',
        success: '#00ff80',
        error: '#ff4040',
        warning: '#ff8000'
    },
    holberton: {
        name: 'Holberton',
        primary: '#007bff',
        secondary: '#28a745',
        accent: '#ffc107',
        background: '#1a1a2e',
        card: '#16213e',
        panel: '#0f3460',
        text: '#ffffff',
        textSecondary: '#ced4da',
        success: '#28a745',
        error: '#dc3545',
        warning: '#ffc107'
    }
};

// Configuration des exercices avancés
const ADVANCED_EXERCISES = [
    {
        id: 4,
        title: 'Fonctions et Modules',
        difficulty: 'medium',
        timeEstimate: '15 min',
        points: 125,
        language: 'python',
        category: 'functions',
        description: `
            <h4>🎯 Objectif</h4>
            <p>Apprendre à créer et utiliser des fonctions Python.</p>
            
            <h4>📋 Instructions</h4>
            <ol>
                <li>Créez une fonction qui calcule la factorielle d'un nombre</li>
                <li>Créez une fonction qui vérifie si un nombre est premier</li>
                <li>Créez une fonction qui génère la suite de Fibonacci</li>
                <li>Testez vos fonctions avec différents paramètres</li>
            </ol>
        `,
        requirements: [
            'Définir au moins 3 fonctions',
            'Utiliser des paramètres et valeurs de retour',
            'Inclure de la documentation (docstrings)',
            'Gérer les cas d\'erreur'
        ],
        starter: `# Exercice 4: Fonctions et Modules

def factorielle(n):
    """Calcule la factorielle d'un nombre entier positif"""
    if n < 0:
        raise ValueError("La factorielle n'existe pas pour les nombres négatifs")
    if n == 0 or n == 1:
        return 1
    # Votre code ici
    
def est_premier(n):
    """Vérifie si un nombre est premier"""
    if n < 2:
        return False
    # Votre code ici
    
def fibonacci(n):
    """Génère les n premiers nombres de la suite de Fibonacci"""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    # Votre code ici

# Tests
print(f"Factorielle de 5: {factorielle(5)}")
print(f"7 est premier: {est_premier(7)}")
print(f"Suite de Fibonacci (10): {fibonacci(10)}")`,
        solution: `def factorielle(n):
    """Calcule la factorielle d'un nombre entier positif"""
    if n < 0:
        raise ValueError("La factorielle n'existe pas pour les nombres négatifs")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
    
def est_premier(n):
    """Vérifie si un nombre est premier"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
    
def fibonacci(n):
    """Génère les n premiers nombres de la suite de Fibonacci"""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    suite = [0, 1]
    for i in range(2, n):
        suite.append(suite[i-1] + suite[i-2])
    return suite

# Tests
print(f"Factorielle de 5: {factorielle(5)}")
print(f"7 est premier: {est_premier(7)}")
print(f"Suite de Fibonacci (10): {fibonacci(10)}")`,
        tests: [
            { name: 'Fonction factorielle définie', test: (code) => code.includes('def factorielle(') },
            { name: 'Fonction est_premier définie', test: (code) => code.includes('def est_premier(') },
            { name: 'Fonction fibonacci définie', test: (code) => code.includes('def fibonacci(') },
            { name: 'Utilisation de docstrings', test: (code) => code.includes('"""') },
            { name: 'Gestion d\'erreurs', test: (code) => code.includes('raise') || code.includes('if') }
        ],
        hints: [
            "💡 Utilisez une boucle for pour calculer la factorielle",
            "💡 Pour vérifier si un nombre est premier, testez la divisibilité jusqu'à sa racine carrée",
            "💡 La suite de Fibonacci: chaque nombre est la somme des deux précédents",
            "💡 N'oubliez pas de gérer les cas spéciaux (n=0, n=1, etc.)"
        ]
    },
    {
        id: 5,
        title: 'Structures de Données',
        difficulty: 'medium',
        timeEstimate: '20 min',
        points: 150,
        language: 'python',
        category: 'data-structures',
        description: `
            <h4>🎯 Objectif</h4>
            <p>Maîtriser les listes, dictionnaires et ensembles en Python.</p>
            
            <h4>📋 Instructions</h4>
            <ol>
                <li>Créez un carnet d'adresses avec des dictionnaires</li>
                <li>Implémentez des fonctions de recherche et tri</li>
                <li>Utilisez des ensembles pour éliminer les doublons</li>
                <li>Manipulez des données complexes imbriquées</li>
            </ol>
        `,
        requirements: [
            'Utiliser des dictionnaires imbriqués',
            'Implémenter des fonctions de manipulation',
            'Utiliser des list comprehensions',
            'Gérer des ensembles (sets)'
        ],
        starter: `# Exercice 5: Structures de Données

# Carnet d'adresses
carnet = {
    "alice": {
        "nom": "Alice Dupont",
        "email": "alice@email.com",
        "telephone": "0123456789",
        "ville": "Paris",
        "competences": ["Python", "JavaScript", "React"]
    },
    "bob": {
        "nom": "Bob Martin",
        "email": "bob@email.com", 
        "telephone": "0987654321",
        "ville": "Lyon",
        "competences": ["Java", "Python", "SQL"]
    }
}

def ajouter_contact(carnet, id_contact, nom, email, telephone, ville, competences):
    """Ajoute un nouveau contact au carnet"""
    # Votre code ici
    
def rechercher_par_ville(carnet, ville):
    """Trouve tous les contacts d'une ville donnée"""
    # Votre code ici
    
def competences_uniques(carnet):
    """Retourne toutes les compétences uniques du carnet"""
    # Votre code ici
    
def contacts_par_competence(carnet, competence):
    """Trouve les contacts ayant une compétence donnée"""
    # Votre code ici

# Tests
ajouter_contact(carnet, "charlie", "Charlie Brown", "charlie@email.com", "0555123456", "Marseille", ["Python", "Django"])
print(f"Contacts à Paris: {rechercher_par_ville(carnet, 'Paris')}")
print(f"Toutes les compétences: {competences_uniques(carnet)}")
print(f"Experts Python: {contacts_par_competence(carnet, 'Python')}")`,
        solution: `# Carnet d'adresses
carnet = {
    "alice": {
        "nom": "Alice Dupont",
        "email": "alice@email.com",
        "telephone": "0123456789",
        "ville": "Paris",
        "competences": ["Python", "JavaScript", "React"]
    },
    "bob": {
        "nom": "Bob Martin",
        "email": "bob@email.com", 
        "telephone": "0987654321",
        "ville": "Lyon",
        "competences": ["Java", "Python", "SQL"]
    }
}

def ajouter_contact(carnet, id_contact, nom, email, telephone, ville, competences):
    """Ajoute un nouveau contact au carnet"""
    carnet[id_contact] = {
        "nom": nom,
        "email": email,
        "telephone": telephone,
        "ville": ville,
        "competences": competences
    }
    
def rechercher_par_ville(carnet, ville):
    """Trouve tous les contacts d'une ville donnée"""
    return [contact["nom"] for contact in carnet.values() if contact["ville"] == ville]
    
def competences_uniques(carnet):
    """Retourne toutes les compétences uniques du carnet"""
    toutes_competences = []
    for contact in carnet.values():
        toutes_competences.extend(contact["competences"])
    return list(set(toutes_competences))
    
def contacts_par_competence(carnet, competence):
    """Trouve les contacts ayant une compétence donnée"""
    return [contact["nom"] for contact in carnet.values() if competence in contact["competences"]]

# Tests
ajouter_contact(carnet, "charlie", "Charlie Brown", "charlie@email.com", "0555123456", "Marseille", ["Python", "Django"])
print(f"Contacts à Paris: {rechercher_par_ville(carnet, 'Paris')}")
print(f"Toutes les compétences: {competences_uniques(carnet)}")
print(f"Experts Python: {contacts_par_competence(carnet, 'Python')}")`,
        tests: [
            { name: 'Fonction ajouter_contact définie', test: (code) => code.includes('def ajouter_contact(') },
            { name: 'Fonction rechercher_par_ville définie', test: (code) => code.includes('def rechercher_par_ville(') },
            { name: 'Fonction competences_uniques définie', test: (code) => code.includes('def competences_uniques(') },
            { name: 'Utilisation de dictionnaires', test: (code) => code.includes('carnet[') && code.includes('{') },
            { name: 'Manipulation de listes', test: (code) => code.includes('[') && code.includes('extend') || code.includes('append') }
        ],
        hints: [
            "💡 Utilisez la méthode .values() pour parcourir les valeurs d'un dictionnaire",
            "💡 Les list comprehensions sont parfaites pour filtrer et transformer des données",
            "💡 set() élimine automatiquement les doublons d'une liste",
            "💡 L'opérateur 'in' vérifie l'appartenance dans une liste"
        ]
    }
];

// Configuration de l'éditeur de code
const EDITOR_CONFIG = {
    themes: {
        dark: {
            background: '#1e1e1e',
            foreground: '#d4d4d4',
            comment: '#6a9955',
            keyword: '#569cd6',
            string: '#ce9178',
            number: '#b5cea8',
            function: '#dcdcaa'
        },
        matrix: {
            background: '#0a0a0a',
            foreground: '#00ff41',
            comment: '#008f11',
            keyword: '#00cc33',
            string: '#00ff99',
            number: '#66ff66',
            function: '#99ff99'
        }
    },
    features: {
        autoIndent: true,
        bracketMatching: true,
        syntaxHighlighting: true,
        lineNumbers: false, // Simplifié pour cette version
        wordWrap: true,
        fontSize: 14,
        fontFamily: "'Fira Code', 'Monaco', 'Menlo', monospace"
    }
};

// Configuration des achievements/badges
const ACHIEVEMENTS = [
    {
        id: 'first_steps',
        name: 'Premiers Pas',
        description: 'Compléter votre premier exercice',
        icon: '🎯',
        condition: (progress) => progress.completedExercises.length >= 1,
        points: 25
    },
    {
        id: 'python_master',
        name: 'Maître Python',
        description: 'Compléter tous les exercices Python',
        icon: '🐍',
        condition: (progress) => progress.completedExercises.length >= 5,
        points: 100
    },
    {
        id: 'speed_coder',
        name: 'Codeur Rapide',
        description: 'Compléter un exercice en moins de 5 minutes',
        icon: '⚡',
        condition: (progress) => progress.fastCompletions >= 1,
        points: 50
    },
    {
        id: 'perfectionist',
        name: 'Perfectionniste',
        description: 'Compléter 3 exercices sans demander d\'indice',
        icon: '💎',
        condition: (progress) => progress.perfectCompletions >= 3,
        points: 75
    },
    {
        id: 'streak_warrior',
        name: 'Guerrier de la Série',
        description: 'Maintenir une série de 7 jours',
        icon: '🔥',
        condition: (progress) => progress.streak >= 7,
        points: 200
    }
];

// Configuration des langages de programmation
const PROGRAMMING_LANGUAGES = {
    python: {
        name: 'Python',
        icon: '🐍',
        color: '#3776ab',
        fileExtension: '.py',
        helloWorld: 'print("Hello, World!")',
        features: ['Variables', 'Boucles', 'Fonctions', 'Classes', 'Modules'],
        difficulty: 'Débutant',
        popularity: 95
    },
    javascript: {
        name: 'JavaScript',
        icon: '🟨',
        color: '#f7df1e',
        fileExtension: '.js',
        helloWorld: 'console.log("Hello, World!");',
        features: ['DOM', 'Async/Await', 'Promesses', 'Closures', 'Prototypes'],
        difficulty: 'Intermédiaire',
        popularity: 98
    },
    html: {
        name: 'HTML',
        icon: '🔗',
        color: '#e34f26',
        fileExtension: '.html',
        helloWorld: '<h1>Hello, World!</h1>',
        features: ['Balises', 'Attributs', 'Formulaires', 'Sémantique', 'Accessibilité'],
        difficulty: 'Débutant',
        popularity: 90
    },
    css: {
        name: 'CSS',
        icon: '🎨',
        color: '#1572b6',
        fileExtension: '.css',
        helloWorld: 'body { color: blue; }',
        features: ['Sélecteurs', 'Flexbox', 'Grid', 'Animations', 'Responsive'],
        difficulty: 'Intermédiaire',
        popularity: 85
    }
};

// Configuration des niveaux de difficulté
const DIFFICULTY_LEVELS = {
    easy: {
        name: 'Débutant',
        color: '#28a745',
        icon: '🟢',
        maxTime: 15, // minutes
        pointsMultiplier: 1.0,
        hintsAllowed: 3
    },
    medium: {
        name: 'Intermédiaire',
        color: '#ffc107',
        icon: '🟡',
        maxTime: 25,
        pointsMultiplier: 1.5,
        hintsAllowed: 2
    },
    hard: {
        name: 'Avancé',
        color: '#dc3545',
        icon: '🔴',
        maxTime: 40,
        pointsMultiplier: 2.0,
        hintsAllowed: 1
    },
    expert: {
        name: 'Expert',
        color: '#6f42c1',
        icon: '🟣',
        maxTime: 60,
        pointsMultiplier: 3.0,
        hintsAllowed: 0
    }
};

// Export des configurations
if (typeof window !== 'undefined') {
    window.CODING_LAB_CONFIG = {
        THEMES,
        ADVANCED_EXERCISES,
        EDITOR_CONFIG,
        ACHIEVEMENTS,
        PROGRAMMING_LANGUAGES,
        DIFFICULTY_LEVELS
    };
}

// Export pour Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        THEMES,
        ADVANCED_EXERCISES,
        EDITOR_CONFIG,
        ACHIEVEMENTS,
        PROGRAMMING_LANGUAGES,
        DIFFICULTY_LEVELS
    };
}

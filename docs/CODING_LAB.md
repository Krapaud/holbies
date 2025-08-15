# 🚀 Coding Lab - Plateforme d'Apprentissage Interactive

## Vue d'ensemble

Le **Coding Lab** est une plateforme d'apprentissage de programmation moderne inspirée de [Coddy.tech](https://coddy.tech/), intégrée au projet Holbies. Elle offre une expérience d'apprentissage interactive avec un éditeur de code en ligne, des tests automatiques et un système de progression gamifié.

## ✨ Fonctionnalités Principales

### 🎯 Interface Moderne
- **Design inspiré de Coddy.tech** avec thème Matrix/Cyberpunk
- **Interface responsive** adaptée aux desktop, tablettes et mobiles
- **Navigation intuitive** avec sidebar d'exercices et zone de travail

### 📝 Éditeur de Code Intégré
- **Coloration syntaxique** pour Python, JavaScript, HTML, CSS
- **Auto-indentation** et autocomplétion basique
- **Support multi-langages** avec templates de démarrage
- **Formatage automatique** du code

### 🧪 Système de Tests Automatiques
- **Validation en temps réel** du code écrit
- **Tests unitaires automatiques** pour chaque exercice
- **Feedback instantané** avec explications détaillées
- **Progression basée sur les résultats**

### 🏆 Gamification
- **Système de points** pour chaque exercice complété
- **Achievements/Badges** pour motiver l'apprentissage
- **Suivi de progression** avec statistiques détaillées
- **Streak counter** pour encourager la régularité

### 💡 Aide Intelligente
- **Système d'indices** contextuels pour débloquer les étudiants
- **Solutions expliquées** disponibles avec pénalité de points
- **Messages d'erreur** clairs et pédagogiques

## 🎓 Exercices Disponibles

### Niveau Débutant
1. **Variables et Types** - Introduction aux variables Python
2. **Conditions et Logique** - Structures if/elif/else
3. **Boucles et Répétitions** - for, while, break, continue

### Niveau Intermédiaire  
4. **Fonctions et Modules** - Définition et utilisation de fonctions
5. **Structures de Données** - Listes, dictionnaires, ensembles

### Niveau Avancé (À venir)
6. **Programmation Orientée Objet** - Classes et objets
7. **Gestion des Erreurs** - try/except/finally
8. **Fichiers et I/O** - Lecture/écriture de fichiers
9. **APIs et Requêtes** - Interaction avec des services web
10. **Projets Intégrés** - Applications complètes

## 🛠️ Technologies Utilisées

### Frontend
- **HTML5/CSS3** avec variables CSS pour les thèmes
- **JavaScript ES6+** pour l'interactivité
- **Font Awesome** pour les icônes
- **Fira Code** font pour l'éditeur de code

### Backend
- **FastAPI** pour l'API REST
- **PostgreSQL** pour la persistance des données
- **Docker** pour la conteneurisation

### Fonctionnalités Techniques
- **Simulateur Python** sécurisé côté client
- **Sauvegarde automatique** de la progression
- **API REST** pour synchronisation multi-appareils

## 🎨 Thèmes Disponibles

### Matrix (Par défaut)
- Couleur primaire: `#00ff41` (vert Matrix)
- Fond sombre avec effets lumineux
- Animation de scan en en-tête

### Cyberpunk  
- Couleurs néon: rose, cyan, jaune
- Ambiance futuriste

### Holberton
- Couleurs officielles de l'école
- Design professionnel

## 📱 Responsive Design

L'interface s'adapte automatiquement aux différentes tailles d'écran :

- **Desktop** (>1024px): Layout complet avec sidebar
- **Tablette** (768-1024px): Layout adapté avec sidebar réduite  
- **Mobile** (<768px): Layout vertical avec navigation simplifiée

## 🚀 Installation et Déploiement

### Prérequis
- Docker et Docker Compose
- Python 3.11+
- PostgreSQL 15+

### Démarrage Rapide
```bash
# Cloner le projet
git clone <repository-url>
cd project-holbies

# Démarrer avec Docker
docker-compose -f deployment/docker-compose.yml up --build -d

# Accéder à l'application
# - Page d'accueil Coding Lab: http://localhost:8000/coding-lab-home  
# - Interface Coding Lab: http://localhost:8000/coding-lab
```

### URLs Principales
- `/coding-lab-home` - Page de présentation des fonctionnalités
- `/coding-lab` - Interface d'apprentissage interactive
- `/api/coding-lab/*` - Endpoints API pour la progression

## 📊 API Endpoints

### Progression Utilisateur
```
GET /api/coding-lab/progress     # Récupérer la progression
POST /api/coding-lab/save-progress # Sauvegarder la progression
```

### Exécution de Code
```
POST /api/coding-lab/run-code    # Exécuter du code de manière sécurisée
```

## 🎯 Roadmap

### Phase 1 (Actuelle)
- [x] Interface de base inspirée de Coddy.tech
- [x] Éditeur de code avec coloration syntaxique
- [x] Système de tests automatiques
- [x] 5 exercices Python de base
- [x] Système de points et progression

### Phase 2 (À venir)
- [ ] Intégration d'un vrai éditeur Monaco/CodeMirror
- [ ] Exécution de code sécurisée côté serveur
- [ ] Plus d'exercices et de langages
- [ ] Système d'achievements avancé
- [ ] Mode collaboratif

### Phase 3 (Future)
- [ ] IA pour génération d'exercices personnalisés
- [ ] Intégration avec GitHub pour projets
- [ ] Certification et évaluation
- [ ] Mode multijoueur/compétitions

## 🔧 Configuration

### Variables d'Environnement
```bash
# Base de données
DATABASE_URL=postgresql://user:password@db:5432/holberton_db

# Sécurité  
SECRET_KEY=your-secret-key

# Coding Lab
CODING_LAB_THEME=matrix
ENABLE_CODE_EXECUTION=true
MAX_EXECUTION_TIME=30
```

### Personnalisation des Thèmes
Les thèmes sont configurables dans `/static/js/coding-lab-config.js`:

```javascript
const THEMES = {
  custom: {
    name: 'Mon Thème',
    primary: '#your-color',
    // ... autres couleurs
  }
};
```

## 📚 Documentation Technique

### Architecture
```
src/
├── templates/
│   ├── coding-lab.html          # Interface principale
│   └── coding-lab-home.html     # Page d'accueil
├── static/
│   ├── css/
│   │   └── coding-lab.css       # Styles principaux
│   └── js/
│       ├── coding-lab.js        # Logique principale
│       └── coding-lab-config.js # Configuration
└── main.py                      # Routes FastAPI
```

### Classes JavaScript Principales
- `CodingLabPlatform` - Gestionnaire principal de l'interface
- `PythonSimulator` - Simulateur d'exécution Python côté client
- `ProgressManager` - Gestion de la progression utilisateur

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commit** vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Ouvrir** une Pull Request

### Guidelines de Développement
- Suivre les conventions de nommage existantes
- Ajouter des tests pour les nouvelles fonctionnalités  
- Documenter les fonctions et classes importantes
- Maintenir la compatibilité responsive

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Coddy.tech** pour l'inspiration de l'interface
- **FastAPI** pour le framework backend
- **Font Awesome** pour les icônes
- **Fira Code** pour la police de l'éditeur

---

**Développé avec ❤️ pour la communauté Holberton School**

> 💡 **Astuce**: Pour une expérience optimale, utilisez un navigateur moderne avec JavaScript activé et une connexion internet stable.

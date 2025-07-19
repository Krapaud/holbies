# 🧠 Holbies Learning Hub

Un système de quiz interactif avec un thème Matrix pour l'apprentissage technique, développé avec FastAPI, PostgreSQL et un design geek sombre inspiré de Matrix. Le projet inclut maintenant un **système de corr2. **🔧 API REST**
   - Documentation interactive avec Swagger
   - Endpoints sécurisés avec JWT
   - Validation automatique des données
   - Gestion d'erreurs complète
   - **API AI Quiz** pour sessions PLD

3. **🗄️ Base de Données**
   - Modèles SQLAlchemy bien structurés
   - **Tables AI Quiz** : sessions, réponses, scores
   - Migrations avec Alembic
   - Relations optimisées
   - Index pour les performancesvancé** pour les questions à réponse libre de type PLD (Peer Learning Day).

![Matrix Theme](https://img.shields.io/badge/Theme-Matrix-00ff41)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue)
![AI Powered](https://img.shields.io/badge/AI-Powered-ff6b35)

## ✨ Fonctionnalités

### 🎯 Système de Quiz Classique
- **50+ questions** style PLD Holberton School
- **Correcteur automatique** avec explications détaillées
- **Catégories variées** : Algorithmes, Python, C, JavaScript, Web, SQL, Linux, Git
- **Suivi des performances** et statistiques personnelles
- **Sessions sauvegardées** avec historique complet

### 🤖 AI Quiz (PLD) - NOUVEAU !
- **Questions à réponse libre** corrigées par Intelligence Artificielle
- **Scoring intelligent** : 70% similarité + 30% usage de termes techniques
- **Bonus technique** : +5 points par terme technique utilisé correctement
- **Feedback détaillé** avec explications personnalisées
- **Analyse sémantique** avancée des réponses
- **Recommandations d'amélioration** basées sur les performances
- **Sessions persistantes** avec historique complet et métriques détaillées

### 🎨 Interface Matrix
- **Thème sombre** avec couleurs néon vertes (#00ff41)
- **Animations Matrix** : code rain, effets de glitch, particules flottantes
- **Design responsive** optimisé mobile et desktop
- **Polices monospace** (Orbitron, Source Code Pro)
- **Effets visuels** immersifs et interactifs

### 🔐 Authentification Sécurisée
- **JWT tokens** pour l'authentification
- **Hachage bcrypt** des mots de passe
- **Validation avancée** côté client et serveur
- **Sessions persistantes** et sécurisées
- **🎬 Vidéo de bienvenue** automatique après connexion avec fermeture auto

### 🎥 Système de Vidéo de Bienvenue
- **Lecture automatique** après connexion réussie
- **Modal plein écran** avec design Matrix intégré
- **Support multi-formats** (MP4, WebM, OGV)
- **Fermeture automatique** à la fin de la vidéo
- **Contrôles manuels** (Escape, clic extérieur, bouton X)
- **Animation de fallback** si aucune vidéo n'est présente
- **Effets visuels Matrix** avec bordures animées

### 📊 Dashboard Interactif
- **Statistiques combinées** : scores des quiz classiques ET des sessions AI Quiz (PLD)
- **Graphiques de performance** avec Chart.js intégrant tous types de sessions
- **Historique unifié** des sessions avec distinction visuelle (📝 Quiz / 🤖 PLD)
- **Métriques détaillées** : pourcentages, scores bruts, séries de réussite
- **Indicateurs de progression** visuels avec animations
- **Comparaison des performances** entre quiz classiques et PLD

## 🚀 Installation Rapide

### Méthode 1 : Script Automatique
```bash
git clone https://github.com/votre-repo/holbies-learning-hub.git
cd holbies-learning-hub
./start.sh
```

### Méthode 2 : Manuel
```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer la base de données
cp .env.example .env
# Modifier .env avec vos paramètres PostgreSQL

# 4. Créer les tables et données
python3 -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
python3 populate_db.py

# 5. Créer un admin (optionnel)
python3 create_admin.py

# 6. Démarrer le serveur
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Méthode 3 : Docker
```bash
docker-compose up --build
```

## 🌐 Accès à l'Application

Une fois démarré, l'application est accessible à :

- **🏠 Accueil** : http://localhost:8000
- **🔐 Connexion** : http://localhost:8000/login
- **📝 Inscription** : http://localhost:8000/register
- **🧠 Quiz Classique** : http://localhost:8000/quiz
- **🤖 AI Quiz (PLD)** : http://localhost:8000/ai-quiz
- **📚 Learning Hub** : http://localhost:8000/learning
- **📊 Dashboard** : http://localhost:8000/dashboard
- **📚 API Docs** : http://localhost:8000/docs

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI** - Framework web moderne et rapide
- **SQLAlchemy** - ORM Python avancé
- **PostgreSQL** - Base de données relationnelle
- **Alembic** - Migrations de base de données
- **python-jose** - JWT pour l'authentification
- **passlib** - Hachage sécurisé des mots de passe
- **AI Corrector** - Système de correction automatique intelligent

### Frontend
- **HTML5/CSS3** - Structure et styles modernes
- **JavaScript ES6+** - Logique interactive
- **CSS Variables** - Thématisation avancée
- **Chart.js** - Graphiques de performance
- **Animations CSS** - Effets Matrix immersifs

### Intelligence Artificielle
- **Analyse sémantique** - Comparaison intelligente de textes
- **Scoring adaptatif** - Évaluation basée sur la similarité et les termes techniques
- **Feedback personnalisé** - Recommandations ciblées selon les performances
- **Sessions persistantes** - Suivi complet des sessions AI Quiz

### Sécurité
- **JWT Authentication** - Tokens sécurisés
- **bcrypt** - Hachage des mots de passe
- **CORS** - Protection cross-origin
- **Variables d'environnement** - Configuration sécurisée

## 📁 Structure du Projet

```
holbies-learning-hub/
├── 🐍 Backend Python
│   ├── app/
│   │   ├── auth.py          # Authentification JWT
│   │   ├── database.py      # Configuration DB
│   │   ├── models.py        # Modèles SQLAlchemy (+ AI Quiz)
│   │   ├── schemas.py       # Schémas Pydantic
│   │   └── routers/         # Routes API
│   │       ├── quiz.py      # Quiz classique
│   │       ├── ai_quiz.py   # AI Quiz (PLD) - NOUVEAU !
│   │       └── users.py     # Gestion utilisateurs
│   ├── main.py              # Point d'entrée FastAPI
│   ├── ai_quiz_corrector.py # Correcteur IA intelligent - NOUVEAU !
│   └── requirements.txt     # Dépendances
├── 🌐 Frontend
│   ├── static/
│   │   ├── css/style.css    # Styles Matrix
│   │   ├── js/              # JavaScript modules
│   │   │   ├── ai-quiz.js   # Gestion AI Quiz - NOUVEAU !
│   │   │   ├── quiz.js      # Quiz classique
│   │   │   ├── dashboard.js # Dashboard unifié
│   │   │   ├── video-modal.js          # Système vidéo de bienvenue
│   │   │   ├── welcome-video-generator.js # Animation de fallback
│   │   │   └── auth.js      # Authentification avec vidéo
│   │   └── video/           # Vidéos de bienvenue
│   └── templates/           # Templates Jinja2
│       ├── ai-quiz.html     # Interface AI Quiz - NOUVEAU !
│       ├── learning.html    # Hub d'apprentissage
│       └── dashboard.html   # Dashboard unifié
├── 🗄️ Base de données
│   ├── alembic/             # Migrations
│   ├── populate_db_balanced.py # Questions équilibrées - MIS À JOUR !
│   └── alembic.ini          # Configuration
├── 🛠️ Scripts utilitaires
│   ├── start.sh             # Démarrage automatique
│   ├── create_admin.py      # Création admin
│   └── test_installation.py # Tests d'installation
└── 🐳 Déploiement
    ├── Dockerfile
    └── docker-compose.yml
```

## 🧪 Test de l'Installation

Vérifiez que tout fonctionne correctement :

```bash
python3 test_installation.py
```

Ce script teste :
- ✅ Imports Python
- ✅ Connexion base de données
- ✅ Modèles de données
- ✅ Fichiers statiques
- ✅ Templates HTML
- ✅ Serveur web

## 🎮 Guide d'Utilisation

### Pour les Étudiants

1. **📝 Inscription**
   - Créer un compte avec username, email, mot de passe
   - Validation en temps réel des champs
   - Indicateur de force du mot de passe

2. **🔐 Connexion**
   - Authentification sécurisée avec JWT
   - **🎬 Vidéo de bienvenue automatique** après connexion
   - Session persistante
   - Redirection automatique vers le dashboard

3. **🧠 Quiz Classique**
   - Questions à choix multiples
   - Feedback instantané avec explications
   - Progression visuelle
   - Scores en temps réel

4. **🤖 AI Quiz (PLD)**
   - Questions à réponse libre
   - Correction intelligente par IA
   - Feedback détaillé et personnalisé
   - Scoring basé sur similarité et termes techniques
   - Recommandations d'amélioration

5. **📊 Dashboard**
   - Statistiques combinées (Quiz + PLD)
   - Graphique de performance unifié
   - Historique des sessions avec distinction visuelle
   - Actions rapides

### Pour les Développeurs

1. **🔧 API REST**
   - Documentation interactive avec Swagger
   - Endpoints sécurisés avec JWT
   - Validation automatique des données
   - Gestion d'erreurs complète

2. **🗄️ Base de Données**
   - Modèles SQLAlchemy bien structurés
   - Migrations avec Alembic
   - Relations optimisées
   - Index pour les performances

## 🎨 Personnalisation du Thème

Le thème Matrix est entièrement personnalisable via les variables CSS :

```css
:root {
    --primary-green: #00ff41;      /* Vert Matrix principal */
    --secondary-green: #008f11;    /* Vert secondaire */
    --matrix-black: #0d1117;       /* Noir de fond */
    --matrix-dark: #161b22;        /* Gris foncé */
    --text-light: #c9d1d9;         /* Texte clair */
    /* ... autres variables */
}
```

## 📚 Questions du Quiz

### Catégories Disponibles

- **🔢 Algorithms** : Complexité, structures de données, tri
- **🐍 Python** : Syntaxe, types, méthodes, concepts avancés
- **⚙️ C Programming** : Pointeurs, mémoire, syntaxe
- **🌐 JavaScript** : ES6+, DOM, JSON, types
- **🌍 Web** : HTML, CSS, HTTP/HTTPS, APIs REST
- **🗄️ SQL** : Requêtes, jointures, optimisation
- **🐧 Linux** : Commandes, permissions, système
- **📚 Git** : Contrôle de version, branches, workflow
- **🔐 Security** : Vulnérabilités, authentification
- **🏗️ OOP** : Héritage, polymorphisme, encapsulation

### Types de Quiz

#### 📝 Quiz Classique (QCM)
- **Questions à choix multiples** avec 4 options
- **Correction automatique** instantanée
- **Explications détaillées** pour chaque réponse
- **Score basé** sur le nombre de bonnes réponses

#### 🤖 AI Quiz (PLD - Peer Learning Day)
- **Questions à réponse libre** nécessitant des explications
- **Correction par Intelligence Artificielle** avec analyse sémantique
- **Scoring intelligent** : 70% similarité + 30% termes techniques
- **Feedback personnalisé** avec recommandations d'amélioration

### Niveaux de Difficulté

- **🟢 Easy** : Concepts de base, syntaxe simple
- **🟡 Medium** : Applications pratiques, concepts intermédiaires
- **🔴 Hard** : Optimisation, concepts avancés, algorithmes complexes

## 🔧 Configuration Avancée

### Variables d'Environnement

```env
# Base de données
DATABASE_URL=postgresql://user:pass@localhost/holbies_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Ajout de Questions

#### Questions Quiz Classique (QCM)

Pour ajouter des questions QCM dans `populate_db_balanced.py` :

```python
{
    "question_text": "Votre question ?",
    "option_a": "Option A",
    "option_b": "Option B", 
    "option_c": "Option C",
    "option_d": "Option D",
    "correct_answer": "a",  # a, b, c, ou d
    "explanation": "Explication de la réponse",
    "difficulty": "medium",  # easy, medium, hard
    "category": "votre-categorie"
}
```

#### Questions AI Quiz (PLD)

Pour ajouter des questions PLD dans `app/routers/ai_quiz.py` :

```python
{
    "id": "unique-id",
    "question_text": "Expliquez en détail le concept...",
    "expected_answer": "Réponse attendue complète",
    "technical_terms": ["terme1", "terme2", "terme3"],
    "explanation": "Explication du concept",
    "difficulty": "medium",
    "category": "c-programming",
    "max_score": 100  # Score maximum pour cette question
}
```

Puis relancer : `python3 populate_db_balanced.py`

## 🎬 Configuration de la Vidéo de Bienvenue

### Ajouter une Vidéo Personnalisée

1. **Placer votre vidéo** dans le dossier `/static/video/`
2. **Nommer le fichier** `welcome.mp4` (ou `.webm`, `.ogv`)
3. **Redémarrer le serveur** pour appliquer les changements

```bash
# Exemple d'ajout de vidéo
cp votre-video.mp4 static/video/welcome.mp4
python main.py
```

### Format Vidéo Recommandé

- **Format** : MP4 (H.264) pour une compatibilité maximale
- **Résolution** : 1280x720 ou 1920x1080
- **Durée** : 3-8 secondes pour une expérience optimale
- **Taille** : Maximum 10-15MB
- **Audio** : AAC, volume modéré

### Optimisation avec FFmpeg

```bash
# Optimiser une vidéo pour le web
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 128k -movflags +faststart static/video/welcome.mp4
```

### Fonctionnement

- ✅ **Détection automatique** de la présence de vidéo
- ✅ **Lecture avec son** après connexion réussie
- ✅ **Fermeture automatique** à la fin
- ✅ **Animation de fallback** si pas de vidéo
- ✅ **Contrôles utilisateur** (Escape, clic, bouton X)

## 🤖 Système AI Quiz (PLD) - Guide Complet

### 🎯 Fonctionnement de l'IA

Le système de correction IA analyse les réponses textuelles selon plusieurs critères :

#### 🔍 **Analyse Sémantique**
- **Similarité textuelle** : Comparaison avec la réponse attendue (70% du score)
- **Correspondance des concepts** : Vérification de la compréhension
- **Structure logique** : Cohérence de l'argumentation

#### 🔧 **Analyse Technique**
- **Détection de termes techniques** : Identification automatique (30% du score)
- **Bonus technique** : +5 points par terme correctly utilisé
- **Validation contextuelle** : Utilisation appropriée des termes

#### 📊 **Scoring Intelligent**
```python
Score Final = (Similarité × 0.7) + (Termes Techniques × 0.3) + Bonus
```

### 📝 **Types de Questions PLD**

#### Difficultés Disponibles
- **🟢 EASY** (100 pts) : Concepts de base, définitions simples
- **🟡 MEDIUM** (100 pts) : Applications pratiques, explications détaillées  
- **🔴 HARD** (100 pts) : Optimisation, algorithmes complexes, analyses poussées

#### Catégories Actuelles
- **⚙️ C Programming** : Compilation, pointeurs, gestion mémoire
- **🐍 Python** : Structures de données, paradigmes, optimisation
- **🔢 Algorithms** : Complexité, tri, recherche, graphes
- **🌐 Web Development** : Architectures, protocoles, sécurité

### 🎯 **Exemple de Session PLD**

#### Question Exemple (C Programming - HARD)
```
Expliquez en détail le processus de compilation en C, 
en décrivant chaque étape et son rôle.
```

#### Réponse Attendue
```
La compilation C se fait en plusieurs étapes : 
préprocesseur (macros, includes), compilateur 
(code source vers assembleur), assembleur 
(assembleur vers code objet), et éditeur de liens 
(liaison des modules pour créer l'exécutable).
```

#### Termes Techniques Détectés
- préprocesseur, compilateur, assembleur
- éditeur de liens, linker, code objet
- exécutable, macros, bibliothèques

#### Exemple de Scoring
- **Réponse utilisateur** : "La compilation transforme le code C en exécutable via le préprocesseur puis le compilateur"
- **Similarité** : 65% (concepts présents mais incomplets)
- **Termes techniques** : 3 détectés → +15 points
- **Score final** : (65 × 0.7) + (100 × 0.3) + 15 = **90.5/100**

### 📈 **Dashboard Intégré**

Le dashboard combine maintenant les performances des deux types de quiz :

#### Statistiques Unifiées
- **Total des quiz** : Quiz classiques + Sessions PLD
- **Score moyen** : Moyenne pondérée des pourcentages
- **Meilleur score** : Maximum atteint (tous types confondus)
- **Série actuelle** : Réussites consécutives (≥60%)

#### Graphique de Performance
- **Ligne temporelle** : Évolution chronologique
- **Distinction visuelle** : 📝 Quiz / 🤖 PLD
- **Métriques détaillées** : Scores et pourcentages

#### Historique des Sessions
```
🤖 PLD - 19/07/2025
425/500 pts (85%)

📝 Quiz - 19/07/2025  
8/10 questions (80%)
```

## 🚀 Déploiement en Production

### Avec Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Avec Docker

```bash
docker build -t holbies-hub .
docker run -p 8000:8000 holbies-hub
```

### Variables de Production

```env
DEBUG=False
SECRET_KEY=your-production-secret-key-very-long-and-complex
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host/prod_db
```

## 🤝 Contribution

1. 🍴 Fork le projet
2. 🌿 Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. 💾 Commit (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. 📤 Push (`git push origin feature/nouvelle-fonctionnalite`)
5. 🔄 Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

## 🚀 Roadmap

### Version 2.0 ✅ **TERMINÉ**
- [x] 🤖 **Système AI Quiz (PLD)** - Questions à réponse libre avec correction IA
- [x] 📊 **Dashboard unifié** - Statistiques combinées Quiz + PLD
- [x] 🔄 **Sessions persistantes** - Sauvegarde complète des sessions AI Quiz
- [x] 📈 **Graphiques de performance** - Intégration des données PLD
- [x] 🎯 **Scoring intelligent** - Analyse sémantique + termes techniques
- [x] 💾 **Modèles de données** - Tables AIQuizSession et AIQuizAnswer

### Version 2.1
- [ ] 🏆 Système de badges et récompenses
- [ ] ⏱️ Quiz chronométrés avec mode challenge
- [ ] 💻 Questions de code avec syntax highlighting
- [ ] 🥇 Classements et compétitions
- [ ] 👥 Mode multijoueur en temps réel
- [ ] 📱 Application mobile Progressive Web App

### Version 2.2
- [ ] 📁 Import/Export de questions (JSON, CSV)
- [ ] 🎨 Thèmes personnalisables (Cyberpunk, Retro, etc.)
- [ ] 🔊 Effets sonores et musique d'ambiance
- [ ] 🎬 Vidéos de bienvenue personnalisées par utilisateur
- [ ] 📈 Analytics avancées et rapports
- [ ] 🌍 Support multilingue (EN, FR, ES)
- [ ] ☁️ Sauvegarde cloud et synchronisation
- [ ] 🧠 **IA améliorée** - Correction plus précise et feedback enrichi

---

**Créé avec ❤️ pour la communauté des développeurs**

🌟 **Star ce projet** si il vous a plu !  
🐛 **Reportez les bugs** dans les Issues  
💡 **Proposez des améliorations** via Pull Request

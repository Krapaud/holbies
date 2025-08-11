# 🎯 Holbies Learning Hub

<div align="center">

**Plateforme d'apprentissage interactive moderne avec thème Matrix et correction IA**

![Matrix Theme](https://img.shields.io/badge/Theme-Matrix-00ff41?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI-Powered-ff6b35?style=for-the-badge)

[🚀 Demo Live](#) • [📖 Documentation](#) • [🐛 Issues](https://github.com/Krapaud/project-holbies/issues) • [💡 Contributing](#-contribution)

</div>

---

## 🌟 Présentation

**Holbies Learning Hub** est une plateforme d'apprentissage technique moderne inspirée de l'univers Matrix. Elle combine quiz classiques et intelligence artificielle pour offrir une expérience d'apprentissage immersive et adaptée aux développeurs.

### ✨ Points Forts

- 🧠 **Quiz Intelligents** - Questions techniques variées avec correction automatique
- 🤖 **IA Avancée** - Correction intelligente des réponses libres avec feedback personnalisé  
- 🎨 **Interface Matrix** - Design cyberpunk avec animations immersives
- 📊 **Analytics** - Suivi des performances et progression détaillée
- 🔐 **Sécurité** - Authentification JWT et protection des données
- 🐳 **Docker Ready** - Déploiement simplifié avec docker-compose

---

## 🚀 Installation Rapide

### Méthode Docker (Recommandée)

```bash
# Cloner le projet
git clone https://github.com/Krapaud/project-holbies.git
cd project-holbies

# Lancer avec Docker
docker-compose up --build

# Accéder à l'application
open http://localhost:8000
```

### Installation Manuelle

```bash
# 1. Prérequis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configuration
cp .env.example .env
# Modifier .env avec vos paramètres

# 3. Base de données
python scripts/create_tables.py
python scripts/populate_db_balanced.py

# 4. Démarrage
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🎮 Fonctionnalités

### 🎯 Quiz Classiques
- **150+ questions** techniques couvrant Python, JavaScript, C, Algorithms, Web, SQL, Linux, Git
- **Correcteur automatique** avec explications détaillées
- **Catégories et difficultés** multiples (Easy/Medium/Hard)
- **Système de scoring** et suivi des performances

### 🤖 AI Quiz (PLD)
- **Questions à réponse libre** corrigées par Intelligence Artificielle
- **Scoring intelligent** : 70% similarité sémantique + 30% termes techniques
- **Feedback personnalisé** avec recommandations d'amélioration
- **Sessions persistantes** avec historique complet

### 🎨 Interface Matrix
- **Thème cyberpunk** avec couleurs néon vertes (#00ff41)
- **Animations fluides** : terminal animé, effets de glitch, particules
- **Design responsive** optimisé mobile et desktop
- **Polices monospace** (Courier New, Source Code Pro)

### 🔐 Authentification
- **JWT Tokens** sécurisés avec expiration
- **Hachage bcrypt** des mots de passe
- **Validation avancée** côté client et serveur
- **Sessions persistantes** avec gestion d'état

### 📊 Dashboard Analytics
- **Statistiques unifiées** combinant quiz classiques et IA
- **Graphiques de performance** avec Chart.js
- **Historique des sessions** avec distinction visuelle
- **Métriques détaillées** : scores, pourcentages, séries de réussite

---

## 🏗️ Architecture

### Stack Technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | FastAPI | 0.104+ |
| **Base de données** | PostgreSQL | 13+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Frontend** | HTML/CSS/JS | ES6+ |
| **Authentification** | JWT | python-jose |
| **Déploiement** | Docker | Compose v3.8 |
| **IA** | Analyse sémantique | Custom |

### Structure du Projet

```
project-holbies/
├── 🐍 Backend
│   ├── app/
│   │   ├── routers/          # Routes API (auth, quiz, ai_quiz, users)
│   │   ├── models.py         # Modèles SQLAlchemy + tables IA
│   │   ├── schemas.py        # Schémas Pydantic
│   │   ├── auth.py          # Authentification JWT
│   │   └── database.py      # Configuration PostgreSQL
│   └── main.py              # Point d'entrée FastAPI
├── 🌐 Frontend
│   ├── static/
│   │   ├── css/style.css    # Styles Matrix + animations
│   │   ├── js/              # Modules JavaScript
│   │   │   ├── ai-quiz.js   # Gestion AI Quiz
│   │   │   ├── dashboard.js # Analytics + graphiques
│   │   │   ├── quiz.js      # Quiz classiques
│   │   │   └── auth.js      # Authentification
│   │   ├── fonts/           # Polices Matrix (Aktiv Grotesk)
│   │   └── images/          # Assets visuels
│   └── templates/           # Templates Jinja2
├── 🗄️ Scripts
│   ├── populate_db_balanced.py  # Questions équilibrées
│   ├── create_admin.py          # Création admin
│   └── ai_quiz_corrector.py     # Correcteur IA
└── 🐳 Docker
    ├── Dockerfile
    └── docker-compose.yml
```

---

## 🌐 API Endpoints

### Authentification
```http
POST /api/auth/register     # Inscription utilisateur
POST /api/auth/token        # Connexion JWT
GET  /api/auth/me          # Profil utilisateur
```

### Quiz Classiques
```http
GET  /api/quiz/questions    # Liste des questions
POST /api/quiz/session      # Créer session
POST /api/quiz/submit       # Soumettre réponses
GET  /api/quiz/history      # Historique sessions
```

### AI Quiz (PLD)
```http
GET  /api/ai-quiz/questions      # Questions IA disponibles
POST /api/ai-quiz/session        # Créer session IA
POST /api/ai-quiz/submit-answer  # Soumettre réponse libre
GET  /api/ai-quiz/history        # Historique sessions IA
```

### Dashboard
```http
GET  /api/dashboard/stats        # Statistiques utilisateur
GET  /api/dashboard/performance  # Données graphiques
```

**📚 Documentation interactive** : http://localhost:8000/docs

---

## 🎯 Système AI Quiz

### 🧠 Fonctionnement de l'IA

Le correcteur IA analyse les réponses textuelles selon plusieurs critères :

#### Scoring Algorithm
```python
Score = (Similarité_Sémantique × 0.7) + (Termes_Techniques × 0.3) + Bonus_Technique

# Exemple :
# Réponse attendue : "La compilation C transforme le code source en exécutable"
# Réponse utilisateur : "Le compilateur convertit le C en programme exécutable"
# → Similarité: 85% + Termes: 3 détectés → Score: 95/100
```

#### Critères d'Évaluation
- **� Analyse sémantique** : Comparaison intelligente des concepts
- **🔧 Termes techniques** : Détection automatique et bonus (+5 pts/terme)
- **📝 Structure logique** : Cohérence de l'argumentation
- **💡 Feedback personnalisé** : Recommandations ciblées

### 📊 Types de Questions

| Difficulté | Points | Exemples |
|------------|--------|----------|
| 🟢 **Easy** | 100 | Définitions, concepts de base |
| 🟡 **Medium** | 100 | Applications pratiques, explications |
| 🔴 **Hard** | 100 | Algorithmes complexes, optimisation |

---

## 🎨 Configuration Thème

### Variables CSS Principales

```css
:root {
  /* Couleurs Matrix */
  --matrix-green: #00ff41;
  --matrix-dark: #0d1117;
  --secondary-green: #008f11;
  
  /* Animations */
  --glow-animation: matrix-glow 2s ease-in-out infinite alternate;
  --terminal-speed: 45ms;
  
  /* Typographie */
  --font-matrix: 'Courier New', monospace;
  --font-size-code: 18px;
}
```

### Personnalisation

```bash
# Modifier les couleurs
sed -i 's/#00ff41/#ff4500/g' static/css/style.css

# Changer la vitesse du terminal
sed -i 's/45ms/30ms/g' static/js/index.js
```

---

## 🧪 Tests et Validation

### Tests Automatiques

```bash
# Test de l'installation
python scripts/test_installation.py

# Test des endpoints API
python -m pytest tests/

# Test de la base de données
python scripts/reset_db.py && python scripts/populate_db_balanced.py
```

### Validation Manuelle

1. **Interface** : http://localhost:8000
2. **Authentification** : Créer compte + connexion
3. **Quiz classique** : Compléter un quiz
4. **AI Quiz** : Tester réponse libre
5. **Dashboard** : Vérifier statistiques

---

## 📈 Métriques et Analytics

### Dashboard Unifié

- **📊 Vue d'ensemble** : Total quiz + sessions IA combinées
- **📈 Graphique performance** : Évolution chronologique avec distinction visuelle
- **🎯 Métriques clés** : Score moyen, meilleur score, série actuelle
- **📋 Historique** : Sessions détaillées avec scores et feedback

### Exemples de Données

```json
{
  "stats": {
    "total_quizzes": 25,
    "total_ai_sessions": 12,
    "average_score": 78.5,
    "best_score": 95,
    "current_streak": 8
  },
  "performance": [
    {"date": "2025-01-15", "type": "quiz", "score": 80},
    {"date": "2025-01-16", "type": "ai_quiz", "score": 85}
  ]
}
```

---

## 🚀 Déploiement Production

### Docker Compose (Production)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${PRODUCTION_SECRET_KEY}
      - DATABASE_URL=${PRODUCTION_DB_URL}
    depends_on:
      - db
      
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: holbies_prod
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Variables d'Environnement

```env
# Production
DEBUG=False
SECRET_KEY=your-super-secret-production-key-256-bits
DATABASE_URL=postgresql://user:pass@db:5432/holbies_prod
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Performance
WORKERS=4
MAX_CONNECTIONS=100
```

### Nginx (Optionnel)

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /app/static/;
        expires 1y;
    }
}
```

---

## 🛠️ Développement

### Ajouter des Questions

#### Quiz Classique (QCM)
```python
# Dans scripts/populate_db_balanced.py
{
    "question_text": "Quelle est la complexité de QuickSort ?",
    "option_a": "O(n)",
    "option_b": "O(n log n)",
    "option_c": "O(n²)",
    "option_d": "O(log n)",
    "correct_answer": "b",
    "explanation": "QuickSort a une complexité moyenne de O(n log n)",
    "difficulty": "medium",
    "category": "algorithms"
}
```

#### AI Quiz (PLD)
```python
# Dans app/routers/ai_quiz.py
{
    "id": "memory-management-c",
    "question_text": "Expliquez la gestion mémoire en C avec malloc/free",
    "expected_answer": "malloc alloue dynamiquement, free libère, attention aux fuites",
    "technical_terms": ["malloc", "free", "heap", "pointeur", "fuite mémoire"],
    "difficulty": "hard",
    "category": "c-programming"
}
```

### Contribution

```bash
# 1. Fork du projet
git clone https://github.com/votre-username/project-holbies.git

# 2. Créer une branche
git checkout -b feature/nouvelle-fonctionnalite

# 3. Développement
# ... vos modifications ...

# 4. Tests
python scripts/test_installation.py

# 5. Commit et Push
git commit -am "Ajouter nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite

# 6. Pull Request
```

---

## 🎯 Roadmap

### ✅ Version 2.0 (Actuelle)
- [x] 🤖 Système AI Quiz avec correction intelligente
- [x] 📊 Dashboard unifié Quiz + IA
- [x] 🎨 Interface Matrix avec animations fluides
- [x] 🔐 Authentification JWT sécurisée
- [x] 📈 Analytics et graphiques de performance
- [x] 🐳 Déploiement Docker simplifié

### 🚧 Version 2.1 (En Cours)
- [ ] 🏆 Système de badges et récompenses
- [ ] ⏱️ Quiz chronométrés avec mode challenge
- [ ] 🥇 Classements et compétitions inter-utilisateurs
- [ ] 💻 Questions de code avec syntax highlighting
- [ ] 📱 Progressive Web App (PWA)
- [ ] 🔊 Effets sonores et musique Matrix

### 🔮 Version 2.2 (Futur)
- [ ] 👥 Mode multijoueur en temps réel
- [ ] 📁 Import/Export de questions (JSON, CSV)
- [ ] 🎨 Thèmes personnalisables (Cyberpunk, Retro)
- [ ] 🌍 Support multilingue (EN, FR, ES)
- [ ] ☁️ Sauvegarde cloud et synchronisation
- [ ] 🧠 IA améliorée avec GPT intégration

---

## 📞 Support & Communauté

### 🐛 Signaler un Bug
- **Issues GitHub** : [Créer un rapport](https://github.com/Krapaud/project-holbies/issues)
- **Template** : Utilisez le template de bug report
- **Labels** : bug, enhancement, question

### 💡 Demander une Fonctionnalité
- **Feature Request** : [Proposer une amélioration](https://github.com/Krapaud/project-holbies/issues)
- **Discussion** : Expliquez le besoin et l'usage attendu

### 🤝 Contribuer
1. 🍴 **Fork** le projet
2. 🌿 **Branch** : `git checkout -b feature/ma-fonctionnalite`
3. 💾 **Commit** : `git commit -am 'Ajouter ma fonctionnalité'`
4. 📤 **Push** : `git push origin feature/ma-fonctionnalite`
5. 🔄 **Pull Request** avec description détaillée

---

## 📄 Licence

```
MIT License

Copyright (c) 2025 Holbies Learning Hub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

**Créé avec ❤️ pour la communauté des développeurs**

🌟 **[Star ce projet](https://github.com/Krapaud/project-holbies)** si il vous a plu !  
🐛 **[Reportez les bugs](https://github.com/Krapaud/project-holbies/issues)** pour nous aider à améliorer  
💡 **[Proposez des améliorations](https://github.com/Krapaud/project-holbies/pulls)** via Pull Request

---

![Matrix Code](https://user-images.githubusercontent.com/placeholder/matrix-animation.gif)

*"There is no spoon... but there is code to learn!"* 🥄💊

</div>

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
git clone https://github.com/Krapaud/project-holbies.git
cd project-holbies
./scripts/start.sh
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

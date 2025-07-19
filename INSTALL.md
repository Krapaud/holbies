# Holbies Learning Hub - Installation et Configuration

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/holbies-learning-hub.git
cd holbies-learning-hub
```

2. **Lancer l'installation automatique**
```bash
./start.sh
```

Le script d'installation va :
- Créer un environnement virtuel Python
- Installer toutes les dépendances
- Configurer la base de données
- Peupler la base avec 50+ questions
- Démarrer le serveur

### Installation Manuelle

1. **Créer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données**
```bash
# Copier le fichier de configuration
cp .env.example .env

# Modifier .env avec vos paramètres PostgreSQL
nano .env
```

4. **Créer la base de données PostgreSQL**
```sql
CREATE DATABASE holbies_db;
CREATE USER holbies_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE holbies_db TO holbies_user;
```

5. **Créer les tables et peupler**
```bash
python3 -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
python3 populate_db.py
```

6. **Créer un utilisateur admin**
```bash
python3 create_admin.py
```

7. **Démarrer le serveur**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Accès à l'Application

- **Site principal** : http://localhost:8000
- **Connexion** : http://localhost:8000/login
- **Inscription** : http://localhost:8000/register
- **Quiz** : http://localhost:8000/quiz
- **Dashboard** : http://localhost:8000/dashboard
- **API Documentation** : http://localhost:8000/docs

## 🎮 Utilisation

### Pour les Étudiants

1. **S'inscrire** sur la plateforme
2. **Se connecter** avec ses identifiants
3. **Commencer un quiz** depuis la page d'accueil
4. **Suivre ses progrès** dans le dashboard

### Pour les Administrateurs

1. Utiliser le compte admin créé avec `create_admin.py`
2. Accéder à l'API documentation pour gérer les questions
3. Consulter les statistiques des utilisateurs

## 🔧 Configuration

### Variables d'Environnement (.env)

```env
# Base de données
DATABASE_URL=postgresql://holbies_user:password@localhost/holbies_db

# JWT
SECRET_KEY=votre-cle-secrete-tres-longue-et-complexe
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Structure de la Base de Données

- **users** : Informations des utilisateurs
- **questions** : Questions du quiz avec réponses
- **quiz_sessions** : Sessions de quiz des utilisateurs
- **quiz_answers** : Réponses données par les utilisateurs

## 🎨 Thème Matrix

Le site utilise un thème sombre inspiré de Matrix avec :
- Couleurs vertes néon (#00ff41)
- Police monospace (Source Code Pro)
- Effets de glitch et animations
- Particules flottantes
- Code rain animation

## 🧠 Système de Quiz

### Fonctionnalités

- **100+ questions** couvrant différents domaines :
  - Algorithmes et structures de données
  - Programmation (Python, C, JavaScript)
  - Web (HTML, CSS, HTTP/HTTPS)
  - Bases de données (SQL)
  - Systèmes (Linux, Git)
  - Sécurité

- **Correcteur automatique** avec explications
- **Suivi des performances** et statistiques
- **Sessions personnalisées** par utilisateur
- **Progression sauvegardée**

### Types de Questions

- Questions à choix multiples (QCM)
- 4 options par question
- Une seule réponse correcte
- Explications détaillées
- Catégorisation par difficulté

## 🔐 Sécurité

- **Authentification JWT** sécurisée
- **Hachage des mots de passe** avec bcrypt
- **Validation des entrées** côté client et serveur
- **Protection CORS** configurée
- **Variables d'environnement** pour les secrets

## 📊 API REST

L'API suit les principes REST avec les endpoints :

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/token` - Connexion

### Quiz
- `GET /api/quiz/questions` - Récupérer des questions
- `POST /api/quiz/start` - Démarrer une session
- `POST /api/quiz/submit-answer` - Soumettre une réponse
- `POST /api/quiz/complete/{session_id}` - Finaliser le quiz

### Utilisateurs
- `GET /api/users/me` - Informations utilisateur
- `GET /api/quiz/sessions` - Historique des sessions

## 🚀 Déploiement

### Développement
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Ou avec Gunicorn :
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (optionnel)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🛠️ Développement

### Ajouter des Questions

1. Modifier `populate_db.py`
2. Ajouter vos questions dans `QUIZ_QUESTIONS`
3. Relancer le script : `python3 populate_db.py`

### Structure du Code

```
holbies-learning-hub/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Authentification JWT
│   ├── database.py      # Configuration base de données
│   ├── models.py        # Modèles SQLAlchemy
│   ├── schemas.py       # Schémas Pydantic
│   └── routers/
│       ├── auth.py      # Routes authentification
│       ├── quiz.py      # Routes quiz
│       └── users.py     # Routes utilisateurs
├── static/
│   ├── css/style.css    # Styles Matrix
│   └── js/
│       ├── main.js      # Fonctions principales
│       ├── auth.js      # Authentification
│       ├── quiz.js      # Logique quiz
│       └── dashboard.js # Dashboard
├── templates/           # Templates HTML
├── main.py             # Point d'entrée FastAPI
└── requirements.txt    # Dépendances Python
```

## 🐛 Dépannage

### Erreurs Communes

1. **Erreur de connexion PostgreSQL**
   - Vérifier que PostgreSQL est en cours d'exécution
   - Vérifier les paramètres dans `.env`

2. **Erreur d'import Python**
   - Vérifier que l'environnement virtuel est activé
   - Réinstaller les dépendances : `pip install -r requirements.txt`

3. **Questions non affichées**
   - Relancer `python3 populate_db.py`
   - Vérifier la connexion à la base de données

### Logs

Les logs de l'application sont affichés dans la console lors du démarrage avec `--reload`.

## 📚 Technologies Utilisées

- **Backend** : FastAPI, SQLAlchemy, PostgreSQL
- **Frontend** : HTML5, CSS3 (Variables CSS), JavaScript (ES6+)
- **Authentification** : JWT avec python-jose
- **Sécurité** : bcrypt pour les mots de passe
- **Base de données** : PostgreSQL avec migrations Alembic
- **Thème** : CSS personnalisé Matrix avec animations

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🎯 Roadmap

- [ ] Système de badges et récompenses
- [ ] Quiz chronométrés
- [ ] Questions de code avec syntax highlighting
- [ ] Classements et compétitions
- [ ] Mode multijoueur
- [ ] Import/Export de questions
- [ ] Thèmes personnalisables
- [ ] Application mobile

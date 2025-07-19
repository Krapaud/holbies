# Quiz Langage C - API Flask

Une API Flask simple pour gérer un quiz de 100 questions sur le langage C.

## Structure du projet

```
flask_c_quiz/
├── app.py              # Application Flask principale
├── database.db         # Base de données SQLite (générée automatiquement)
├── init_db.py          # Script d'initialisation de la base de données
├── questions.py        # Liste des 100 questions sur le C
├── templates/
│   └── index.html      # Interface web simple (optionnelle)
└── README.md
```

## Installation et utilisation

### 1. Installer Flask

```bash
pip install flask
```

### 2. Initialiser la base de données

```bash
python init_db.py
```

### 3. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Endpoints de l'API

- `GET /` - Page d'accueil
- `GET /questions` - Récupérer toutes les questions
- `GET /question/<id>` - Récupérer une question spécifique par son ID

## Exemples d'utilisation

### Récupérer toutes les questions
```bash
curl http://localhost:5000/questions
```

### Récupérer une question spécifique
```bash
curl http://localhost:5000/question/1
```

## Questions couvertes

Le quiz couvre 10 catégories principales :
1. **Notions de base** (10 questions)
2. **Structures de contrôle** (10 questions)
3. **Tableaux et chaînes** (10 questions)
4. **Fonctions** (10 questions)
5. **Pointeurs** (10 questions)
6. **Fichiers** (10 questions)
7. **Structures et typedef** (10 questions)
8. **Compilation et erreurs** (10 questions)
9. **Arithmétique et logique** (10 questions)
10. **Concepts avancés** (10 questions)

## Interface web

Une interface web simple est disponible à l'adresse `http://localhost:5000/` pour visualiser toutes les questions.
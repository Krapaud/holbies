# Holbies Learning Hub

Un système de quiz interactif avec un thème Matrix pour l'apprentissage technique.

## Fonctionnalités

- Système d'authentification sécurisé
- Quiz de 100 questions style PLD Holberton School
- Interface web avec thème Matrix/geek sombre
- API FastAPI
- Base de données PostgreSQL
- Correcteur automatique

## Installation

1. Installer les dépendances Python :
```bash
pip install -r requirements.txt
```

2. Configurer la base de données PostgreSQL
3. Créer un fichier `.env` avec vos variables d'environnement
4. Lancer les migrations :
```bash
alembic upgrade head
```

5. Démarrer le serveur :
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Structure du projet

- `main.py` - Point d'entrée FastAPI
- `app/` - Code application
- `static/` - Fichiers CSS, JS, images
- `templates/` - Templates HTML
- `alembic/` - Migrations base de données

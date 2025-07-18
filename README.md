# hackaton
## 🚀 Fonctionnalités

### 🔐 Authentification
- Inscription et connexion sécurisées
- Mots de passe hashés avec salt
- Sessions sécurisées
- Gestion des rôles (Utilisateur/Administrateur)

### 🎨 Interface
- Thème geek sombre avec effets Matrix
- Design responsive et moderne
- Animations CSS et JavaScript
- Interface utilisateur intuitive

### ⚙️ Administration
- Panel d'administration complet
- Gestion des utilisateurs
- Statistiques en temps réel
- Contrôle d'accès basé sur les rôles

### 🛠️ Technologies
- **Backend**: Python/Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de données**: SQLite
- **Sécurité**: Werkzeug Security
- **Design**: CSS Grid, Flexbox, Animations

## 📋 Installation

### Prérequis
- Python 3.7+
- pip

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd dev-learning-hub
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 🔑 Comptes par défaut

### Administrateur
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@geeksite.com`

> ⚠️ **Important**: Changez ces identifiants en production !

## 📁 Structure du projet

```
dev-learning-hub/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── users.db              # Base de données SQLite (générée automatiquement)
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Tableau de bord utilisateur
│   ├── admin.html        # Panel d'administration
│   └── profile.html      # Page de profil
└── static/              # Fichiers statiques
    ├── css/
    │   └── style.css     # Styles CSS principaux
    └── js/
        ├── matrix.js     # Effets Matrix et animations
        └── main.js       # JavaScript principal
```

## 🎯 Fonctionnalités détaillées

### Interface utilisateur
- **Page d'accueil**: Présentation du site avec appels à l'action
- **Authentification**: Formulaires sécurisés avec validation
- **Dashboard**: Espace personnel avec statistiques
- **Profil**: Gestion des informations personnelles

### Administration
- **Gestion utilisateurs**: Voir, modifier, supprimer les comptes
- **Promotion/Rétrogradation**: Gérer les privilèges administrateur
- **Statistiques**: Vue d'ensemble des utilisateurs et activités
- **Sécurité**: Audit des connexions et actions

### Sécurité
- Mots de passe hashés avec SHA-256 et salt
- Protection CSRF
- Sessions sécurisées
- Validation côté serveur et client
- Contrôle d'accès granulaire

## 🎨 Thème et Design

### Palette de couleurs
- **Primaire**: `#00ff41` (Vert Matrix)
- **Secondaire**: `#00cc33` (Vert foncé)
- **Accent**: `#ff6b35` (Orange)
- **Arrière-plan**: `#0a0a0a` (Noir profond)
- **Cartes**: `#1e1e1e` (Gris foncé)

### Typographie
- **Principale**: JetBrains Mono (monospace)
- **Titres**: Orbitron (futuriste)

### Effets spéciaux
- Pluie de Matrix en arrière-plan
- Animations CSS fluides
- Effets de hover interactifs
- Notifications animées

## ⌨️ Raccourcis clavier

- `Ctrl + Shift + D`: Accéder au Dashboard
- `Ctrl + Shift + A`: Panel d'administration (si admin)
- `Ctrl + Shift + L`: Déconnexion
- `Échap`: Fermer les menus

## 🐛 Console Commands

Ouvrez la console développeur pour accéder aux commandes easter egg :

```javascript
konami()    // Animation rotation
matrix()    // Toggle Matrix rain
glitch()    // Effet glitch sur les titres
hack()      // Mode hacker visuel
```

## 📱 Responsive Design

Le site est entièrement responsive et s'adapte à :
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🔧 Configuration

### Variables d'environnement
```python
# Dans app.py
app.secret_key = 'votre_cle_secrete_super_securisee'  # À changer !
DATABASE = 'users.db'
```

### Base de données
La base de données SQLite est créée automatiquement au premier lancement avec :
- Table `users` avec tous les champs nécessaires
- Compte administrateur par défaut
- Index pour les performances

## 🚀 Déploiement

### Production
1. Changez la clé secrète dans `app.py`
2. Modifiez les identifiants admin par défaut
3. Configurez un serveur web (nginx + gunicorn)
4. Activez HTTPS
5. Configurez les sauvegardes de base de données

### Docker (optionnel)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
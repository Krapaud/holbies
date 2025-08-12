# 🚫 RESTRICTION - ENVIRONNEMENT VIRTUEL PYTHON

## ⚠️ **IMPORTANT : CE PROJET UTILISE DOCKER UNIQUEMENT**

### 🐳 **Utilisation Docker Obligatoire**
Ce projet Holbies est configuré pour fonctionner **EXCLUSIVEMENT avec Docker** et Docker Compose.

### 🚫 **Interdictions strictes :**
- ❌ **PAS d'environnement virtuel Python** (venv, virtualenv, conda, etc.)
- ❌ **PAS d'installation pip locale**
- ❌ **PAS de configure_python_environment**
- ❌ **PAS d'install_python_packages en local**

### ✅ **Méthodes autorisées :**
- ✅ **Docker Compose** : `docker-compose -f deployment/docker-compose.yml up --build`
- ✅ **Docker** : Toutes les dépendances sont gérées dans le conteneur
- ✅ **Makefile** : Utiliser les commandes Make si disponibles

### 📁 **Structure Docker du projet :**
```
deployment/
├── docker-compose.yml       ✅ Configuration principale
├── docker-compose.simple.yml ✅ Configuration simplifiée  
├── Dockerfile               ✅ Image de l'application
├── nginx.conf               ✅ Configuration Nginx
└── requirements.txt         ✅ Dépendances Python (dans le conteneur)
```

### 🚨 **En cas d'erreur :**
Si un environnement virtuel Python est créé par erreur :

1. **Supprimer immédiatement :**
   ```bash
   rm -rf .venv venv env __pycache__ *.pyc
   ```

2. **Utiliser Docker à la place :**
   ```bash
   docker-compose -f deployment/docker-compose.yml up --build
   ```

### 🎯 **Commandes Docker utiles :**
```bash
# Démarrer l'application
docker-compose -f deployment/docker-compose.yml up --build

# Arrêter l'application  
docker-compose -f deployment/docker-compose.yml down

# Reconstruire les conteneurs
docker-compose -f deployment/docker-compose.yml up --build --force-recreate

# Voir les logs
docker-compose -f deployment/docker-compose.yml logs -f

# Entrer dans le conteneur web
docker-compose -f deployment/docker-compose.yml exec web bash
```

### 📋 **Services Docker disponibles :**
- **web** : Application FastAPI (Python)
- **db** : Base de données PostgreSQL  
- **nginx** : Serveur web et proxy inverse

### 🌐 **Accès à l'application :**
- **URL principale** : http://localhost
- **Port** : 80 (via Nginx)
- **API** : http://localhost/api

---

**⚠️ RAPPEL : Toujours utiliser Docker pour ce projet !**

**Date de création :** 12 août 2025  
**Status :** 🔒 RESTRICTION ACTIVE

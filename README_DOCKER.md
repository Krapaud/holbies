# 🐳 DOCKER SETUP - Projet Holbies

## 🚀 Démarrage rapide

```bash
# Cloner le projet
git clone <repo-url>
cd project-holbies

# Démarrer avec Docker (UNIQUEMENT)
docker-compose -f deployment/docker-compose.yml up --build
```

## 🌐 Accès
- **Application** : http://localhost
- **API** : http://localhost/api

## ⚠️ IMPORTANT
**Ce projet utilise EXCLUSIVEMENT Docker !**

❌ **PAS d'environnement virtuel Python**  
✅ **Docker Compose OBLIGATOIRE**

Voir `DOCKER_ONLY_RESTRICTION.md` pour plus de détails.

## 🛠️ Commandes utiles

```bash
# Arrêter
docker-compose -f deployment/docker-compose.yml down

# Reconstruire
docker-compose -f deployment/docker-compose.yml up --build --force-recreate

# Logs
docker-compose -f deployment/docker-compose.yml logs -f

# Shell dans le conteneur
docker-compose -f deployment/docker-compose.yml exec web bash
```

## 📁 Structure
```
deployment/
├── docker-compose.yml    # 🐳 Configuration principale
├── Dockerfile           # 🐳 Image application
└── nginx.conf           # 🌐 Configuration Nginx
```

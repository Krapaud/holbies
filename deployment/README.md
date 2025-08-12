# Deployment Directory

Ce répertoire contient tous les fichiers nécessaires au déploiement de l'application Holbies Learning Platform avec Docker.

## 🚀 Démarrage Rapide

### Prérequis
- Docker Engine (version 20.10+)
- Docker Compose (version 2.0+)

### Lancement de l'application

```bash
# Option 1: Script de gestion (recommandé)
cd deployment
./docker-manager.sh start

# Option 2: Docker Compose direct
cd deployment
docker-compose up -d --build
```

L'application sera disponible sur :
- **Interface web (nginx)** : http://localhost:80
- **Interface web (direct)** : http://localhost:8000
- **Base de données** : localhost:5432

## 📁 Structure des fichiers

```
deployment/
├── Dockerfile                    # Configuration du conteneur application
├── docker-compose.yml           # Configuration multi-conteneurs complète
├── docker-manager.sh            # Script de gestion pratique
├── wait-for-postgres.sh         # Script d'attente PostgreSQL
├── nginx.conf                   # Configuration Nginx
├── init-db.sql                  # Script d'initialisation BDD
├── .env                         # Variables d'environnement (dev)
├── .env.example                 # Exemple de configuration
└── README.md                    # Ce fichier
```

## 🛠️ Script de Gestion

Le script `docker-manager.sh` offre une interface simple pour gérer l'application :

```bash
# Démarrer l'application
./docker-manager.sh start

# Arrêter l'application
./docker-manager.sh stop

# Redémarrer l'application
./docker-manager.sh restart

# Voir les logs en temps réel
./docker-manager.sh logs

# Vérifier l'état des services
./docker-manager.sh status

# Accéder au shell du conteneur web
./docker-manager.sh shell

# Accéder à la base de données
./docker-manager.sh db

# Nettoyage complet
./docker-manager.sh clean
```

## ⚙️ Configuration

### Variables d'environnement

Copiez `.env.example` vers `.env` et modifiez selon vos besoins :

```bash
cp .env.example .env
```

Variables importantes :
- `POSTGRES_PASSWORD` : Mot de passe de la base de données
- `SECRET_KEY` : Clé secrète pour l'application
- `DEBUG` : Mode debug (true/false)

### Configuration de production

Pour un déploiement en production :

1. **Sécurité** :
   - Changez tous les mots de passe par défaut
   - Générez une nouvelle `SECRET_KEY`
   - Désactivez le mode debug (`DEBUG=false`)

2. **Base de données** :
   - Utilisez des mots de passe forts
   - Configurez des sauvegardes automatiques
   - Limitez l'accès réseau

3. **Proxy inverse** :
   - Utilisez `docker-compose.yml` (avec nginx)
   - Configurez SSL/TLS
   - Ajustez les paramètres de cache

## 🐳 Configurations Docker

### Configuration complète (nginx + application)
Fichier : `docker-compose.yml`
- Application FastAPI + PostgreSQL + Nginx
- Proxy inverse avec cache et optimisations
- Accès via nginx (port 80) et direct (port 8000)
- Configuration recommandée pour développement et production

## 📊 Monitoring

### Vérification de l'état
```bash
# État des conteneurs
docker-compose ps

# Logs de l'application
docker-compose logs web

# Logs de nginx
docker-compose logs nginx

# Logs de la base de données
docker-compose logs db

# Utilisation des ressources
docker stats
```

### Tests de fonctionnement
```bash
# Test de l'API via nginx
curl -I http://localhost:80

# Test de l'API directe
curl -I http://localhost:8000

# Test de la page d'accueil
curl http://localhost:80

# Test de l'API des stats
curl http://localhost:80/quiz/stats
```

## 🔧 Dépannage

### Problèmes courants

**1. Erreur de connexion à la base de données**
```bash
# Vérifier l'état de PostgreSQL
./docker-manager.sh status

# Redémarrer les services
./docker-manager.sh restart
```

**2. Port déjà utilisé**
```bash
# Vérifier les ports utilisés
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :5432

# Arrêter l'application
./docker-manager.sh stop
```

**3. Problèmes de permissions**
```bash
# Reconstruire complètement
./docker-manager.sh clean
./docker-manager.sh start
```

**4. Logs détaillés**
```bash
# Logs en temps réel
./docker-manager.sh logs

# Logs spécifiques
```bash
# Logs spécifiques
docker-compose logs web -f
docker-compose logs nginx -f
```
```

## 🚀 Déploiement en production

La configuration actuelle avec nginx est déjà optimisée pour la production.

### Configuration SSL/TLS

1. Ajoutez vos certificats dans `deployment/ssl/`
2. Modifiez `nginx.conf` pour activer HTTPS
3. Redémarrez les services

### Sauvegarde des données

```bash
# Sauvegarde de la base de données
docker-compose exec db pg_dump -U holberton_user holberton_db > backup.sql

# Restauration
docker-compose exec -T db psql -U holberton_user holberton_db < backup.sql
```

## 📈 Performance

### Optimisations recommandées

1. **PostgreSQL** :
   - Ajustez `shared_buffers` et `effective_cache_size`
   - Configurez `max_connections` selon vos besoins
   - Activez le monitoring avec `pg_stat_statements`

2. **Application** :
   - Utilisez plusieurs workers uvicorn en production
   - Configurez la mise en cache appropriée
   - Optimisez les requêtes de base de données

3. **Nginx** :
   - Activez la compression gzip
   - Configurez le cache des fichiers statiques
   - Ajustez les timeouts selon vos besoins

## 🆘 Support

En cas de problème :

1. Vérifiez les logs : `./docker-manager.sh logs`
2. Vérifiez l'état : `./docker-manager.sh status`
3. Redémarrez : `./docker-manager.sh restart`
4. Nettoyage complet : `./docker-manager.sh clean && ./docker-manager.sh start`

Pour plus d'aide, consultez la documentation du projet principal.

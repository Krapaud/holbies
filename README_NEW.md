# 🎓 Holbies Learning Platform

![Holbies](https://img.shields.io/badge/Holberton-Learning%20Platform-0167b3)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed)
![Python](https://img.shields.io/badge/Python-3.11-3776ab)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)

Une plateforme d'apprentissage interactive avec thème Matrix, développée avec FastAPI et Docker.

## 🌟 Fonctionnalités

- ✅ **Quiz interactifs** avec système de scoring
- ✅ **IA intégrée** pour génération de questions personnalisées
- ✅ **Système d'authentification** sécurisé
- ✅ **Interface Matrix** avec animations CSS
- ✅ **Dashboard utilisateur** avec statistiques
- ✅ **API RESTful** complète
- ✅ **Responsive design** mobile-friendly

## 🚀 Démarrage rapide

### Docker (Recommandé)

```bash
# Cloner le projet
git clone https://github.com/Krapaud/project-holbies.git
cd project-holbies

# Lancer avec Docker
docker-compose -f deployment/docker-compose.yml up --build -d

# Accéder à l'application
open http://localhost:8000
```

### Google Cloud Platform (Étudiants)

```bash
# Configuration pour étudiants (0-7€/mois)
./deployment/gcp/scripts/setup-student.sh

# Déploiement
./deployment/gcp/scripts/deploy-student.sh
```

## 📁 Structure du projet

```
project-holbies/
├── 📂 src/                    # Code source principal
│   ├── main.py               # Point d'entrée FastAPI
│   ├── app/                  # Package application
│   │   ├── models.py         # Modèles de base de données
│   │   ├── routers/          # Routes API
│   │   └── auth.py           # Authentification
│   ├── static/               # Fichiers statiques (CSS, JS, images)
│   └── templates/            # Templates HTML
├── 📂 deployment/            # Configuration déploiement
│   ├── docker-compose.yml    # Docker local
│   ├── Dockerfile           # Image Docker
│   └── gcp/                 # Google Cloud Platform
├── 📂 config/               # Configuration
├── 📂 scripts/              # Scripts utilitaires
├── 📂 docs/                 # Documentation
└── 📂 tests/                # Tests automatisés
```

## 🛠️ Technologies

- **Backend** : FastAPI + SQLAlchemy + PostgreSQL
- **Frontend** : HTML5 + CSS3 + JavaScript (thème Matrix)
- **Conteneurisation** : Docker + Docker Compose
- **Cloud** : Google Cloud Platform (Cloud Run + Cloud SQL)
- **CI/CD** : GitHub Actions + Google Cloud Build

## 🔧 Configuration

### Variables d'environnement

Copiez et adaptez le fichier de configuration :

```bash
cp deployment/.env.example deployment/.env
```

### Base de données

Le projet utilise PostgreSQL via Docker :

```bash
# Réinitialiser la base de données
docker-compose down -v
docker-compose up --build -d
```

## 📚 Documentation

- 📖 [Guide d'installation](docs/INSTALL.md)
- 🏗️ [Architecture](docs/ARCHITECTURE_IA.md)
- 🚀 [Déploiement GCP](deployment/gcp/MIGRATION_GUIDE.md)
- 🎓 [Version étudiante](deployment/gcp/STUDENT_GUIDE.md)
- 🛠️ [Administration](docs/ADMIN_GUIDE.md)

## 🎓 Pour les étudiants

### Déploiement gratuit sur Google Cloud

Le projet propose une configuration spéciale pour étudiants :

- **Coût** : 0-7€/mois (vs 50-185€ version production)
- **300$ de crédits gratuits** pour nouveaux comptes GCP
- **GitHub Student Pack** : crédits supplémentaires
- **Fonctionnalités** : 95% identiques à la version production

```bash
# Configuration ultra-simple
./deployment/gcp/scripts/setup-student.sh
```

## 🧪 Tests

```bash
# Tests unitaires
docker-compose exec web python -m pytest

# Tests d'intégration
docker-compose exec web python -m pytest tests/integration/

# Coverage
docker-compose exec web python -m pytest --cov=src/
```

## 🔍 Développement

### Lancer en mode développement

```bash
# Mode développement avec rechargement automatique
docker-compose -f deployment/docker-compose.yml up --build

# Logs en temps réel
docker-compose logs -f web
```

### Structure de l'API

- `GET /` - Page d'accueil
- `GET /login` - Page de connexion
- `GET /register` - Page d'inscription
- `GET /profile` - Profil utilisateur
- `GET /pld` - Interface quiz PLD
- `POST /api/auth/*` - Endpoints d'authentification
- `GET/POST /api/quiz/*` - Gestion des quiz
- `GET/POST /api/pld/*` - API quiz PLD avec IA

## 🌍 Déploiement

### Local (Docker)
```bash
docker-compose -f deployment/docker-compose.yml up -d
```

### Production (GCP)
```bash
./deployment/gcp/scripts/setup-gcp.sh
./deployment/gcp/scripts/deploy.sh
```

### Staging
```bash
# Utiliser l'environnement de test
cp deployment/.env.example deployment/.env.staging
docker-compose -f deployment/docker-compose.yml up -d
```

## 📊 Monitoring

- **Logs** : `docker-compose logs -f`
- **Métriques** : Intégration Google Cloud Monitoring
- **Health checks** : `/health` endpoint
- **Database** : pgAdmin via `http://localhost:5050`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Krapaud** - *Développeur principal*

- GitHub: [@Krapaud](https://github.com/Krapaud)
- Projet: [project-holbies](https://github.com/Krapaud/project-holbies)

## 🙏 Remerciements

- Holberton School pour l'inspiration pédagogique
- La communauté FastAPI pour l'excellent framework
- Google Cloud Platform pour les outils cloud

---

⭐ N'hésitez pas à donner une étoile si ce projet vous aide !

## 🚨 Statut du projet

- ✅ **Version stable** : Application fonctionnelle
- ✅ **Docker** : Configuration prête pour production
- ✅ **GCP** : Migration cloud disponible
- ✅ **Tests** : Suite de tests automatisés
- ✅ **Documentation** : Complète et à jour

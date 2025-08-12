# 🐳 Makefile - Projet Holbies (Docker UNIQUEMENT)
# ⚠️  Ce projet utilise EXCLUSIVEMENT Docker - Pas d'environnement virtuel Python

.PHONY: help start stop restart build logs shell clean check-docker

# Aide par défaut
help:
	@echo "🐳 Projet Holbies - Docker UNIQUEMENT"
	@echo ""
	@echo "Commandes disponibles :"
	@echo "  make start     - Démarrer l'application avec Docker"
	@echo "  make stop      - Arrêter l'application"
	@echo "  make restart   - Redémarrer l'application"
	@echo "  make build     - Reconstruire les conteneurs"
	@echo "  make logs      - Voir les logs"
	@echo "  make shell     - Ouvrir un shell dans le conteneur web"
	@echo "  make clean     - Nettoyer Docker"
	@echo "  make check     - Vérifier la configuration Docker"
	@echo ""
	@echo "⚠️  RAPPEL : Pas d'environnement virtuel Python !"
	@echo "📄 Voir : DOCKER_ONLY_RESTRICTION.md"

# Vérification Docker
check-docker:
	@echo "🔍 Vérification Docker..."
	@docker --version || (echo "❌ Docker non installé !" && exit 1)
	@docker-compose --version || (echo "❌ Docker Compose non installé !" && exit 1)
	@echo "✅ Docker OK"

# Démarrer l'application
start: check-docker
	@echo "🚀 Démarrage de l'application avec Docker..."
	docker-compose -f deployment/docker-compose.yml up --build

# Arrêter l'application
stop:
	@echo "🛑 Arrêt de l'application..."
	docker-compose -f deployment/docker-compose.yml down

# Redémarrer l'application
restart: stop start

# Reconstruire les conteneurs
build: check-docker
	@echo "🔨 Reconstruction des conteneurs..."
	docker-compose -f deployment/docker-compose.yml up --build --force-recreate

# Voir les logs
logs:
	@echo "📋 Affichage des logs..."
	docker-compose -f deployment/docker-compose.yml logs -f

# Shell dans le conteneur
shell:
	@echo "🐚 Ouverture d'un shell dans le conteneur web..."
	docker-compose -f deployment/docker-compose.yml exec web bash

# Nettoyage Docker
clean:
	@echo "🧹 Nettoyage Docker..."
	docker-compose -f deployment/docker-compose.yml down --remove-orphans
	docker system prune -f

# Vérification de la configuration
check: check-docker
	@echo "🔍 Vérification de la configuration..."
	@test -f deployment/docker-compose.yml || (echo "❌ docker-compose.yml introuvable !" && exit 1)
	@test -f deployment/Dockerfile || (echo "❌ Dockerfile introuvable !" && exit 1)
	@test ! -d .venv || (echo "⚠️  Environnement virtuel détecté - Supprimer avec: rm -rf .venv" && exit 1)
	@test ! -d venv || (echo "⚠️  Environnement virtuel détecté - Supprimer avec: rm -rf venv" && exit 1)
	@echo "✅ Configuration OK"

# Commande par défaut
default: help
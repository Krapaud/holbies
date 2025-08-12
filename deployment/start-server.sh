#!/bin/bash

# Script de démarrage pour le serveur Docker
# Ce script configure et démarre l'application avec Docker Compose

set -e

echo "🚀 Démarrage du serveur Holbies Learning Hub"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker et Docker Compose."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose."
    exit 1
fi

# Se déplacer vers le répertoire de déploiement
cd "$(dirname "$0")"

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env à partir de .env.example"
    cp .env.example .env
    echo "⚠️  IMPORTANT: Modifiez le fichier deployment/.env avec vos propres valeurs!"
    echo "   Particulièrement les mots de passe et clés secrètes."
fi

# Arrêter les conteneurs existants
echo "🔄 Arrêt des conteneurs existants..."
docker-compose down

# Construire et démarrer les services
echo "🔨 Construction et démarrage des services..."
docker-compose up --build -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 10

# Vérifier l'état des services
echo "📊 État des services:"
docker-compose ps

# Afficher les logs en arrière-plan
echo "📋 Logs en temps réel (Ctrl+C pour arrêter l'affichage):"
echo "   Application web (nginx): http://localhost:80"
echo "   Application web (direct): http://localhost:8000"
echo "   PostgreSQL: localhost:5432"
echo ""
echo "🔍 Pour voir les logs:"
echo "   docker-compose logs -f web"
echo "   docker-compose logs -f nginx"
echo "   docker-compose logs -f db"
echo ""
echo "⏹️  Pour arrêter l'application:"
echo "   docker-compose down"

# Suivre les logs
docker-compose logs -f

#!/bin/bash
# 🔍 Script de vérification Docker-only pour projet Holbies

echo "🔍 Vérification de la configuration Docker-only..."
echo ""

# Vérifier Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker installé : $(docker --version)"
else
    echo "❌ Docker non installé !"
    exit 1
fi

# Vérifier Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose installé : $(docker-compose --version)"
else
    echo "❌ Docker Compose non installé !"
    exit 1
fi

# Vérifier fichiers Docker
if [ -f "deployment/docker-compose.yml" ]; then
    echo "✅ docker-compose.yml présent"
else
    echo "❌ deployment/docker-compose.yml introuvable !"
    exit 1
fi

if [ -f "deployment/Dockerfile" ]; then
    echo "✅ Dockerfile présent"
else
    echo "❌ deployment/Dockerfile introuvable !"
    exit 1
fi

# Vérifier absence d'environnements virtuels
if [ -d ".venv" ] || [ -d "venv" ] || [ -d "env" ]; then
    echo "⚠️  ATTENTION : Environnement virtuel Python détecté !"
    echo "   Supprimer avec : rm -rf .venv venv env"
    echo "   Ce projet utilise UNIQUEMENT Docker !"
    exit 1
else
    echo "✅ Aucun environnement virtuel détecté"
fi

# Vérifier restrictions
if [ -f "DOCKER_ONLY_RESTRICTION.md" ]; then
    echo "✅ Fichier de restrictions présent"
else
    echo "⚠️  Fichier de restrictions manquant"
fi

echo ""
echo "🎉 Configuration Docker-only validée !"
echo ""
echo "🚀 Pour démarrer l'application :"
echo "   docker-compose -f deployment/docker-compose.yml up --build"
echo ""
echo "📄 Voir DOCKER_ONLY_RESTRICTION.md pour plus d'infos"

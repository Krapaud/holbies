#!/bin/bash

echo "🤖 Installation IA GRATUITE - Hugging Face Transformers"
echo "======================================================"
echo ""
echo "Cette installation ajoute:"
echo "✅ Hugging Face Transformers (modèles IA gratuits)"
echo "✅ PyTorch (moteur IA)"
echo "✅ Modèles de langage français"
echo "✅ 100% GRATUIT - Aucun coût"
echo ""
echo "Espace requis: ~3 GB (modèles + dépendances)"
echo ""

read -p "Voulez-vous continuer ? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Installation annulée"
    exit 1
fi

echo "📦 Installation des dépendances IA..."

# Installer dans le container Docker
echo "� Installation dans le container Docker..."
cd /home/krapaud/project-holbies/deployment

# Reconstruire l'image avec les dépendances IA
echo "🔧 Reconstruction de l'image Docker avec IA..."
docker-compose build --no-cache web

# Redémarrer les services
echo "🚀 Redémarrage des services..."
docker-compose down
docker-compose up -d

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🤖 Votre système utilise maintenant l'IA Hugging Face !"
echo "📊 Les feedbacks sont générés par des modèles de langage"
echo "💡 Vérifiez les logs: docker-compose logs web"
echo ""
echo "🌐 Testez sur: http://localhost/pld.html"
echo ""
echo "📋 Vérification du chargement IA:"
echo "docker-compose logs web | grep 'Hugging Face'"
echo ""

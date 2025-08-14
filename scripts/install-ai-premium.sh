#!/bin/bash

# Script pour activer le feedback IA premium avec OpenAI

echo "🤖 Installation du feedback IA premium..."
echo "⚠️  ATTENTION: Ceci activera l'utilisation de l'API OpenAI (payante)"
echo "💰 Coût estimé: ~0.001€ par feedback généré"
echo ""

read -p "Voulez-vous continuer ? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Installation annulée"
    exit 1
fi

echo "📦 Installation d'OpenAI..."
pip install openai==1.6.1

echo ""
echo "🔑 Configuration de la clé API..."
echo "1. Allez sur https://platform.openai.com/api-keys"
echo "2. Créez une nouvelle clé API"
echo "3. Ajoutez-la dans le fichier .env:"
echo "   OPENAI_API_KEY=sk-votre-cle-ici"
echo ""
echo "📊 Monitoring des coûts:"
echo "   - Surveillez sur https://platform.openai.com/usage"
echo "   - Configurez des limites de dépenses"
echo ""
echo "✅ Installation terminée !"
echo "🔄 Redémarrez le serveur pour activer le feedback IA premium"

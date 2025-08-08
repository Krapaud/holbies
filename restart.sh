#!/bin/bash

# Script de redémarrage pour Holbies Learning Hub

echo "🔄 Redémarrage de Holbies Learning Hub..."

# Arrêter les processus existants
echo "Arrêt des processus FastAPI existants..."
pkill -f "uvicorn main:app"

# Attendre un court instant pour que les ports se libèrent
sleep 2

# Lancer le script de démarrage
./start.sh

echo "✅ Redémarrage terminé."

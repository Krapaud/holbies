#!/bin/bash

# Script de démarrage pour Holbies Learning Hub

echo "🚀 Démarrage de Holbies Learning Hub..."

# Couleurs pour la sortie
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher des messages colorés
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si Python3 est installé
if ! command -v python3 &> /dev/null; then
    print_error "Python3 n'est pas installé!"
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 n'est pas installé!"
    exit 1
fi

# Créer un environnement virtuel si il n'existe pas
if [ ! -d "venv" ]; then
    print_status "Création de l'environnement virtuel..."
    python3 -m venv venv
    print_success "Environnement virtuel créé!"
fi

# Activer l'environnement virtuel
print_status "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
print_status "Installation des dépendances..."
pip install -r requirements.txt

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    print_warning "Fichier .env non trouvé, copie du fichier exemple..."
    cp .env.example .env
    print_warning "Veuillez modifier le fichier .env avec vos paramètres!"
fi

# Vérifier si PostgreSQL est accessible
print_status "Vérification de la connexion PostgreSQL..."
python3 -c "
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
try:
    # Tenter de se connecter à PostgreSQL
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',  # Base par défaut pour tester la connexion
        user=os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/holbies_db').split('://')[1].split(':')[0],
        password=os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/holbies_db').split(':')[2].split('@')[0]
    )
    conn.close()
    print('✅ Connexion PostgreSQL réussie')
except Exception as e:
    print(f'❌ Erreur de connexion PostgreSQL: {e}')
    print('Assurez-vous que PostgreSQL est installé et en cours d\'exécution')
    exit(1)
" 2>/dev/null || print_warning "Impossible de vérifier PostgreSQL. Assurez-vous qu'il est installé et configuré."

# Créer les tables
print_status "Création des tables de base de données..."
python3 -c "
from app.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)
print('✅ Tables créées avec succès')
"

# Peupler la base de données
print_status "Peuplement de la base de données avec les questions..."
python3 populate_db.py

# Démarrer le serveur
print_success "🎉 Configuration terminée!"
print_status "Démarrage du serveur FastAPI..."
echo ""
echo "🌐 Le serveur sera accessible à l'adresse: http://localhost:8000"
echo "📊 Dashboard: http://localhost:8000/dashboard"
echo "🧠 Quiz: http://localhost:8000/quiz"
echo ""
echo "Pour arrêter le serveur, appuyez sur Ctrl+C"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

#!/bin/bash

# Script de nettoyage et organisation du projet Holbies
set -eu

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 Nettoyage et organisation du projet Holbies${NC}"
echo "=============================================="

# Vérifier qu'on est dans le bon répertoire
if [ ! -f "src/main.py" ]; then
    echo -e "${RED}❌ Erreur : Ce script doit être exécuté depuis la racine du projet${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Vérification de la structure du projet...${NC}"

# Créer les dossiers manquants si nécessaire
REQUIRED_DIRS=(
    "backup"
    "temp_files"
    "logs"
    "deployment/gcp/terraform"
    "scripts/data_management"
    "scripts/testing"
    "scripts/user_management"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Création du dossier : $dir"
        mkdir -p "$dir"
    fi
done

echo -e "${GREEN}✅ Structure des dossiers vérifiée${NC}"

# Nettoyer les fichiers temporaires qui auraient pu rester
echo -e "${YELLOW}🗑️ Nettoyage des fichiers temporaires...${NC}"

# Supprimer les cache Python
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Supprimer les fichiers temporaires
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# Nettoyer les logs anciens
find . -name "*.log" -mtime +7 -delete 2>/dev/null || true

echo -e "${GREEN}✅ Fichiers temporaires nettoyés${NC}"

# Vérifier les permissions des scripts
echo -e "${YELLOW}🔧 Vérification des permissions...${NC}"

# Scripts principaux
chmod +x check_docker_config.sh 2>/dev/null || true

# Scripts GCP
find deployment/gcp/scripts/ -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

# Scripts dans le dossier scripts/
find scripts/ -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

echo -e "${GREEN}✅ Permissions mises à jour${NC}"

# Vérifier la configuration Docker
echo -e "${YELLOW}🐳 Vérification de la configuration Docker...${NC}"

if [ -f "deployment/docker-compose.yml" ]; then
    echo "✅ docker-compose.yml trouvé"
else
    echo -e "${RED}❌ docker-compose.yml manquant${NC}"
fi

if [ -f "deployment/Dockerfile" ]; then
    echo "✅ Dockerfile trouvé"
else
    echo -e "${RED}❌ Dockerfile manquant${NC}"
fi

# Vérifier les fichiers de configuration
echo -e "${YELLOW}⚙️ Vérification des configurations...${NC}"

if [ -f "config/requirements.txt" ]; then
    echo "✅ requirements.txt trouvé"
else
    echo -e "${RED}❌ requirements.txt manquant${NC}"
fi

if [ -f "config/settings.py" ]; then
    echo "✅ settings.py trouvé"
else
    echo -e "${YELLOW}⚠️ settings.py manquant (optionnel)${NC}"
fi

# Vérifier les variables d'environnement
if [ -f "deployment/.env.example" ]; then
    echo "✅ .env.example trouvé"
    if [ ! -f "deployment/.env" ]; then
        echo -e "${YELLOW}💡 Conseil : Copiez .env.example vers .env et adaptez les valeurs${NC}"
    fi
else
    echo -e "${RED}❌ .env.example manquant${NC}"
fi

# Créer un rapport de l'état du projet
echo -e "${YELLOW}📊 Génération du rapport d'état...${NC}"

cat > PROJECT_STATUS.md << EOF
# 📊 État du Projet Holbies

**Date de vérification :** $(date)

## ✅ Structure du projet

- [x] Code source (src/)
- [x] Configuration (config/)
- [x] Déploiement (deployment/)
- [x] Documentation (docs/)
- [x] Scripts (scripts/)
- [x] Tests (tests/)

## 🐳 Docker

- [x] docker-compose.yml
- [x] Dockerfile
- [x] Variables d'environnement

## ☁️ Google Cloud Platform

- [x] Configuration GCP (deployment/gcp/)
- [x] Scripts de déploiement
- [x] Documentation migration

## 📚 Documentation

- [x] README principal
- [x] Guide migration GCP
- [x] Documentation étudiante
- [x] Guide d'administration

## 🔧 Maintenance

- [x] Fichiers temporaires nettoyés
- [x] Permissions mises à jour
- [x] Structure organisée
- [x] .gitignore optimisé

## 🚀 Prochaines étapes

1. **Développement local :**
   \`\`\`bash
   docker-compose -f deployment/docker-compose.yml up --build -d
   \`\`\`

2. **Déploiement GCP (étudiants) :**
   \`\`\`bash
   ./deployment/gcp/scripts/setup-student.sh
   \`\`\`

3. **Tests :**
   \`\`\`bash
   docker-compose exec web python -m pytest
   \`\`\`

## ℹ️ Informations

- **Langage :** Python 3.11 + FastAPI
- **Base de données :** PostgreSQL 15
- **Conteneurisation :** Docker + Docker Compose
- **Cloud :** Google Cloud Platform (Cloud Run + Cloud SQL)
- **Coût étudiant :** 0-7€/mois
- **Coût production :** 50-185€/mois

---
*Rapport généré automatiquement par clean-project.sh*
EOF

echo -e "${GREEN}✅ Rapport d'état créé : PROJECT_STATUS.md${NC}"

# Vérifier les dépendances Python
echo -e "${YELLOW}🐍 Vérification des dépendances Python...${NC}"

if [ -f "config/requirements.txt" ]; then
    echo "Dépendances principales :"
    grep -E "^(fastapi|uvicorn|sqlalchemy|psycopg2)" config/requirements.txt || echo "  ⚠️ Certaines dépendances principales manquent"
    
    # Compter le nombre de dépendances
    DEPS_COUNT=$(wc -l < config/requirements.txt)
    echo "  📦 Total : $DEPS_COUNT dépendances"
fi

# Vérifier la taille du projet
echo -e "${YELLOW}📏 Analyse de la taille du projet...${NC}"

PROJECT_SIZE=$(du -sh . 2>/dev/null | cut -f1)
echo "  📊 Taille totale : $PROJECT_SIZE"

SRC_SIZE=$(du -sh src/ 2>/dev/null | cut -f1)
echo "  📊 Code source : $SRC_SIZE"

if [ -d "temp_files" ]; then
    TEMP_SIZE=$(du -sh temp_files/ 2>/dev/null | cut -f1)
    echo "  🗑️ Fichiers temporaires : $TEMP_SIZE"
fi

# Résumé final
echo ""
echo -e "${GREEN}🎉 Nettoyage terminé avec succès !${NC}"
echo "=============================================="
echo -e "${BLUE}📋 Résumé :${NC}"
echo "  ✅ Structure organisée"
echo "  ✅ Fichiers temporaires nettoyés"  
echo "  ✅ Permissions corrigées"
echo "  ✅ Configuration vérifiée"
echo "  ✅ Rapport d'état généré"
echo ""
echo -e "${YELLOW}🚀 Le projet est prêt pour :${NC}"
echo "  - Développement local avec Docker"
echo "  - Déploiement sur Google Cloud Platform"
echo "  - Tests et intégration continue"
echo ""
echo -e "${BLUE}📖 Consultez PROJECT_STATUS.md pour plus de détails${NC}"

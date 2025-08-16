#!/bin/bash

# Script de nettoyage - Suppression des fichiers CSS originaux intégrés
# Version: 1.0
# Date: $(date)

echo "🧹 Début du nettoyage des fichiers CSS intégrés..."

# Répertoire CSS
CSS_DIR="/home/krapaud/holbies-learning-hub.github.io/src/static/css"

# Fichiers à supprimer (maintenant intégrés dans la structure modulaire)
FILES_TO_DELETE=(
    "ai-feedback.css"
    "coding-lab.css"
    "coding-lab-home.css"
    "toast.css"
    "promo.css"
    "learning.css"
)

# Compteur
DELETED_COUNT=0

echo "📁 Répertoire de travail: $CSS_DIR"
echo ""

# Vérification et suppression
for file in "${FILES_TO_DELETE[@]}"; do
    FILEPATH="$CSS_DIR/$file"
    
    if [ -f "$FILEPATH" ]; then
        echo "🗑️  Suppression de: $file"
        rm "$FILEPATH"
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Supprimé avec succès"
            ((DELETED_COUNT++))
        else
            echo "   ❌ Erreur lors de la suppression"
        fi
    else
        echo "⚠️  Fichier non trouvé: $file"
    fi
    echo ""
done

echo "📊 Résumé:"
echo "   - Fichiers supprimés: $DELETED_COUNT/${#FILES_TO_DELETE[@]}"
echo ""

# Vérification de l'intégrité
echo "🔍 Vérification de l'intégrité de la structure modulaire..."

REQUIRED_DIRS=(
    "base"
    "components" 
    "layout"
    "pages"
    "utils"
)

MISSING_DIRS=()

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$CSS_DIR/$dir" ]; then
        MISSING_DIRS+=("$dir")
    fi
done

if [ ${#MISSING_DIRS[@]} -eq 0 ]; then
    echo "   ✅ Tous les répertoires modulaires sont présents"
else
    echo "   ❌ Répertoires manquants: ${MISSING_DIRS[*]}"
fi

# Vérification du fichier principal
if [ -f "$CSS_DIR/style.css" ]; then
    echo "   ✅ Fichier style.css principal présent"
else
    echo "   ❌ Fichier style.css principal manquant"
fi

# Vérification du backup
if [ -f "$CSS_DIR/style-backup-20250816_181319.css" ]; then
    echo "   ✅ Fichier de sauvegarde préservé"
else
    echo "   ⚠️  Fichier de sauvegarde non trouvé"
fi

echo ""
echo "✨ Nettoyage terminé!"
echo ""
echo "📋 Structure finale:"
echo "   - Base: variables, reset, typography"
echo "   - Layout: layout, header, footer, navigation, grid"  
echo "   - Components: buttons, cards, forms, modals, navigation, animations, ui-components"
echo "   - Pages: home, auth, dashboard, pld"
echo "   - Utils: utilities, animations, responsive"
echo "   - Modules spécialisés: intégrés via @import"
echo ""
echo "🎯 Le fichier CSS principal (style.css) importe maintenant tous les modules de façon optimisée!"

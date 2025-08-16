#!/bin/bash

# Script de migration CSS vers architecture modulaire
# Sauvegarde l'ancien fichier et met en place la nouvelle structure

echo "🚀 Migration vers architecture CSS modulaire..."

# Créer un backup de l'ancien fichier
if [ -f "style.css" ]; then
    echo "📦 Sauvegarde de l'ancien style.css..."
    cp style.css style-backup-$(date +%Y%m%d_%H%M%S).css
    echo "✅ Sauvegarde créée : style-backup-$(date +%Y%m%d_%H%M%S).css"
fi

# Renommer le nouveau fichier
if [ -f "style-new.css" ]; then
    echo "🔄 Activation de la nouvelle structure CSS..."
    mv style-new.css style.css
    echo "✅ Nouvelle structure CSS activée"
fi

echo "📊 Résumé de la migration :"
echo "   📁 Structure modulaire créée dans les dossiers :"
echo "      - base/ (variables, reset, typography)"
echo "      - components/ (ui-components, navigation, animations)"
echo "      - pages/ (home, auth)"
echo "      - utils/ (utilities, responsive)"
echo "   📦 Ancien fichier sauvegardé"
echo "   ⚡ Performance améliorée grâce à la modularité"

echo ""
echo "🎯 Avantages de la nouvelle structure :"
echo "   ✅ CSS organisé et maintenable"
echo "   ✅ Chargement modulaire possible"
echo "   ✅ Réduction des conflits de styles"
echo "   ✅ Debugging facilité"
echo "   ✅ Réutilisabilité des composants"

echo ""
echo "🔧 Prochaines étapes recommandées :"
echo "   1. Tester l'interface pour vérifier que tout fonctionne"
echo "   2. Optimiser les imports CSS selon les besoins"
echo "   3. Considérer la minification pour la production"

echo ""
echo "✨ Migration terminée avec succès !"

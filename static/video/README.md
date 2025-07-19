# Dossier Vidéo de Bienvenue

## Instructions pour ajouter votre vidéo

1. **Placez votre fichier vidéo** dans ce dossier avec le nom `welcome.mp4`
   - Formats supportés : MP4, WebM, OGV
   - Taille recommandée : Maximum 50MB pour un chargement rapide
   - Résolution recommandée : 1280x720 ou 1920x1080

2. **Formats alternatifs** (optionnel pour compatibilité)
   - `welcome.webm` pour les navigateurs modernes
   - `welcome.ogv` pour Firefox plus ancien

## Fonctionnement

- La vidéo se lance automatiquement après une connexion réussie
- Elle s'affiche en plein écran avec un style Matrix
- Se ferme automatiquement à la fin
- L'utilisateur peut la fermer manuellement avec le bouton X ou Escape
- Si aucune vidéo n'est trouvée, l'utilisateur est redirigé directement vers le dashboard

## Exemples de fichiers à placer ici

```
static/video/
├── welcome.mp4     (fichier principal)
├── welcome.webm    (optionnel)
└── welcome.ogv     (optionnel)
```

## Test

Pour tester sans vidéo, le système passera automatiquement au dashboard.
Pour ajouter une vidéo de test rapide, vous pouvez utiliser n'importe quel fichier MP4.

## Modification du chemin

Si vous voulez changer le nom ou l'emplacement de la vidéo, modifiez la ligne dans `/static/js/auth.js` :

```javascript
const videoPath = '/static/video/welcome.mp4'; // Changez ce chemin
```

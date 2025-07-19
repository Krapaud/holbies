# Guide d'utilisation du CSS Global - Holbies Learning Hub

## Vue d'ensemble

Le fichier `/static/css/global.css` centralise tous les styles du site Holbies Learning Hub pour une maintenance plus facile et une cohérence visuelle optimale.

## Structure du fichier

### 1. Variables CSS (Thème Matrix)
```css
:root {
    --primary-green: #00ff41;
    --secondary-green: #008f11;
    --matrix-black: #0d1117;
    --matrix-dark: #161b22;
    /* ... autres variables */
}
```

### 2. Sections principales

#### Base et Reset
- Reset CSS universel
- Styles de base pour `body`, `html`
- Animation de fond Matrix

#### Navigation
- `.navbar` - Barre de navigation fixe
- `.nav-menu` - Menu principal
- `.nav-link` - Liens de navigation avec effets hover

#### Typography
- Styles pour les titres (H1-H6)
- Police principale : `Source Code Pro`
- Police des titres : `Orbitron`

#### Composants principaux

**Boutons**
- `.btn` - Classe de base
- `.btn-primary` - Bouton principal (vert Matrix)
- `.btn-secondary` - Bouton secondaire (contour vert)

**Pages spécifiques**
- **Home** : `.hero`, `.features`, `.stats`
- **Auth** : `.auth-section`, `.auth-card`, `.auth-form`
- **Quiz** : `.quiz-section`, `.quiz-content`, `.question-options`
- **Tutor** : `.tutor-container`, `.toolbar`, `.code-input`
- **Dashboard** : `.dashboard-section`, `.stat-card`

**Modales**
- `.modal` - Conteneur de modale
- `.modal-content` - Contenu de la modale
- `.modal-header`, `.modal-body`, `.modal-footer`

#### Utilitaires
- `.hidden` - Masquer un élément
- `.text-center` - Centrer le texte
- `.text-success`, `.text-danger`, `.text-warning` - Couleurs de texte
- Marges : `.mb-1`, `.mb-2`, `.mt-1`, `.mt-2`, etc.

## Comment utiliser

### 1. Dans les templates HTML

**✅ Recommandé** - Utilisez les classes du CSS global :
```html
{% extends "base.html" %}
{% block content %}
<div class="tutor-container">
    <div class="tutor-header">
        <h1>Mon titre</h1>
    </div>
    <button class="btn btn-primary">Action</button>
</div>
{% endblock %}
```

**❌ Évitez** - CSS inline dans les templates :
```html
{% block extra_css %}
<style>
    .mon-style { /* ... */ }
</style>
{% endblock %}
```

### 2. Ajout de nouveaux styles

Si vous devez ajouter de nouveaux styles :

1. **Ajoutez-les dans `global.css`** dans la section appropriée
2. **Utilisez les variables CSS** existantes pour la cohérence
3. **Suivez la convention de nommage** Matrix/cyberpunk

```css
/* Nouvelle section dans global.css */
.nouvelle-fonctionnalite {
    background: var(--matrix-dark);
    border: 1px solid var(--primary-green);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-glow);
}
```

### 3. Responsive Design

Le fichier inclut des media queries pour :
- `@media (max-width: 768px)` - Tablettes
- `@media (max-width: 480px)` - Mobiles

## Avantages

### ✅ Avantages du CSS centralisé

1. **Maintenance facile** - Un seul fichier à modifier
2. **Cohérence visuelle** - Variables CSS partagées
3. **Performance** - Un seul fichier CSS à charger
4. **Réutilisabilité** - Classes disponibles partout
5. **Debugging simplifié** - Tous les styles au même endroit

### ❌ Problèmes évités

1. **Duplication de code** - Fini les styles répétés
2. **Incohérences** - Variables unifiées
3. **Surcharge CSS** - Plus de `!important` partout
4. **Maintenance difficile** - Plus de CSS éparpillé

## Intégration dans les templates

Le fichier est automatiquement chargé via `base.html` :

```html
<!-- Dans base.html -->
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="/static/css/global.css">
```

## Exemple d'usage complet

```html
<!-- Template simplifié utilisant le CSS global -->
{% extends "base.html" %}

{% block content %}
<section class="auth-section">
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-header">
                <h1 class="auth-title">Nouvelle fonctionnalité</h1>
                <p class="auth-subtitle">Description</p>
            </div>
            
            <form class="auth-form">
                <div class="form-group">
                    <label>Label</label>
                    <input type="text" placeholder="Texte">
                </div>
                
                <button class="btn btn-primary btn-full">
                    Valider
                </button>
            </form>
        </div>
    </div>
</section>
{% endblock %}
```

## Migration des templates existants

Pour migrer un template existant :

1. **Supprimez le bloc `{% block extra_css %}`**
2. **Remplacez les styles inline par les classes globales**
3. **Vérifiez que l'apparence est conservée**
4. **Testez le responsive**

## Classes principales à retenir

| Composant | Classe principale | Description |
|-----------|------------------|-------------|
| Container | `.tutor-container`, `.quiz-container` | Conteneurs principaux |
| Headers | `.tutor-header`, `.auth-header` | En-têtes de section |
| Buttons | `.btn`, `.btn-primary`, `.btn-secondary` | Boutons stylisés |
| Forms | `.form-group`, `.auth-form` | Formulaires |
| Cards | `.feature-card`, `.stat-card` | Cartes de contenu |
| Modals | `.modal`, `.modal-content` | Modales |

## Support et maintenance

- **Variables** : Modifiez les variables CSS pour changer le thème
- **Nouvelles sections** : Ajoutez-les en fin de fichier avec commentaires
- **Debugging** : Utilisez les DevTools pour inspecter les classes
- **Performance** : Le fichier est optimisé pour le cache navigateur

---

*Ce guide sera mis à jour avec l'évolution du projet.*

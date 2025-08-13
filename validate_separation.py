#!/usr/bin/env python3
"""
Script de validation pour la séparation HTML/JS
"""

import re
import os

def check_html_template():
    """Vérifie que le template HTML ne contient plus de JavaScript inline"""
    template_path = "/home/krapaud/project-holbies/src/templates/pld.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher les onclick inline
    onclick_matches = re.findall(r'onclick\s*=\s*["\'][^"\']*["\']', content, re.IGNORECASE)
    
    # Rechercher les scripts inline
    script_matches = re.findall(r'<script[^>]*>.*?</script>', content, re.DOTALL | re.IGNORECASE)
    
    # Rechercher les handlers d'événements inline
    event_handlers = re.findall(r'on\w+\s*=\s*["\'][^"\']*["\']', content, re.IGNORECASE)
    
    return {
        'onclick_count': len(onclick_matches),
        'onclick_matches': onclick_matches,
        'script_count': len(script_matches),
        'script_matches': script_matches,
        'event_handlers_count': len(event_handlers),
        'event_handlers': event_handlers
    }

def check_js_file():
    """Vérifie que le fichier JS contient les event listeners appropriés"""
    js_path = "/home/krapaud/project-holbies/src/static/js/pld.js"
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher les fonctions importantes
    functions_to_check = [
        'setupEventListeners',
        'addEventListener',
        'selectCategory',
        'backToCategories'
    ]
    
    found_functions = {}
    for func in functions_to_check:
        matches = re.findall(f'{func}', content, re.IGNORECASE)
        found_functions[func] = len(matches)
    
    # Vérifier la structure de classe
    class_match = re.search(r'class\s+AIQuizManager', content)
    initialization_match = re.search(r'DOMContentLoaded', content)
    
    return {
        'functions': found_functions,
        'has_class': bool(class_match),
        'has_initialization': bool(initialization_match),
        'file_size': len(content)
    }

def main():
    print("🔍 VALIDATION DE LA SÉPARATION HTML/JS")
    print("=" * 50)
    
    # Vérification du template HTML
    print("\n📄 VÉRIFICATION DU TEMPLATE HTML:")
    html_results = check_html_template()
    
    if html_results['onclick_count'] == 0:
        print("   ✅ Aucun onclick inline trouvé")
    else:
        print(f"   ❌ {html_results['onclick_count']} onclick inline trouvés:")
        for onclick in html_results['onclick_matches']:
            print(f"      - {onclick}")
    
    if html_results['event_handlers_count'] == 0:
        print("   ✅ Aucun handler d'événement inline trouvé")
    else:
        print(f"   ⚠️ {html_results['event_handlers_count']} handlers d'événements trouvés:")
        for handler in html_results['event_handlers']:
            print(f"      - {handler}")
    
    if html_results['script_count'] == 0:
        print("   ✅ Aucun script inline trouvé")
    else:
        print(f"   ⚠️ {html_results['script_count']} scripts inline trouvés")
    
    # Vérification du fichier JS
    print("\n📜 VÉRIFICATION DU FICHIER JS:")
    js_results = check_js_file()
    
    if js_results['has_class']:
        print("   ✅ Classe AIQuizManager trouvée")
    else:
        print("   ❌ Classe AIQuizManager manquante")
    
    if js_results['has_initialization']:
        print("   ✅ Initialisation DOMContentLoaded trouvée")
    else:
        print("   ❌ Initialisation DOMContentLoaded manquante")
    
    print(f"   📊 Taille du fichier: {js_results['file_size']} caractères")
    
    print("\n📋 FONCTIONS JAVASCRIPT:")
    for func, count in js_results['functions'].items():
        if count > 0:
            print(f"   ✅ {func}: {count} occurrence(s)")
        else:
            print(f"   ❌ {func}: non trouvé")
    
    # Résumé
    print("\n" + "=" * 50)
    total_issues = html_results['onclick_count'] + html_results['script_count']
    required_js_functions = sum(1 for count in js_results['functions'].values() if count > 0)
    
    if total_issues == 0 and required_js_functions >= 3:
        print("🎉 SÉPARATION RÉUSSIE !")
        print("   ✅ HTML propre (pas de JS inline)")
        print("   ✅ JS bien structuré avec event listeners")
        print("   ✅ Architecture maintenable")
    else:
        print("⚠️ AMÉLIORATIONS NÉCESSAIRES:")
        if total_issues > 0:
            print(f"   - Supprimer {total_issues} élément(s) JS inline du HTML")
        if required_js_functions < 3:
            print("   - Ajouter les fonctions JS manquantes")
    
    print("\n🧪 POUR TESTER:")
    print("   1. Ouvrir http://localhost:8000/pld")
    print("   2. Vérifier la console browser (F12)")
    print("   3. Cliquer sur une catégorie")
    print("   4. Vérifier que les toasts s'affichent")

if __name__ == "__main__":
    main()

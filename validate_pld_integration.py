#!/usr/bin/env python3
"""
Script de validation après suppression de pld-init.js
"""

import os
import re

def check_pld_js_integration():
    """Vérifie que pld.js contient toutes les fonctionnalités nécessaires"""
    pld_js_path = "/home/krapaud/project-holbies/src/static/js/pld.js"
    
    with open(pld_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fonctionnalités à vérifier
    required_functions = [
        'function selectCategory',
        'DOMContentLoaded',
        'setupEventListeners',
        'initializeAIQuizManager',
        'addEventListener',
        'AIQuizManager',
        'showForcedToast'
    ]
    
    found_functions = {}
    for func in required_functions:
        matches = re.findall(func, content, re.IGNORECASE)
        found_functions[func] = len(matches)
    
    return found_functions, len(content)

def check_template_includes():
    """Vérifie que le template n'inclut plus pld-init.js"""
    template_path = "/home/krapaud/project-holbies/src/templates/pld.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher les inclusions de pld-init.js
    pld_init_includes = re.findall(r'pld-init\.js', content, re.IGNORECASE)
    
    # Vérifier que pld.js est inclus
    pld_js_includes = re.findall(r'pld\.js', content, re.IGNORECASE)
    
    return {
        'pld_init_includes': len(pld_init_includes),
        'pld_js_includes': len(pld_js_includes)
    }

def main():
    print("🔍 VALIDATION APRÈS SUPPRESSION DE PLD-INIT.JS")
    print("=" * 55)
    
    # Vérifier que pld-init.js n'existe plus
    pld_init_path = "/home/krapaud/project-holbies/src/static/js/pld-init.js"
    if os.path.exists(pld_init_path):
        print("❌ ERREUR: pld-init.js existe encore!")
        return
    else:
        print("✅ pld-init.js a bien été supprimé")
    
    # Vérifier l'intégration dans pld.js
    print("\n📜 VÉRIFICATION DE PLD.JS:")
    functions, file_size = check_pld_js_integration()
    
    all_functions_present = True
    for func, count in functions.items():
        if count > 0:
            print(f"   ✅ {func}: {count} occurrence(s)")
        else:
            print(f"   ❌ {func}: MANQUANT")
            all_functions_present = False
    
    print(f"   📊 Taille du fichier: {file_size} caractères")
    
    # Vérifier le template
    print("\n📄 VÉRIFICATION DU TEMPLATE:")
    template_results = check_template_includes()
    
    if template_results['pld_init_includes'] == 0:
        print("   ✅ pld-init.js n'est plus inclus")
    else:
        print(f"   ❌ pld-init.js encore inclus {template_results['pld_init_includes']} fois")
    
    if template_results['pld_js_includes'] > 0:
        print(f"   ✅ pld.js est inclus ({template_results['pld_js_includes']} fois)")
    else:
        print("   ❌ pld.js n'est pas inclus!")
    
    # Résumé final
    print("\n" + "=" * 55)
    if (all_functions_present and 
        template_results['pld_init_includes'] == 0 and 
        template_results['pld_js_includes'] > 0):
        print("🎉 INTÉGRATION RÉUSSIE!")
        print("   ✅ pld-init.js supprimé")
        print("   ✅ Toutes les fonctionnalités intégrées dans pld.js")
        print("   ✅ Template mis à jour")
        print("   ✅ Architecture propre et consolidée")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS:")
        if not all_functions_present:
            print("   - Fonctionnalités manquantes dans pld.js")
        if template_results['pld_init_includes'] > 0:
            print("   - pld-init.js encore référencé dans le template")
        if template_results['pld_js_includes'] == 0:
            print("   - pld.js non inclus dans le template")
    
    print("\n🧪 FICHIERS JAVASCRIPT FINAUX:")
    js_dir = "/home/krapaud/project-holbies/src/static/js/"
    js_files = [f for f in os.listdir(js_dir) if f.endswith('.js')]
    for js_file in sorted(js_files):
        print(f"   📄 {js_file}")
    
    print(f"\n   Total: {len(js_files)} fichiers JavaScript")

if __name__ == "__main__":
    main()

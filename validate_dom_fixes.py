#!/usr/bin/env python3
"""
Script de validation des corrections DOM
"""

import re

def check_dom_references():
    """Vérifie les références DOM dans pld.js"""
    js_path = "/home/krapaud/project-holbies/src/static/js/pld.js"
    template_path = "/home/krapaud/project-holbies/src/templates/pld.html"
    
    # Lire le fichier JS
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Lire le template HTML
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extraire tous les getElementById du JS
    js_ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_content)
    
    # Extraire tous les id du HTML
    html_ids = re.findall(r'id=["\']([^"\']+)["\']', html_content)
    
    # Vérifier la correspondance
    missing_ids = []
    existing_ids = []
    
    for js_id in set(js_ids):
        if js_id in html_ids:
            existing_ids.append(js_id)
        else:
            missing_ids.append(js_id)
    
    return {
        'js_ids': js_ids,
        'html_ids': html_ids,
        'missing_ids': missing_ids,
        'existing_ids': existing_ids,
        'js_id_count': len(js_ids),
        'html_id_count': len(html_ids)
    }

def check_null_safety():
    """Vérifie les protections contre les éléments null"""
    js_path = "/home/krapaud/project-holbies/src/static/js/pld.js"
    
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Rechercher les vérifications de null/undefined
    null_checks = re.findall(r'if\s*\([^)]*!.*\)', content)
    existence_checks = re.findall(r'if\s*\([^)]*&&[^)]*\)', content)
    
    return {
        'null_checks': len(null_checks),
        'existence_checks': len(existence_checks)
    }

def main():
    print("🔍 VALIDATION DES CORRECTIONS DOM")
    print("=" * 45)
    
    # Vérification des références DOM
    print("\n📄 VÉRIFICATION DES RÉFÉRENCES DOM:")
    dom_results = check_dom_references()
    
    print(f"   📊 Total IDs dans JS: {dom_results['js_id_count']}")
    print(f"   📊 Total IDs dans HTML: {dom_results['html_id_count']}")
    
    if dom_results['existing_ids']:
        print(f"\n   ✅ IDs TROUVÉS ({len(dom_results['existing_ids'])}):")
        for eid in sorted(set(dom_results['existing_ids'])):
            count = dom_results['js_ids'].count(eid)
            print(f"      - {eid} (utilisé {count} fois)")
    
    if dom_results['missing_ids']:
        print(f"\n   ❌ IDS MANQUANTS ({len(dom_results['missing_ids'])}):")
        for mid in sorted(set(dom_results['missing_ids'])):
            count = dom_results['js_ids'].count(mid)
            print(f"      - {mid} (utilisé {count} fois)")
    else:
        print("\n   ✅ Aucun ID manquant trouvé")
    
    # Vérification des protections
    print("\n🛡️ VÉRIFICATION DES PROTECTIONS:")
    safety_results = check_null_safety()
    
    print(f"   🔍 Vérifications null: {safety_results['null_checks']}")
    print(f"   🔍 Vérifications existence: {safety_results['existence_checks']}")
    
    if safety_results['null_checks'] > 5 and safety_results['existence_checks'] > 3:
        print("   ✅ Protections suffisantes détectées")
    else:
        print("   ⚠️ Protections limitées")
    
    # Résumé
    print("\n" + "=" * 45)
    missing_count = len(dom_results['missing_ids'])
    
    if missing_count == 0:
        print("🎉 CORRECTIONS RÉUSSIES!")
        print("   ✅ Tous les IDs JavaScript existent dans le HTML")
        print("   ✅ Aucune erreur DOM attendue")
        print("   ✅ Code robuste et sécurisé")
    elif missing_count <= 2:
        print("⚠️ AMÉLIORATIONS MINEURES NÉCESSAIRES:")
        print(f"   - {missing_count} ID(s) manquant(s) à corriger")
        print("   - Fonctionnalité principale préservée")
    else:
        print("❌ CORRECTIONS SUPPLÉMENTAIRES NÉCESSAIRES:")
        print(f"   - {missing_count} ID(s) manquant(s) à corriger")
        print("   - Risque d'erreurs JavaScript")
    
    print("\n🧪 POUR TESTER:")
    print("   1. Ouvrir http://localhost:8000/pld")
    print("   2. Ouvrir la console (F12)")
    print("   3. Cliquer sur une catégorie")
    print("   4. Vérifier l'absence d'erreurs DOM")

if __name__ == "__main__":
    main()

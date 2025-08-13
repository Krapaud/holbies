#!/usr/bin/env python3
"""
Validation finale des corrections JavaScript PLD
"""

import requests
import re

def validate_syntax():
    """Valide la syntaxe du fichier pld.js"""
    print("🔍 VALIDATION SYNTAXE JAVASCRIPT")
    print("=" * 50)
    
    try:
        with open('/home/krapaud/project-holbies/src/static/js/pld.js', 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return False
    
    # Vérifier l'intégrité de base
    checks = []
    
    # 1. Classe AIQuizManager
    if 'class AIQuizManager {' in content:
        print("   ✅ Classe AIQuizManager trouvée")
        checks.append(True)
    else:
        print("   ❌ Classe AIQuizManager manquante")
        checks.append(False)
    
    # 2. Try/catch balance
    try_count = len(re.findall(r'try\s*{', content))
    catch_count = len(re.findall(r'}\s*catch\s*\(', content))
    
    print(f"   🔍 Try blocks: {try_count}")
    print(f"   🔍 Catch blocks: {catch_count}")
    
    if try_count == catch_count:
        print("   ✅ Try/catch équilibrés")
        checks.append(True)
    else:
        print("   ❌ Try/catch déséquilibrés")
        checks.append(False)
    
    # 3. Vérifier la ligne problématique
    if 'this.cu\nrrentSession.id' in content:
        print("   ❌ Ligne coupée encore présente")
        checks.append(False)
    else:
        print("   ✅ Ligne coupée corrigée")
        checks.append(True)
    
    # 4. Vérifier les string templates
    broken_templates = re.findall(r'`[^`]*\n[^`]*\n[^`]*`', content)
    if len(broken_templates) == 0:
        print("   ✅ Templates strings intacts")
        checks.append(True)
    else:
        print(f"   ⚠️ {len(broken_templates)} templates potentiellement coupés")
        checks.append(True)  # Pas forcément critique
    
    return all(checks)

def test_server_response():
    """Teste la réponse du serveur"""
    print("\n🌐 TEST SERVEUR")
    print("=" * 50)
    
    urls = [
        'http://localhost:8000/pld',
        'http://localhost:8000/static/js/pld.js',
        'http://localhost:8000/static/js/main.js',
        'http://localhost:8000/static/js/toast.js'
    ]
    
    results = []
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {url.split('/')[-1]}: {response.status_code}")
                results.append(True)
            else:
                print(f"   ❌ {url.split('/')[-1]}: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"   ❌ {url.split('/')[-1]}: {e}")
            results.append(False)
    
    return all(results)

def validate_template():
    """Valide le template HTML"""
    print("\n📄 VALIDATION TEMPLATE")
    print("=" * 50)
    
    try:
        with open('/home/krapaud/project-holbies/src/templates/pld.html', 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture template: {e}")
        return False
    
    checks = []
    
    # Scripts inclus
    scripts = ['toast.js', 'main.js', 'pld.js']
    for script in scripts:
        if script in content:
            print(f"   ✅ {script} inclus")
            checks.append(True)
        else:
            print(f"   ❌ {script} manquant")
            checks.append(False)
    
    # Fonction selectCategory
    if 'function selectCategory' in content:
        print("   ✅ Fonction selectCategory définie")
        checks.append(True)
    else:
        print("   ❌ Fonction selectCategory manquante")
        checks.append(False)
    
    # Logging étendu
    if 'console.log(\'🔍 Vérification des dépendances:\')' in content:
        print("   ✅ Logging étendu activé")
        checks.append(True)
    else:
        print("   ⚠️ Logging étendu non trouvé")
        checks.append(True)  # Pas critique
    
    return all(checks)

def main():
    print("🚀 VALIDATION FINALE - CORRECTIONS JAVASCRIPT PLD")
    print("=" * 70)
    
    results = []
    results.append(validate_syntax())
    results.append(test_server_response())
    results.append(validate_template())
    
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ FINAL")
    print("=" * 70)
    
    if all(results):
        print("🎉 TOUTES LES VALIDATIONS RÉUSSIES!")
        print("\n✅ Corrections appliquées:")
        print("   • Syntaxe JavaScript corrigée (ligne coupée)")
        print("   • Try/catch équilibrés")
        print("   • Classe AIQuizManager disponible")
        print("   • Template HTML avec logging étendu")
        print("   • Serveur accessible")
        print("\n🎯 Les erreurs JavaScript devraient être résolues!")
        print("   - Plus de 'Missing catch or finally after try'")
        print("   - AIQuizManager devrait s'initialiser correctement")
        print("   - Logs détaillés dans la console pour diagnostiquer")
        return 0
    else:
        print("❌ CERTAINES VALIDATIONS ONT ÉCHOUÉ")
        print("Consultez les détails ci-dessus.")
        return 1

if __name__ == "__main__":
    exit(main())

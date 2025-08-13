#!/usr/bin/env python3
"""
Validation finale du nouveau comportement des catégories vides dans PLD
"""

import requests
import sys

def validate_new_api_behavior():
    """Valide que l'API retourne bien 204 pour les catégories vides"""
    
    print("🧪 VALIDATION DU NOUVEAU COMPORTEMENT API")
    print("=" * 60)
    
    # Se connecter d'abord
    try:
        session = requests.Session()
        login_data = {'username': 'testuser', 'password': 'testpass'}
        login_response = session.post('http://localhost:8000/auth/login', data=login_data)
        
        if login_response.status_code not in [200, 302]:
            print(f"❌ Erreur de connexion: {login_response.status_code}")
            return False
        
        print("✅ Connexion réussie")
        
        # Tests de l'API
        tests = [
            {
                'category': 'test_empty',
                'expected_status': 204,
                'description': 'Catégorie vide (doit retourner 204)',
                'should_have_json': False
            },
            {
                'category': 'c', 
                'expected_status': 200,
                'description': 'Catégorie avec thèmes (doit retourner 200 + JSON)',
                'should_have_json': True
            },
            {
                'category': 'shell',
                'expected_status': 200, 
                'description': 'Catégorie avec thèmes (doit retourner 200 + JSON)',
                'should_have_json': True
            }
        ]
        
        all_passed = True
        
        for test in tests:
            print(f"\n📁 Test: {test['description']}")
            
            response = session.get(f'http://localhost:8000/api/pld/categories/{test["category"]}/themes')
            
            print(f"   Catégorie: {test['category']}")
            print(f"   Status reçu: {response.status_code}")
            print(f"   Status attendu: {test['expected_status']}")
            
            # Vérifier le status code
            if response.status_code == test['expected_status']:
                print("   ✅ Status code correct")
            else:
                print("   ❌ Status code incorrect")
                all_passed = False
                continue
            
            # Vérifier le contenu JSON
            if test['should_have_json']:
                try:
                    data = response.json()
                    if 'themes' in data and isinstance(data['themes'], list):
                        print(f"   ✅ JSON valide avec {len(data['themes'])} thème(s)")
                    else:
                        print("   ❌ JSON invalide ou structure incorrecte")
                        all_passed = False
                except:
                    print("   ❌ Impossible de parser le JSON")
                    all_passed = False
            else:
                # Pour les 204, il ne devrait pas y avoir de JSON
                try:
                    response.json()
                    print("   ❌ JSON présent alors qu'il ne devrait pas y en avoir")
                    all_passed = False
                except:
                    print("   ✅ Pas de JSON (correct pour 204)")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 VALIDATION RÉUSSIE - NOUVEAU COMPORTEMENT CORRECT")
            print("\n✅ Résumé des améliorations :")
            print("   • Catégories vides : HTTP 204 (au lieu de 200 + JSON vide)")
            print("   • Catégories avec thèmes : HTTP 200 + JSON (inchangé)")
            print("   • Frontend : Seul le toast s'affiche pour les catégories vides")
            print('   • Plus de {"themes":[]} retourné par l\'API')
        else:
            print("❌ VALIDATION ÉCHOUÉE - Certains tests ont échoué")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la validation: {e}")
        return False

def check_frontend_code():
    """Vérifie que le code frontend gère bien le statut 204"""
    
    print("\n🔍 VÉRIFICATION DU CODE FRONTEND")
    print("=" * 60)
    
    try:
        with open('/home/krapaud/project-holbies/src/static/js/pld.js', 'r') as f:
            content = f.read()
        
        checks = [
            {
                'name': 'Gestion du statut 204 dans loadThemes()',
                'pattern': 'response.status === 204',
                'found': 'response.status === 204' in content
            },
            {
                'name': 'Gestion du statut 204 dans loadThemesForCategory()',
                'pattern': 'response.status === 204',
                'found': content.count('response.status === 204') >= 2
            },
            {
                'name': 'Toast pour catégories vides',
                'pattern': 'Aucun thème disponible',
                'found': 'Aucun thème disponible' in content
            }
        ]
        
        for check in checks:
            status = "✅" if check['found'] else "❌"
            print(f"   {status} {check['name']}")
        
        return all(check['found'] for check in checks)
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du code: {e}")
        return False

def main():
    print("🎯 VALIDATION COMPLÈTE - NOUVEAU COMPORTEMENT CATÉGORIES VIDES")
    print("=" * 70)
    
    api_ok = validate_new_api_behavior()
    frontend_ok = check_frontend_code()
    
    print("\n" + "=" * 70)
    print("📋 RÉSULTAT FINAL:")
    print("=" * 70)
    
    if api_ok and frontend_ok:
        print("🎉 ✅ TOUTES LES VALIDATIONS RÉUSSIES !")
        print("\n🚀 Le nouveau comportement est opérationnel :")
        print("   1. ✅ API modifiée : 204 pour catégories vides")
        print("   2. ✅ Frontend adapté : Gestion du statut 204")
        print("   3. ✅ UX améliorée : Seul le toast s'affiche")
        print("   4. ✅ Plus de JSON vide retourné")
        
        print("\n💡 Comment tester :")
        print("   • Aller sur http://localhost:8000/pld")
        print("   • Se connecter avec testuser/testpass")
        print("   • Cliquer sur 'Test Vide' dans la sidebar")
        print("   • Voir le toast sans redirection ni JSON vide")
        
    else:
        print("❌ CERTAINES VALIDATIONS ONT ÉCHOUÉ")
        if not api_ok:
            print("   ❌ Problème avec l'API")
        if not frontend_ok:
            print("   ❌ Problème avec le code frontend")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

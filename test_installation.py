#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation de Holbies Learning Hub
"""

import sys
import os
import requests
import time
import subprocess
import signal
from multiprocessing import Process

def test_imports():
    """Test les imports Python nécessaires"""
    print("🔍 Test des imports Python...")
    
    try:
        import fastapi
        print("✅ FastAPI importé avec succès")
        
        import sqlalchemy
        print("✅ SQLAlchemy importé avec succès")
        
        import psycopg2
        print("✅ psycopg2 importé avec succès")
        
        import uvicorn
        print("✅ Uvicorn importé avec succès")
        
        import jose
        print("✅ python-jose importé avec succès")
        
        import passlib
        print("✅ passlib importé avec succès")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_database_connection():
    """Test la connexion à la base de données"""
    print("\n🔍 Test de la connexion à la base de données...")
    
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Connexion à la base de données réussie")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def test_models():
    """Test les modèles de base de données"""
    print("\n🔍 Test des modèles de base de données...")
    
    try:
        from app.models import User, Question, QuizSession, QuizAnswer
        print("✅ Tous les modèles importés avec succès")
        
        from app.database import SessionLocal
        db = SessionLocal()
        
        # Test si les tables existent
        user_count = db.query(User).count()
        question_count = db.query(Question).count()
        
        print(f"✅ {user_count} utilisateurs dans la base")
        print(f"✅ {question_count} questions dans la base")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ Erreur avec les modèles: {e}")
        return False

def start_server():
    """Démarre le serveur en arrière-plan"""
    import uvicorn
    from main import app
    
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

def test_server():
    """Test le serveur web"""
    print("\n🔍 Test du serveur web...")
    
    # Démarrer le serveur en arrière-plan
    server_process = Process(target=start_server)
    server_process.start()
    
    # Attendre que le serveur démarre
    time.sleep(3)
    
    try:
        # Test de la page d'accueil
        response = requests.get("http://127.0.0.1:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
        else:
            print(f"❌ Page d'accueil retourne: {response.status_code}")
            return False
        
        # Test de l'API docs
        response = requests.get("http://127.0.0.1:8001/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Documentation API accessible")
        else:
            print(f"❌ Documentation API retourne: {response.status_code}")
        
        # Test d'une route API
        response = requests.get("http://127.0.0.1:8001/api/quiz/questions?limit=1", timeout=5)
        if response.status_code == 401:  # Unauthorized (normal sans token)
            print("✅ API fonctionnelle (authentification requise)")
        else:
            print(f"ℹ️ API retourne: {response.status_code}")
        
        server_process.terminate()
        server_process.join()
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion au serveur: {e}")
        server_process.terminate()
        server_process.join()
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test du serveur: {e}")
        server_process.terminate()
        server_process.join()
        return False

def test_static_files():
    """Test l'existence des fichiers statiques"""
    print("\n🔍 Test des fichiers statiques...")
    
    static_files = [
        "static/css/style.css",
        "static/js/main.js",
        "static/js/auth.js",
        "static/js/quiz.js",
        "static/js/dashboard.js"
    ]
    
    all_exist = True
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} manquant")
            all_exist = False
    
    return all_exist

def test_templates():
    """Test l'existence des templates"""
    print("\n🔍 Test des templates...")
    
    template_files = [
        "templates/base.html",
        "templates/index.html",
        "templates/login.html",
        "templates/register.html",
        "templates/quiz.html",
        "templates/dashboard.html"
    ]
    
    all_exist = True
    for file_path in template_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} manquant")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Lance tous les tests"""
    print("🧪 TESTS DE L'INSTALLATION HOLBIES LEARNING HUB")
    print("=" * 60)
    
    tests = [
        ("Imports Python", test_imports),
        ("Connexion base de données", test_database_connection),
        ("Modèles de données", test_models),
        ("Fichiers statiques", test_static_files),
        ("Templates HTML", test_templates),
        ("Serveur web", test_server)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat final: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés! L'installation est complète.")
        print("\n💡 Pour démarrer l'application:")
        print("   ./start.sh")
        print("\n🌐 Ou manuellement:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué.")
        print("Consultez les messages d'erreur ci-dessus pour résoudre les problèmes.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Script pour nettoyer les données de performance d'un utilisateur spécifique
"""

import sys
sys.path.append('/app/src')

from app.database import get_db
from app.models import User, QuizSession, AIQuizSession, UserPerformanceStats, UserActivity
from sqlalchemy.orm import Session

def clean_user_performance_data(username: str):
    """Nettoie toutes les données de performance d'un utilisateur"""
    
    print(f"🧹 NETTOYAGE DES DONNÉES DE PERFORMANCE")
    print(f"👤 Utilisateur: {username}")
    print("=" * 50)
    
    # Obtenir une session de base de données
    db = next(get_db())
    
    try:
        # Trouver l'utilisateur
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            print(f"❌ Utilisateur '{username}' non trouvé!")
            return
        
        user_id = user.id
        print(f"✅ Utilisateur trouvé: {user.username} (ID: {user_id})")
        print(f"📧 Email: {user.email}")
        print()
        
        # Compter les données avant suppression
        quiz_sessions_count = db.query(QuizSession).filter(QuizSession.user_id == user_id).count()
        ai_quiz_sessions_count = db.query(AIQuizSession).filter(AIQuizSession.user_id == user_id).count()
        performance_stats_count = db.query(UserPerformanceStats).filter(UserPerformanceStats.user_id == user_id).count()
        activities_count = db.query(UserActivity).filter(UserActivity.user_id == user_id).count()
        
        print("📊 DONNÉES À SUPPRIMER:")
        print(f"   🎯 Quiz Sessions: {quiz_sessions_count}")
        print(f"   🤖 AI Quiz Sessions: {ai_quiz_sessions_count}")
        print(f"   📈 Performance Stats: {performance_stats_count}")
        print(f"   ⚡ Activités: {activities_count}")
        print()
        
        if quiz_sessions_count == 0 and ai_quiz_sessions_count == 0 and performance_stats_count == 0 and activities_count == 0:
            print("✅ Aucune donnée de performance à supprimer!")
            return
        
        # Confirmation
        print("⚠️  ATTENTION: Cette action supprimera toutes les données de performance!")
        print("   Les données utilisateur (compte, mot de passe) seront conservées.")
        print()
        
        # Effectuer la suppression
        print("🗑️  SUPPRESSION EN COURS...")
        
        # Supprimer les quiz sessions
        if quiz_sessions_count > 0:
            deleted_quiz = db.query(QuizSession).filter(QuizSession.user_id == user_id).delete()
            print(f"   ✅ Quiz Sessions supprimées: {deleted_quiz}")
        
        # Supprimer les AI quiz sessions
        if ai_quiz_sessions_count > 0:
            deleted_ai_quiz = db.query(AIQuizSession).filter(AIQuizSession.user_id == user_id).delete()
            print(f"   ✅ AI Quiz Sessions supprimées: {deleted_ai_quiz}")
        
        # Supprimer les stats de performance
        if performance_stats_count > 0:
            deleted_stats = db.query(UserPerformanceStats).filter(UserPerformanceStats.user_id == user_id).delete()
            print(f"   ✅ Performance Stats supprimées: {deleted_stats}")
        
        # Supprimer les activités
        if activities_count > 0:
            deleted_activities = db.query(UserActivity).filter(UserActivity.user_id == user_id).delete()
            print(f"   ✅ Activités supprimées: {deleted_activities}")
        
        # Confirmer les changements
        db.commit()
        
        print()
        print("✅ NETTOYAGE TERMINÉ!")
        print(f"👤 L'utilisateur '{username}' a maintenant un profil vierge")
        print("🎯 Vous pouvez maintenant commencer vos vrais quiz!")
        print()
        print("🌐 Liens utiles:")
        print("   📊 Analytics: http://localhost:8000/api/performance/analytics")
        print("   🎯 Quiz: http://localhost:8000/quiz")
        print("   🤖 AI Quiz: http://localhost:8000/ai-quiz")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def verify_clean_data(username: str):
    """Vérifie que les données ont bien été nettoyées"""
    
    print(f"\n🔍 VÉRIFICATION POST-NETTOYAGE")
    print(f"👤 Utilisateur: {username}")
    print("-" * 30)
    
    db = next(get_db())
    
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ Utilisateur '{username}' non trouvé!")
            return
        
        user_id = user.id
        
        # Vérifier les compteurs
        quiz_count = db.query(QuizSession).filter(QuizSession.user_id == user_id).count()
        ai_quiz_count = db.query(AIQuizSession).filter(AIQuizSession.user_id == user_id).count()
        stats_count = db.query(UserPerformanceStats).filter(UserPerformanceStats.user_id == user_id).count()
        activities_count = db.query(UserActivity).filter(UserActivity.user_id == user_id).count()
        
        print(f"📊 ÉTAT ACTUEL:")
        print(f"   🎯 Quiz Sessions: {quiz_count}")
        print(f"   🤖 AI Quiz Sessions: {ai_quiz_count}")
        print(f"   📈 Performance Stats: {stats_count}")
        print(f"   ⚡ Activités: {activities_count}")
        
        if quiz_count == 0 and ai_quiz_count == 0 and stats_count == 0 and activities_count == 0:
            print("\n✅ PARFAIT! Toutes les données ont été nettoyées")
            print("🎯 Votre profil est maintenant vierge et prêt pour de vrais quiz!")
        else:
            print("\n⚠️  Il reste encore des données...")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    username = "Krapaud"
    
    print("🧹 SCRIPT DE NETTOYAGE DES DONNÉES DE PERFORMANCE")
    print("=" * 60)
    
    # Nettoyer les données
    clean_user_performance_data(username)
    
    # Vérifier le nettoyage
    verify_clean_data(username)

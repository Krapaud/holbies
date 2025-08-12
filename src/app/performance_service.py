"""
Service de gestion des statistiques de performance en temps réel
"""
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from app.models import User, QuizSession, AIQuizSession, UserPerformanceStats, DailySystemStats, UserActivity
from app.database import SessionLocal

class PerformanceStatsService:
    """Service pour calculer et gérer les statistiques de performance"""
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
    
    def calculate_user_performance(self, user_id: int) -> Dict:
        """Calcule les statistiques de performance d'un utilisateur"""
        try:
            # Statistiques Quiz classique
            quiz_stats = self.db.query(
                func.count(QuizSession.id).label('sessions_count'),
                func.sum(QuizSession.score).label('total_score'),
                func.sum(QuizSession.total_questions).label('total_questions'),
                func.avg(QuizSession.score).label('avg_score'),
                func.max(QuizSession.score).label('best_score')
            ).filter(
                QuizSession.user_id == user_id,
                QuizSession.completed == True
            ).first()
            
            # Statistiques AI Quiz
            ai_quiz_stats = self.db.query(
                func.count(AIQuizSession.id).label('sessions_count'),
                func.sum(AIQuizSession.total_score).label('total_score'),
                func.sum(AIQuizSession.total_questions).label('total_questions'),
                func.avg(AIQuizSession.total_score).label('avg_score'),
                func.max(AIQuizSession.total_score).label('best_score')
            ).filter(
                AIQuizSession.user_id == user_id,
                AIQuizSession.completed == True
            ).first()
            
            # Activité récente (7 derniers jours)
            week_ago = datetime.now() - timedelta(days=7)
            recent_activity = self.db.query(UserActivity).filter(
                UserActivity.user_id == user_id,
                UserActivity.timestamp >= week_ago
            ).count()
            
            # Calcul du niveau et XP
            total_score = (quiz_stats.total_score or 0) + (ai_quiz_stats.total_score or 0)
            level = max(1, int(total_score / 100) + 1)
            experience_points = int(total_score * 10)
            
            # Calcul du streak
            streak = self._calculate_streak(user_id)
            
            return {
                'user_id': user_id,
                'quiz': {
                    'sessions_completed': quiz_stats.sessions_count or 0,
                    'total_score': quiz_stats.total_score or 0,
                    'total_questions': quiz_stats.total_questions or 0,
                    'average_score': float(quiz_stats.avg_score or 0),
                    'best_score': quiz_stats.best_score or 0
                },
                'ai_quiz': {
                    'sessions_completed': ai_quiz_stats.sessions_count or 0,
                    'total_score': float(ai_quiz_stats.total_score or 0),
                    'total_questions': ai_quiz_stats.total_questions or 0,
                    'average_score': float(ai_quiz_stats.avg_score or 0),
                    'best_score': float(ai_quiz_stats.best_score or 0)
                },
                'global': {
                    'level': level,
                    'experience_points': experience_points,
                    'streak_days': streak,
                    'recent_activity': recent_activity
                }
            }
        except Exception as e:
            print(f"Erreur calcul performance utilisateur {user_id}: {e}")
            return self._empty_user_stats(user_id)
    
    def get_user_progress_timeline(self, user_id: int, days: int = 30) -> List[Dict]:
        """Récupère l'évolution des performances sur une période"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            # Progression des scores par jour
            daily_progress = self.db.execute(text("""
                SELECT 
                    DATE(completed_at) as date,
                    COUNT(*) as sessions,
                    AVG(score) as avg_score,
                    SUM(score) as total_score,
                    SUM(total_questions) as total_questions
                FROM quiz_sessions 
                WHERE user_id = :user_id 
                    AND completed = true 
                    AND completed_at >= :start_date
                GROUP BY DATE(completed_at)
                ORDER BY date
            """), {"user_id": user_id, "start_date": start_date}).fetchall()
            
            # Progression AI Quiz
            ai_daily_progress = self.db.execute(text("""
                SELECT 
                    DATE(completed_at) as date,
                    COUNT(*) as sessions,
                    AVG(total_score) as avg_score,
                    SUM(total_score) as total_score,
                    SUM(total_questions) as total_questions
                FROM ai_quiz_sessions 
                WHERE user_id = :user_id 
                    AND completed = true 
                    AND completed_at >= :start_date
                GROUP BY DATE(completed_at)
                ORDER BY date
            """), {"user_id": user_id, "start_date": start_date}).fetchall()
            
            # Combiner les données
            timeline = []
            for row in daily_progress:
                timeline.append({
                    'date': row[0].isoformat() if row[0] else None,
                    'type': 'quiz',
                    'sessions': row[1] or 0,
                    'avg_score': float(row[2] or 0),
                    'total_score': row[3] or 0,
                    'total_questions': row[4] or 0
                })
            
            for row in ai_daily_progress:
                timeline.append({
                    'date': row[0].isoformat() if row[0] else None,
                    'type': 'ai_quiz',
                    'sessions': row[1] or 0,
                    'avg_score': float(row[2] or 0),
                    'total_score': float(row[3] or 0),
                    'total_questions': row[4] or 0
                })
            
            return sorted(timeline, key=lambda x: x['date'] or '')
            
        except Exception as e:
            print(f"Erreur timeline utilisateur {user_id}: {e}")
            return []
    
    def get_system_performance_stats(self) -> Dict:
        """Calcule les statistiques de performance globales du système"""
        try:
            today = datetime.now().date()
            week_ago = datetime.now() - timedelta(days=7)
            month_ago = datetime.now() - timedelta(days=30)
            
            # Utilisateurs
            total_users = self.db.query(User).count()
            active_users_today = self.db.query(UserActivity).filter(
                func.date(UserActivity.timestamp) == today
            ).distinct(UserActivity.user_id).count()
            
            new_users_week = self.db.query(User).filter(
                User.created_at >= week_ago
            ).count()
            
            # Quiz sessions
            quiz_sessions_today = self.db.query(QuizSession).filter(
                func.date(QuizSession.started_at) == today
            ).count()
            
            ai_quiz_sessions_today = self.db.query(AIQuizSession).filter(
                func.date(AIQuizSession.started_at) == today
            ).count()
            
            # Moyennes de performance
            avg_quiz_score = self.db.query(func.avg(QuizSession.score)).filter(
                QuizSession.completed == True,
                QuizSession.completed_at >= month_ago
            ).scalar() or 0
            
            avg_ai_score = self.db.query(func.avg(AIQuizSession.total_score)).filter(
                AIQuizSession.completed == True,
                AIQuizSession.completed_at >= month_ago
            ).scalar() or 0
            
            # Top performers
            top_quiz_users = self.db.execute(text("""
                SELECT u.username, AVG(qs.score) as avg_score, COUNT(qs.id) as sessions
                FROM users u
                JOIN quiz_sessions qs ON u.id = qs.user_id
                WHERE qs.completed = true
                GROUP BY u.id, u.username
                HAVING COUNT(qs.id) >= 3
                ORDER BY avg_score DESC
                LIMIT 5
            """)).fetchall()
            
            top_ai_users = self.db.execute(text("""
                SELECT u.username, AVG(aqs.total_score) as avg_score, COUNT(aqs.id) as sessions
                FROM users u
                JOIN ai_quiz_sessions aqs ON u.id = aqs.user_id
                WHERE aqs.completed = true
                GROUP BY u.id, u.username
                HAVING COUNT(aqs.id) >= 3
                ORDER BY avg_score DESC
                LIMIT 5
            """)).fetchall()
            
            return {
                'users': {
                    'total': total_users,
                    'active_today': active_users_today,
                    'new_this_week': new_users_week
                },
                'activity': {
                    'quiz_sessions_today': quiz_sessions_today,
                    'ai_quiz_sessions_today': ai_quiz_sessions_today,
                    'total_sessions_today': quiz_sessions_today + ai_quiz_sessions_today
                },
                'performance': {
                    'avg_quiz_score': float(avg_quiz_score),
                    'avg_ai_score': float(avg_ai_score)
                },
                'leaderboard': {
                    'top_quiz_users': [
                        {'username': row[0], 'avg_score': float(row[1]), 'sessions': row[2]}
                        for row in top_quiz_users
                    ],
                    'top_ai_users': [
                        {'username': row[0], 'avg_score': float(row[1]), 'sessions': row[2]}
                        for row in top_ai_users
                    ]
                }
            }
            
        except Exception as e:
            print(f"Erreur statistiques système: {e}")
            return self._empty_system_stats()
    
    def log_user_activity(self, user_id: int, activity_type: str, activity_data: Dict = None):
        """Enregistre une activité utilisateur"""
        try:
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                activity_data=json.dumps(activity_data) if activity_data else None
            )
            self.db.add(activity)
            self.db.commit()
        except Exception as e:
            print(f"Erreur log activité: {e}")
            self.db.rollback()
    
    def _calculate_streak(self, user_id: int) -> int:
        """Calcule la série de jours consécutifs d'activité"""
        try:
            # Récupérer les jours d'activité des 30 derniers jours
            thirty_days_ago = datetime.now() - timedelta(days=30)
            activity_dates = self.db.execute(text("""
                SELECT DISTINCT DATE(timestamp) as activity_date
                FROM user_activities
                WHERE user_id = :user_id AND timestamp >= :start_date
                ORDER BY activity_date DESC
            """), {"user_id": user_id, "start_date": thirty_days_ago}).fetchall()
            
            if not activity_dates:
                return 0
            
            streak = 0
            today = datetime.now().date()
            current_date = today
            
            for row in activity_dates:
                activity_date = row[0]
                if activity_date == current_date:
                    streak += 1
                    current_date -= timedelta(days=1)
                else:
                    break
            
            return streak
            
        except Exception as e:
            print(f"Erreur calcul streak: {e}")
            return 0
    
    def _empty_user_stats(self, user_id: int) -> Dict:
        """Retourne des statistiques vides pour un utilisateur"""
        return {
            'user_id': user_id,
            'quiz': {'sessions_completed': 0, 'total_score': 0, 'total_questions': 0, 'average_score': 0, 'best_score': 0},
            'ai_quiz': {'sessions_completed': 0, 'total_score': 0, 'total_questions': 0, 'average_score': 0, 'best_score': 0},
            'global': {'level': 1, 'experience_points': 0, 'streak_days': 0, 'recent_activity': 0}
        }
    
    def _empty_system_stats(self) -> Dict:
        """Retourne des statistiques système vides"""
        return {
            'users': {'total': 0, 'active_today': 0, 'new_this_week': 0},
            'activity': {'quiz_sessions_today': 0, 'ai_quiz_sessions_today': 0, 'total_sessions_today': 0},
            'performance': {'avg_quiz_score': 0, 'avg_ai_score': 0},
            'leaderboard': {'top_quiz_users': [], 'top_ai_users': []}
        }
    
    def close(self):
        """Ferme la session de base de données"""
        if self.db:
            self.db.close()

# Instance globale
def get_performance_service() -> PerformanceStatsService:
    """Factory pour obtenir le service de performance"""
    return PerformanceStatsService()

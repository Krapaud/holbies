"""
Modèles de base de données PostgreSQL pour Dev Learning Hub Matrix
Utilise SQLAlchemy pour une gestion moderne et sécurisée
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://devhub_user:matrix_secure_2025@localhost:5432/devhub_matrix")

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle User
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    quiz_scores = relationship("QuizScore", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")

# Modèle QuizScore
class QuizScore(Base):
    __tablename__ = "quiz_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    date_taken = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="quiz_scores")

# Modèle UserSession (pour gérer les sessions avec PostgreSQL)
class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(String(64), primary_key=True, index=True)  # session_id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    ip_address = Column(String(45), nullable=True)  # Support IPv4 et IPv6
    user_agent = Column(Text, nullable=True)
    
    # Relations
    user = relationship("User", back_populates="sessions")

# Modèle TutorHistory (nouveau - pour sauvegarder l'historique des codes)
class TutorHistory(Base):
    __tablename__ = "tutor_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    result = Column(Text, nullable=True)
    execution_time = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User")

# Fonctions utilitaires
def get_db():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Créer toutes les tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables PostgreSQL créées avec succès")

def drop_tables():
    """Supprimer toutes les tables (pour les tests)"""
    Base.metadata.drop_all(bind=engine)
    print("🗑️ Tables supprimées")

if __name__ == "__main__":
    # Créer les tables
    create_tables()

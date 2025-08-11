from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    quiz_sessions = relationship("QuizSession", back_populates="user")
    ai_quiz_sessions = relationship("AIQuizSession", back_populates="user")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)  # 'a', 'b', 'c', ou 'd'
    explanation = Column(Text)
    difficulty = Column(String, default="medium")  # easy, medium, hard
    category = Column(String, default="general")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    quiz_answers = relationship("QuizAnswer", back_populates="question")

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relations
    user = relationship("User", back_populates="quiz_sessions")
    answers = relationship("QuizAnswer", back_populates="session")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String, nullable=False)  # 'a', 'b', 'c', ou 'd'
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    session = relationship("QuizSession", back_populates="answers")
    question = relationship("Question", back_populates="quiz_answers")

class AIQuizSession(Base):
    __tablename__ = "ai_quiz_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_score = Column(Float, default=0.0)  # Score total (somme des points)
    total_questions = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relations
    user = relationship("User", back_populates="ai_quiz_sessions")
    ai_answers = relationship("AIQuizAnswer", back_populates="session")

class AIQuizAnswer(Base):
    __tablename__ = "ai_quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("ai_quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, nullable=False)  # ID de la question AI
    question_text = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    score = Column(Float, nullable=False)  # Score obtenu (sur 100)
    max_score = Column(Integer, default=100)
    percentage = Column(Float, nullable=False)
    similarity = Column(Float, nullable=False)
    technical_terms_found = Column(Text)  # JSON string des termes trouvés
    technical_bonus = Column(Integer, default=0)
    feedback = Column(Text)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    session = relationship("AIQuizSession", back_populates="ai_answers")

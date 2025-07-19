from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Question schemas
class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = "medium"
    category: Optional[str] = "general"

class QuestionCreate(QuestionBase):
    correct_answer: str

class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionWithAnswer(Question):
    correct_answer: str

# Quiz schemas
class QuizAnswer(BaseModel):
    question_id: int
    user_answer: str

class QuizAnswerSubmission(BaseModel):
    session_id: int
    question_id: int
    user_answer: str

class QuizSessionCreate(BaseModel):
    pass

class QuizSession(BaseModel):
    id: int
    user_id: int
    score: int
    total_questions: int
    completed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuizResult(BaseModel):
    session_id: int
    score: int
    total_questions: int
    percentage: float
    correct_answers: List[int]
    incorrect_answers: List[int]

# AI Quiz schemas
class AIQuizSessionCreate(BaseModel):
    pass

class AIQuizSession(BaseModel):
    id: int
    user_id: int
    total_score: float
    total_questions: int
    completed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class AIQuizAnswerSubmission(BaseModel):
    session_id: int
    question_id: int
    user_answer: str

class AIQuizAnswer(BaseModel):
    id: int
    session_id: int
    question_id: int
    question_text: str
    user_answer: str
    expected_answer: str
    score: float
    max_score: int
    percentage: float
    similarity: float
    technical_terms_found: str  # JSON string
    technical_bonus: int
    feedback: str
    answered_at: datetime
    
    class Config:
        from_attributes = True

class AIQuizResult(BaseModel):
    session_id: int
    total_score: float
    total_questions: int
    average_percentage: float
    answers: List[AIQuizAnswer]

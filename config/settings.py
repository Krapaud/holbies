"""
Configuration settings for the Holberton Learning Platform.
"""
import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Database settings
    database_url: str = "postgresql://user:password@localhost/dbname"
    test_database_url: str = "sqlite:///./test.db"
    
    # Security settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application settings
    app_name: str = "Holberton Learning Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Static and template paths
    static_dir: Path = BASE_DIR / "src" / "static"
    templates_dir: Path = BASE_DIR / "src" / "templates"
    
    # AI/ML settings
    openai_api_key: str = ""
    max_quiz_questions: int = 10
    
    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    """Get cached settings instance."""
    return Settings()

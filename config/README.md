# Configuration files and environment variables

This directory contains configuration files for the application:

- `settings.py`: Main application settings with environment variable support
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not tracked in git)

## Environment Variables

Create a `.env` file in this directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/holberton_db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=false
APP_NAME=Holberton Learning Platform

# AI/ML
OPENAI_API_KEY=your-openai-api-key
MAX_QUIZ_QUESTIONS=10
```

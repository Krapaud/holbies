# 🎓 Holberton Learning Platform

> An interactive learning platform with AI-powered quizzes and Matrix-themed interface

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Krapaud/project-holbies.git
cd project-holbies

# Create environment variables
cp config/.env.example config/.env
# Edit config/.env with your settings

# Start the application
cd deployment
docker-compose up --build
```

The application will be available at `http://localhost:8000`

### Manual Installation

```bash
# Install dependencies
pip install -r config/requirements.txt

# Set up environment variables
cp config/.env.example config/.env

# Initialize database
python tools/scripts/init_db.py

# Create admin user
python tools/scripts/create_admin.py

# Start the application
python run.py
```


## 📁 Project Structure & Auto-organization

The project is organized by type (backend, static, templates, scripts, docs, tests, deployment, config). To keep the project clean, use the script:

```bash
python scripts/organize_project.py
```

This script will automatically move new files to the correct folder based on their extension or type (Python, JS, CSS, images, etc.).


```
project-holbies/
├── 📂 src/                    # Source code
│   ├── 📄 main.py            # FastAPI application entry point
│   ├── 📂 app/               # Core application package
│   │   ├── 🔧 auth.py        # Authentication logic
│   │   ├── 🗃️ database.py    # Database configuration
│   │   ├── 📊 models.py      # SQLAlchemy models
│   │   ├── 📋 schemas.py     # Pydantic schemas
│   │   └── 📂 routers/       # API endpoints
│   ├── 📂 static/            # Web assets (CSS, JS, images)
│   └── 📂 templates/         # HTML templates
├── 📂 config/                # Configuration files
│   ├── ⚙️ settings.py        # Application settings
│   ├── 📋 requirements.txt   # Python dependencies
│   └── 🔐 .env              # Environment variables
├── 📂 deployment/            # Docker and deployment files
│   ├── 🐳 Dockerfile         # Container configuration
│   ├── 📝 docker-compose.yml # Multi-container setup
│   └── 🔧 wait-for-postgres.sh
├── 📂 tools/                 # Development and database tools
│   └── 📂 scripts/           # Utility scripts
├── 📂 tests/                 # Test suites
├── 📂 docs/                  # Documentation
├── 🚀 run.py                 # Application entry point
└── 📖 README.md             # This file
```

## ✨ Features

### 🎯 Core Features
- **Interactive Quiz System** - Comprehensive quiz management with real-time scoring
- **AI-Powered Assessments** - Intelligent quiz generation and automated correction
- **User Authentication** - Secure login/registration with session management
- **Progress Tracking** - Detailed learning analytics and progress monitoring
- **Responsive Design** - Matrix-themed interface optimized for all devices

### 🤖 AI Integration
- **Smart Quiz Generation** - AI creates questions based on learning objectives
- **Automated Grading** - Intelligent assessment with detailed feedback
- **Personalized Learning** - Adaptive content based on performance
- **Code Analysis** - Python code visualization and debugging assistance

### 👥 User Management
- **Role-Based Access** - Admin, instructor, and student roles
- **Profile Management** - Customizable user profiles and preferences
- **Learning Paths** - Structured curriculum progression
- **Achievement System** - Badges and rewards for milestones

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and Object-Relational Mapping
- **PostgreSQL** - Advanced open-source relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **HTML5/CSS3** - Modern web standards with responsive design
- **JavaScript** - Interactive user interface components
- **Jinja2** - Server-side templating engine
- **Matrix Theme** - Cyberpunk-inspired visual design

### DevOps & Deployment
- **Docker** - Containerization for consistent deployment
- **Docker Compose** - Multi-container application orchestration
- **Uvicorn** - Lightning-fast ASGI server
- **pytest** - Testing framework with comprehensive coverage

## 🗃️ Database Schema

### Core Models
- **Users** - Authentication and profile information
- **Quizzes** - Quiz metadata and configuration
- **Questions** - Individual quiz questions and answers
- **Submissions** - User quiz attempts and results
- **Progress** - Learning progress and achievements

### AI Models
- **AI Sessions** - AI-generated quiz sessions
- **Feedback** - Automated assessment feedback
- **Analytics** - Learning pattern analysis

## 🔧 Configuration

### Environment Variables

Create a `config/.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/holberton_db
POSTGRES_DB=holberton_db
POSTGRES_USER=holberton_user
POSTGRES_PASSWORD=secure_password

# Security Settings
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=false
HOST=0.0.0.0
PORT=8000
APP_NAME=Holberton Learning Platform

# AI Integration
OPENAI_API_KEY=your-openai-api-key
MAX_QUIZ_QUESTIONS=10
```

### Database Setup

```bash
# Initialize database
python tools/scripts/init_db.py

# Create tables
python tools/scripts/create_tables.py

# Populate with sample data
python tools/scripts/populate_db_balanced.py

# Create admin user
python tools/scripts/create_admin.py
```

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=src/app --cov-report=html

# Run specific test categories
pytest tests/test_auth.py  # Authentication tests
pytest tests/test_api.py   # API endpoint tests
```

## 📚 API Documentation

Once the application is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

#### Quiz Management
- `GET /api/quiz/` - List available quizzes
- `POST /api/quiz/` - Create new quiz
- `GET /api/quiz/{id}` - Get quiz details
- `POST /api/quiz/{id}/submit` - Submit quiz answers

#### AI Features
- `POST /api/ai-quiz/generate` - Generate AI quiz
- `POST /api/ai-quiz/evaluate` - AI evaluation
- `GET /api/ai-quiz/feedback` - Get AI feedback

## 🚀 Deployment

### Production Deployment

1. **Prepare Environment**
   ```bash
   # Update environment variables for production
   cp config/.env.example config/.env.production
   # Edit production settings
   ```

2. **Deploy with Docker**
   ```bash
   cd deployment
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Set Up Reverse Proxy**
   - Configure nginx or Apache as reverse proxy
   - Set up SSL/TLS certificates
   - Configure domain and DNS

4. **Database Migration**
   ```bash
   # Run database migrations
   docker-compose exec web alembic upgrade head
   ```

### Performance Optimization

- Use Redis for session storage and caching
- Implement CDN for static assets
- Set up database connection pooling
- Configure horizontal scaling with load balancer

## 📖 Documentation

- [Installation Guide](docs/INSTALL.md) - Detailed setup instructions
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md) - Technical overview
- [CSS Global Guide](docs/CSS_GLOBAL_GUIDE.md) - Styling guidelines
- [Video Instructions](docs/VIDEO_INSTRUCTIONS.md) - Video tutorials

### Directory Documentation
- [Source Code](src/README.md) - Code structure and components
- [Configuration](config/README.md) - Settings and environment
- [Tools](tools/README.md) - Development utilities
- [Deployment](deployment/README.md) - Docker and deployment
- [Tests](tests/README.md) - Testing guidelines

## 🤝 Contributing

1. **Fork the Repository**
   ```bash
   git fork https://github.com/Krapaud/project-holbies.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow coding standards
   - Add tests for new features
   - Update documentation

4. **Run Tests**
   ```bash
   pytest tests/
   ```

5. **Submit Pull Request**
   - Describe changes clearly
   - Reference related issues
   - Ensure CI passes

### Code Standards

- **Python**: Follow PEP 8 style guide
- **JavaScript**: Use modern ES6+ features
- **HTML/CSS**: Semantic markup and responsive design
- **Documentation**: Clear docstrings and comments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Holberton School** - Educational foundation and inspiration
- **FastAPI Community** - Excellent framework and documentation
- **Matrix Universe** - Aesthetic inspiration for the interface
- **Open Source Community** - Tools and libraries that make this possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Krapaud/project-holbies/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Krapaud/project-holbies/discussions)
- **Email**: support@holbies.dev

---

⭐ **Star this repository if you found it helpful!**

Built with ❤️ for the Holberton community

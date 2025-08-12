# Source Code Directory

This directory contains the main source code for the Holberton Learning Platform.

## Structure

```
src/
├── main.py              # FastAPI application entry point
├── app/                 # Core application package
│   ├── __init__.py
│   ├── auth.py          # Authentication logic
│   ├── database.py      # Database configuration and connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas for API
│   └── routers/         # API route handlers
│       ├── __init__.py
│       ├── ai_quiz.py   # AI-powered quiz endpoints
│       ├── auth.py      # Authentication endpoints
│       ├── quiz.py      # Quiz management endpoints
│       ├── tutor.py     # Tutoring system endpoints
│       └── users.py     # User management endpoints
├── static/              # Static web assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   ├── images/          # Images and icons
│   ├── fonts/           # Font files
│   └── video/           # Video content
└── templates/           # Jinja2 HTML templates
    ├── base.html        # Base template
    ├── index.html       # Homepage
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── dashboard.html   # User dashboard
    ├── quiz.html        # Quiz interface
    ├── ai-quiz.html     # AI quiz interface
    └── learning.html    # Learning modules
```

## Key Components

### FastAPI Application (`main.py`)
- Main application setup and configuration
- Route definitions for web pages
- Static file serving
- Session management
- Template rendering

### Application Package (`app/`)
- **models.py**: Database models using SQLAlchemy ORM
- **schemas.py**: Request/response validation using Pydantic
- **database.py**: Database connection and session management
- **auth.py**: Authentication and authorization utilities

### API Routers (`app/routers/`)
- Modular API endpoints organized by functionality
- RESTful API design
- Authentication integration
- Error handling and validation

### Frontend (`static/` and `templates/`)
- Modern responsive web interface
- Matrix-themed design
- Interactive JavaScript components
- Mobile-friendly layouts

## Development

To work with the source code:

```bash
# Install dependencies
pip install -r config/requirements.txt

# Run the development server
python run.py

# Or run directly
python src/main.py
```

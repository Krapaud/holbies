# Tools Directory

This directory contains utility scripts and development tools for the Holberton Learning Platform.

## Database Management Scripts

### Core Database Operations
- `init_db.py` - Initialize the database with required tables and indexes
- `create_tables.py` - Create database tables from SQLAlchemy models
- `reset_db.py` - Reset database to initial state (keeps structure, clears data)
- `complete_reset_db.py` - Complete database reset (drops and recreates everything)
- `force_reset_db.py` - Force reset database bypassing safeguards
- `sqlalchemy_reset.py` - SQLAlchemy-specific database reset utilities

### Data Population
- `populate_db_balanced.py` - Populate database with balanced test data
- `create_test_user.py` - Create test users for development
- `create_admin.py` - Create admin users with elevated privileges

### User Management
- `delete_all_users.py` - Remove all users from the database (development only)

### AI and Quiz Tools
- `ai_quiz_corrector.py` - AI-powered quiz correction and validation system

## Usage

From the project root directory:

```bash
# Initialize database
python tools/scripts/init_db.py

# Create an admin user
python tools/scripts/create_admin.py

# Populate with test data
python tools/scripts/populate_db_balanced.py

# Reset database
python tools/scripts/reset_db.py
```

## Safety Notes

⚠️ **Warning**: Database reset scripts will permanently delete data. Use with caution, especially in production environments.

Always backup your database before running any reset scripts.

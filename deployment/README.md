# Deployment Directory

This directory contains all deployment-related files for the Holberton Learning Platform.

## Files

- `Dockerfile` - Docker container configuration for the application
- `docker-compose.yml` - Multi-container Docker setup with PostgreSQL
- `wait-for-postgres.sh` - Script to wait for PostgreSQL to be ready before starting the app

## Quick Start

From the project root directory:

```bash
# Start the application with Docker Compose
cd deployment
docker-compose up --build

# Stop the application
docker-compose down

# View logs
docker-compose logs -f web
```

## Environment Variables

Make sure to create a `.env` file in the `config/` directory with the required environment variables:

```env
# Database
POSTGRES_DB=holberton_db
POSTGRES_USER=holberton_user
POSTGRES_PASSWORD=secure_password
DATABASE_URL=postgresql://holberton_user:secure_password@db:5432/holberton_db

# Security
SECRET_KEY=your-super-secret-key-here

# Application
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

## Production Deployment

For production deployment:

1. Ensure all environment variables are properly set
2. Use a reverse proxy (nginx) in front of the application
3. Set up SSL/TLS certificates
4. Configure proper logging and monitoring
5. Set up database backups

## Docker Commands

```bash
# Build only
docker-compose build

# Run in background
docker-compose up -d

# Scale the web service
docker-compose up --scale web=3

# Reset everything
docker-compose down -v
docker-compose up --build
```

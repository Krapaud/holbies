# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de requirements
COPY config/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY src/ ./src/
COPY scripts/user_management/ ./scripts/user_management/
COPY config/ ./config/
COPY deployment/wait-for-postgres.sh ./deployment/

# Rendre le script wait-for-postgres exécutable
RUN chmod +x ./deployment/wait-for-postgres.sh

# Créer un lien symbolique pour que l'import app fonctionne
RUN ln -sf /app/src/app /app/app

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONPATH=/app/src
ENV HOST=0.0.0.0
ENV PORT=8000

# Commande de démarrage
CMD ["python", "src/main.py"]

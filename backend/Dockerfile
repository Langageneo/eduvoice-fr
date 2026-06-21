# EduVoice FR™ - Backend Dockerfile
# Fichier: backend/Dockerfile

FROM python:3.12-slim

# --- Dépendances système ---
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# --- Répertoire de travail ---
WORKDIR /app

# --- Copier les fichiers ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copier le code ---
COPY . .

# --- Variables d'environnement ---
ENV REDIS_URL=redis://redis:6379
ENV POSTGRES_URL=postgresql://user:password@postgres:5432/eduvoice
ENV PYTHONPATH=/app

# --- Exposer le port ---
EXPOSE 8000

# --- Commande de démarrage ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

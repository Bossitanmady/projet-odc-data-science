# Utilisation de l'image Python officielle (version Slim pour une taille réduite)
FROM python:3.12.4-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port par défaut (modifiable via $PORT)
ENV PORT=80
EXPOSE $PORT

# Création et utilisation d'un utilisateur non root pour des raisons de sécurité
RUN useradd -m appuser
USER appuser

# Commande pour démarrer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "$PORT"]

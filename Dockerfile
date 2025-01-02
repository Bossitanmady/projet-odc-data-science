# Utiliser une image légère Python
FROM python:3.12.4-slim

# Définir un répertoire de travail
WORKDIR /app

# Copier uniquement les fichiers nécessaires pour installer les dépendances
COPY requirements.txt /app/requirements.txt

# Installer les dépendances dans un environnement minimal
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code dans le conteneur
COPY . /app

# Exposer le port pour Uvicorn
EXPOSE 80

# Commande pour démarrer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

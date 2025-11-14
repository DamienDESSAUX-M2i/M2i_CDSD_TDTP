FROM python:latest

# Dossier de travail dans le conteneur
WORKDIR /app

# Installer les dépendances Python (requirements.txt est à la racine du projet)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier le code du service generator (fichiers présents dans ./generator côté host)
COPY . /app/

# Lancer le service
CMD ["python", "main.py"]

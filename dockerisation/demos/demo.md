# Dockerisation

## Etape 1 : Initialisation

```bash
# Création de l'environnement virtuel
python -m venv .venv

# Activation de l'environnement virtuel
.venv/Scripts/activate
```

## Etape 2 : Explorer une image python

```bash
# Télécharger une image
docker pull python:3.9-slim

# Afficher la liste des images téléchargées
docker images

# Lancer un conteneur ayant pour image python:3.9-slim
# docker run (lancer)
#   -it (mode itéractif)
#   python:3.9-slim (image)
#   python (commande lancée)
docker run -it python:3.9-slim python
docker run -it python:3.9-slim bash

# Exécuter un script local via docker
# docker run (lancer)
#   -v (créer volume)
#   ${PWD}:/app (chemin_local:chemin_dans_le_conteneur)
#   python:3.9-slim (image)
#   python /app/test.py (commande)
docker run -v ${PWD}:/app python:3.9-slim python /app/test.py
```

## Etape 3 : Gérer les conteneurs

```bash
# Lancer un conteneur en arrière plan
docker run -d --name my_container python:3.9-slim

# Voir les conteneurs en cours d'exécution
docker ps

# Arrêter un conteneur
docker stop my_container

# Supprimer un conteneur
docker rm my_container
```

## Etape 4 : Projet ML conteneurisé

### Structure du projet

```
demo_ml/
├───.venv/
├───train_simple.py
├───README.md
├───requirements.txt
└───Dockerfile
```

### Fichiers

**requirements.txt**

```txt
joblib==1.5.3
numpy==2.4.4
pandas==3.0.2
python-dateutil==2.9.0.post0
scikit-learn==1.8.0
scipy==1.17.1
six==1.17.0
threadpoolctl==3.6.0
tzdata==2026.1
```

**Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train_simple.py .

ENTRYPOINT ["python", "train_simple.py"]
```

### Build image

On se place à la racine du dossier `docker_ml`.

```bash
# Construire une image
# docker build (contruire une image)
#   -t (afficher dans le terminal)
#   docker_ml_simple (nom du build)
#   . (chemin vers le Dockerfile)
docker build -t docker_ml_simple .

# Lancer un conteneur
docker run --name container_ml_simple docker_ml_simple
```

# Volume Docker

## Bind mount

```bash
# Build image
docker build -t data-generator .

# Lancer un conteneur avec un volume bind mount
docker run -v ${PWD}/data_output:/app/data_output data-generator
```

## Named volumes

```bash
# Créer un volume
docker volume create my-volume

# Liste de volumes
docker volume ls

# Lancer un conteneur avec un volume nommé
docker run -v my-volume:/app/data_output data-generator

# Vérifier le contenu d'un volume
docker run --rm -v my-volume:/volume alpine ls -lh /volume
```

# Variables d'environnement

## Commande

```bash
docker run --rm -e MESSAGE="Hello World!" python:3.11-slim python -c "import os;print(os.getenv('MESSAGE', 'error'))"
```

## Fichier d'environnement

```yaml
NAME="Lucky Luke"
AGE="79"
```

```bash
docker build -t hello .
docker run --rm --env-file .env hello
```

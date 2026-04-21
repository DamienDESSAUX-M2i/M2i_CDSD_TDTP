# Dockerisation – Exercice 5

## Description

Ce projet est une API REST simple développée avec Flask permettant de simuler une prédiction à partir d’une donnée d’entrée (`feature`).

Chaque prédiction est :

* générée aléatoirement (simulation)
* stockée dans une base de données PostgreSQL
* consultable via un endpoint d’historique

L’ensemble est entièrement conteneurisé avec Docker et orchestré via Docker Compose.

## Architecture

Le projet repose sur trois services :

* **api_exo5** : API Flask (port 5000)
* **postgres_exo5** : base de données PostgreSQL (port 5432)
* **pgadmin_exo5** : interface web de gestion PostgreSQL (port 8080)

## Structure du projet

```
.
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── postgres/
│   └── init.sql
├── .env
├── docker-compose.yml
└── README.md
```

## Configuration

### Variables d’environnement (`.env`)

Exemple :

```
POSTGRES_USER=username
POSTGRES_PASSWORD=userpassword
POSTGRES_DBNAME=mydb

PGADMIN_EMAIL=username@example.com
PGADMIN_PASSWORD=userpassword
```

## Lancement du projet

### 1. Build et démarrage

```bash
docker-compose up -d
```

### 2. Vérifier les services

* API : [http://localhost:5000](http://localhost:5000)
* pgAdmin : [http://localhost:8080](http://localhost:8080)

## Endpoints API

### POST `/predict`

Simule une prédiction et l’enregistre en base.

#### Requête :

```json
{
  "feature": "example_value"
}
```

#### Réponse :

```json
{
  "success": true,
  "data": {
    "id": 1,
    "feature": "example_value",
    "prediction": 1,
    "probability": 0.73
  }
}
```

### GET `/history`

Récupère toutes les prédictions enregistrées.

#### Réponse :

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "feature": "example_value",
      "prediction": 1,
      "probability": 0.73
    }
  ]
}
```

## Base de données

La table `predictions` est initialisée automatiquement via un script SQL :

```sql
CREATE TABLE IF NOT EXISTS predictions (
    prediction_id SERIAL PRIMARY KEY,
    feature VARCHAR(255) NOT NULL,
    prediction INTEGER NOT NULL,
    probability FLOAT NOT NULL
);
```

## Test avec curl

### POST

```bash
curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"feature": "test"}'
```

### GET

```bash
curl http://localhost:5000/history
```

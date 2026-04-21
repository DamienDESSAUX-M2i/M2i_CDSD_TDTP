# Exercice 3 : Networking - Système de Prédiction ML Multi-Conteneurs

## Objectif

Créer une architecture multi-conteneurs avec networking pour un système de prédiction ML :

- **API** : Service de prédiction Flask
- **Database** : PostgreSQL pour stocker les résultats

## Tâche 1 : Créer une API de prédiction avec base de données

Créez une API Flask qui :

1. Se connecte à PostgreSQL
2. Expose un endpoint `/predict` qui :
   - Génère une prédiction aléatoire (simulant un modèle ML)
   - Génère des métriques aléatoires (accuracy, precision, recall) via `random.uniform()`
   - Stocke la prédiction avec ses métriques dans PostgreSQL
3. Expose un endpoint `/history` qui retourne l'historique des prédictions stockées

**Structure attendue** :

```
exercice3/
├── api/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── init.sql
└── README.md
```

### requirements.txt

```
flask==3.0.0
psycopg2-binary==2.9.9
```

### Dockerfile

### init.sql

## Étapes à suivre

### Étape 1 : Créer un réseau Docker

```bash
docker network create ml-network
```

### Étape 2 : Lancer PostgreSQL sur ce réseau

### Étape 3 : Construire et lancer l'API sur le même réseau

### Étape 4 : Tester tous les endpoints

## Tâche 2 : Tests de communication réseau

Effectuez les tests suivants pour valider l'architecture réseau :

### Test 1 : Vérifier que les conteneurs sont sur le même réseau

```bash
docker network inspect ml-network
```

### Test 2 : Tester la résolution DNS depuis l'API

```bash
docker exec api ping -c 2 db
```

### Test 3 : Tester la connexion DB depuis un conteneur temporaire

```bash
docker run --rm --network ml-network \
  postgres:13-alpine \
  psql -h db -U postgres -d mldb -c "SELECT COUNT(*) FROM predictions;"
```

### Test 4 : Vérifier les logs des services

```bash
docker logs api
docker logs db
```

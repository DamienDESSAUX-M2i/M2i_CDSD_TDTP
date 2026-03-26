# Backend FastAPI + SQLite + modèle PKL

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

## Base de données

Le fichier SQLite sera créé automatiquement :

```text
predictions.db
```

## Endpoints

### POST `/predict-intent`

Corps JSON :

```json
{
  "first_name": "Chris",
  "text": "bonjour, j'ai un problème de paiement"
}
```

### GET `/predictions`

Retourne l'historique des prédictions enregistrées.

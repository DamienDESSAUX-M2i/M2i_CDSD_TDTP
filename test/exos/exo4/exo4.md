# Exercice Pratique : API de Machine Learning avec Tests Pytest

## Contexte

Vous travaillez pour une entreprise de e-commerce qui souhaite prédire le taux de satisfaction client basé sur des métriques comportementales. Votre mission est de créer une API Flask qui expose un modèle de ML et d'écrire des tests complets avec pytest.

## Objectifs

1. Créer une API Flask avec plusieurs endpoints
2. Écrire des tests unitaires et d'intégration avec pytest
3. Atteindre une couverture de tests > 80%
4. Gérer les cas d'erreur et la validation des données

## Le Modèle

Un fichier `train_satisfaction_model.py` vous est fourni qui entraîne un modèle prédisant la **satisfaction client** (0-4 étoiles) basé sur 5 features :

- `order_count` : nombre de commandes (0-50)
- `avg_order_value` : valeur moyenne des commandes (10-500€)
- `days_since_last_order` : jours depuis la dernière commande (0-365)
- `returns_count` : nombre de retours (0-10)
- `support_tickets` : nombre de tickets support (0-15)

## Partie 1 : Créer l'API (app_satisfaction.py)

### Endpoints à implémenter :

#### 1. `GET /health`
- Retourne le statut de santé de l'API
- Doit inclure : `status`, `model_loaded`, `timestamp`
- Status code : 200

#### 2. `POST /predict`
Prédiction individuelle

**Request body :**
```json
{
  "features": [25, 150.5, 30, 2, 3]
}
```

**Response :**
```json
{
  "satisfaction_score": 3,
  "confidence": 0.85,
  "timestamp": "2024-01-15T10:30:00"
}
```

**Validations à implémenter :**
- Vérifier que `features` existe
- Vérifier que le tableau contient exactement 5 éléments
- Vérifier que toutes les valeurs sont numériques
- Retourner 400 si invalide, 503 si modèle non chargé

#### 3. `POST /predict_batch`
Prédictions multiples

**Request body :**
```json
{
  "customers": [
    {
      "customer_id": "CUST001",
      "features": [25, 150.5, 30, 2, 3]
    },
    {
      "customer_id": "CUST002",
      "features": [10, 80.0, 120, 5, 8]
    }
  ]
}
```

**Response :**
```json
{
  "predictions": [
    {
      "customer_id": "CUST001",
      "satisfaction_score": 3,
      "confidence": 0.85
    },
    {
      "customer_id": "CUST002",
      "satisfaction_score": 1,
      "confidence": 0.72
    }
  ],
  "total_processed": 2
}
```

#### 4. `GET /stats`
Statistiques des prédictions

- Retourne le nombre total de prédictions
- La moyenne des scores de satisfaction prédits
- Le timestamp de la dernière prédiction

## Partie 2 : Écrire les Tests (test_app_satisfaction.py)

### Tests à implémenter :

#### Classe `TestHealthEndpoint`
- [ ] Test que l'endpoint retourne 200
- [ ] Test que la réponse est en JSON
- [ ] Test que le status est "healthy"
- [ ] Test que `model_loaded` est un booléen
- [ ] Test que le timestamp est présent

#### Classe `TestPredictEndpoint`
- [ ] Test avec des données valides
- [ ] Test sans le champ `features`
- [ ] Test avec un nombre incorrect de features (3 au lieu de 5)
- [ ] Test avec des valeurs non numériques
- [ ] Test que le score est entre 0 et 4
- [ ] Test que la confidence est entre 0 et 1
- [ ] Test avec des features à 0
- [ ] Test avec des features négatives (doit échouer)

#### Classe `TestPredictBatchEndpoint`
- [ ] Test avec 2 clients valides
- [ ] Test avec une liste vide
- [ ] Test avec un customer_id manquant
- [ ] Test que `total_processed` correspond au nombre de clients
- [ ] Test avec 10+ clients (performance)

#### Classe `TestStatsEndpoint`
- [ ] Test que les stats sont à 0 au départ
- [ ] Test que les stats augmentent après des prédictions
- [ ] Test que la moyenne est correctement calculée

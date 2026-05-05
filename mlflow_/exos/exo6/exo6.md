# TP MLOps Maintenance Prédictive Industrielle

## Contexte

Une entreprise manufacturière exploite plusieurs centaines de machines CNC réparties sur différents sites de production. Chaque arrêt non planifié coûte en moyenne **12 000 €/heure**. L'équipe data souhaite déployer un système de maintenance prédictive capable d'anticiper les pannes à partir des données capteurs des machines.

Votre mission est de construire et déployer un pipeline MLOps complet : de l'entraînement du modèle jusqu'à son exposition via une API REST conteneurisée.

## Dataset — AI4I 2020 Predictive Maintenance

Le dataset est disponible sur l'[UCI ML Repository](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) (10 000 observations).

`Type` - Catégorielle - Qualité du produit : L (Low), M (Medium), H (High)
`Air temperature [K]` - Numérique - Température ambiante
`Process temperature [K]` - Numérique - Température du process
`Rotational speed [rpm]` - Numérique - Vitesse de rotation de la broche
`Torque [Nm]` - Numérique - Couple moteur
`Tool wear [min]` - Numérique - Durée d'usure de l'outil
`Machine failure` - Binaire - **Variable cible** — 0 : OK, 1 : Panne

**Note** : Les colonnes `TWF`, `HDF`, `PWF`, `OSF`, `RNF` représentent les modes de défaillance individuels. Vous ne les utiliserez pas comme features.

## Structure attendue du projet

```
mlops-predictive-maintenance/
├── data/
│   └── ai4i2020.csv
├── src/
│   ├── preprocess.py
│   └── train.py
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── model_loader.py
├── tests/
│   ├── test_preprocess.py
│   ├── test_model.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Partie 1 — Preprocessing & Entraînement avec MLflow

### 1.1 — Chargement et exploration des données

Commencez par une analyse exploratoire rapide dans un notebook ou un script Python.

1. Quelle est la répartition des classes (pannes vs. non-pannes)
2. Y a-t-il des valeurs manquantes ?
3. Quelle feature vous semble la plus corrélée avec la variable cible ?

### 1.2 — Pipeline de preprocessing (`src/preprocess.py`)

Implémentez les fonctions suivantes dans `src/preprocess.py` :

**a) `load_raw_data(path: str) -> pd.DataFrame`**

Charge le CSV et renomme les colonnes en snake_case

Supprimez également les colonnes inutiles : `UDI`, `Product ID`, `TWF`, `HDF`, `PWF`, `OSF`, `RNF`.

**b) `add_engineered_features(df: pd.DataFrame) -> pd.DataFrame`**

Ajoutez trois features dérivées des mesures capteurs, justifiées par le contexte métier :

`temp_delta` : `process_temperature - air_temperature` Mesure le stress thermique subi par la pièce  
`power_proxy` : `rotational_speed × torque` Estimation de la puissance mécanique consommée
`wear_per_rpm` : `tool_wear / (rotational_speed + 1e-6)` Taux d'abrasion normalisé par la vitesse |

**Attention** : La fonction ne doit **pas modifier** le DataFrame original (utilisez `.copy()`).

**c) `get_feature_pipeline() -> ColumnTransformer`**

Construisez un `ColumnTransformer` sklearn qui :

- Applique un `StandardScaler` sur les features numériques
- Applique un `OrdinalEncoder` sur la feature `type` avec l'ordre `["L", "M", "H"]`

### 1.3 — Script d'entraînement avec tracking MLflow (`src/train.py`)

Implémentez la fonction `train()` qui :

1. Charge et prépare les données via les fonctions de `preprocess.py`
2. Applique le feature engineering
3. Effectue un split stratifié train/test (80/20)
4. Construit un pipeline `imbalanced-learn` incluant :
   - Le preprocessor
   - Un `SMOTE` pour rééquilibrer les classes
   - Un `RandomForestClassifier(class_weight="balanced", random_state=42)`
5. Lance une cross-validation stratifiée à 5 folds sur le train set
6. Entraîne le pipeline final
7. Log dans MLflow :
   - Les **paramètres** : `model_name`, `n_estimators`, `use_smote`, `test_size`
   - Les **métriques** : `f1_score`, `recall`, `precision`, `roc_auc`, `cv_f1_mean`
   - Le **modèle** avec sa signature et un input example
8. Enregistre le modèle dans le **MLflow Model Registry** sous le nom `predictive-maintenance-model`

## Partie 2 — Serving avec FastAPI

### 2.1 — Schémas Pydantic (`api/schemas.py`)

Implémentez les modèles Pydantic suivants :

**`PredictionRequest`** — Valide les données capteurs en entrée

**`PredictionResponse`** — Retourne le résultat enrichi

### 2.2 — Chargeur de modèle (`api/model_loader.py`)

Implémentez un `ModelLoader` qui :

1. Charge le modèle depuis le MLflow Model Registry via `mlflow.sklearn.load_model("models:/predictive-maintenance-model/latest")`
2. En cas d'échec du Registry, tente de charger depuis le dernier run disponible de l'expériment `predictive-maintenance`
3. Expose une propriété `is_loaded` (bool) et `version` (str)
4. Expose les méthodes `predict(X)` et `predict_proba(X)`

### 2.3 — Application FastAPI (`api/main.py`)

Implémentez l'application FastAPI avec les endpoints suivants :

**`GET /health`** — Retourne l'état de l'API et du modèle chargé

**`GET /metrics`** — Retourne depuis le démarrage :

- Nombre total de prédictions
- Nombre de prédictions de panne
- Taux de pannes

**`POST /predict`** — Prédiction unitaire :

Le niveau de risque est calculé selon la probabilité de panne :

| Probabilité | Niveau   | Action recommandée                  |
| ----------- | -------- | ----------------------------------- |
| < 0.2       | LOW      | Aucune action requise               |
| 0.2 – 0.5   | MEDIUM   | Planifier une inspection préventive |
| 0.5 – 0.75  | HIGH     | Inspection dans les 24h             |
| ≥ 0.75      | CRITICAL | Arrêt immédiat recommandé           |

**`POST /predict/batch`** — Prédiction en lot (maximum 100 machines par appel)

**Remarque** : Le chargement du modèle doit se faire au démarrage de l'application via le mécanisme `lifespan` de FastAPI (et non via `@app.on_event` déprécié).

## Partie 3 — Conteneurisation Docker

### 3.1 — Dockerfile

Rédigez un `Dockerfile` pour l'API

### 3.2 — Docker Compose (`docker-compose.yml`)

Définissez une stack Docker Compose avec trois services :

**`mlflow`** : Serveur MLflow avec :

- Persistance via un volume nommé
- Backend SQLite (`--backend-store-uri sqlite:///mlflow/mlflow.db`)
- Healthcheck sur `http://localhost:5000/health`
- image : `ghcr.io/mlflow/mlflow:v2.13.0`

**`trainer`** : Service one-shot qui :

- Lance `python src/train.py` après que MLflow soit healthy
- Redémarre jamais (`restart: "no"`)

**`api`** : Service FastAPI qui :

- Démarre après MLflow
- Expose le port 8000
- Récupère les variables d'environnement `MLFLOW_TRACKING_URI` et `MODEL_NAME`

Tous les services doivent être connectés via un réseau bridge dédié `mlops-network`.

### 3.3 — Vérification

Lancez la stack complète et vérifiez

## Bonus A — Tests avec pytest

Implémentez les fichiers de tests suivants (coverage minimum attendu : **70%**) :

### `tests/test_preprocess.py`

- `test_pipeline_fit_transform_shape` : la transformation ne change pas le nombre de lignes
- `test_numeric_features_are_scaled` : après StandardScaler, les features numériques sont centrées
- `test_categorical_encoding` : L→0, M→1, H→2 après OrdinalEncoder
- `test_temp_delta_computed` : `temp_delta = process_temperature - air_temperature`
- `test_wear_per_rpm_no_division_by_zero` : pas d'inf/NaN quand `rotational_speed = 0`
- `test_original_df_not_mutated` : `add_engineered_features` ne modifie pas le DataFrame d'entrée

### `tests/test_model.py`

- `test_probabilities_in_valid_range` : toutes les probabilités sont dans [0, 1]
- `test_predictions_are_binary` : les prédictions sont exclusivement 0 ou 1
- `test_model_is_not_trivial` : le modèle ne prédit pas uniquement la classe 0
- `test_deterministic_predictions` : deux appels successifs donnent le même résultat
- `test_recall_above_threshold` : Recall ≥ 0.3 sur un jeu de test synthétique
- `test_roc_auc_above_threshold` : ROC-AUC ≥ 0.55 (mieux que le hasard)

### `tests/test_api.py`

Utilisez `unittest.mock.patch` pour mocker le `model_loader` (pas de dépendance à MLflow dans les tests).

- `test_health_returns_200` : le endpoint `/health` répond 200
- `test_predict_returns_200` : une requête valide retourne 200
- `test_predict_response_schema` : la réponse contient tous les champs attendus
- `test_predict_probability_range` : la probabilité est dans [0, 1]
- `test_invalid_type_returns_422` : un type invalide (ex. `"X"`) retourne 422
- `test_temperature_out_of_range_returns_422` : une température hors bornes retourne 422
- `test_batch_max_100` : un batch de 101 éléments retourne 422
- `test_metrics_increments_after_predict` : `/metrics` reflète les prédictions effectuées

## Bonus B — Pipeline CI/CD GitHub Actions

Créez `.github/workflows/ci.yml` définissant **4 jobs** exécutés sur chaque push sur `main` :

**Job 1 — Tests & Qualité** (`test`) :

- Setup Python 3.11
- Installation des dépendances
- Exécution de tous les tests pytest avec coverage ≥ 70%

**Job 2 — Build Docker** (`build`) :

- Dépend de `test`
- Build et push de l'image vers GitHub Container Registry (GHCR)
- Tagging automatique : `latest` sur `main`, `sha-<commit>` sinon

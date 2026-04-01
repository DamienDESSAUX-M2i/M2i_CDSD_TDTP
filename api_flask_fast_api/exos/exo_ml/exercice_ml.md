# TP: API ML Production-Ready — FastAPI + scikit-learn + Docker


## Contexte

Vous développez une API de classification de fleurs Iris. Le projet suit une architecture en couches séparées dans plusieurs fichiers. Le modèle est entraîné en amont via un script dédié, puis chargé au démarrage de l'API.

---

## Structure du projet

Reproduisez exactement cette arborescence :

```
ml-api/
├── models/
│   └── iris_model.pkl          # généré par le script d'entraînement
├── src/
│   ├── main.py                 # application FastAPI
│   ├── models.py               # modèles Pydantic
│   ├── ml_utils.py             # chargement et inférence ML
│   └── config.py               # configuration
├── scripts/
│   ├── train.py                # entraînement du modèle
│   └── evaluate.py             # évaluation (extension)
├── tests/
│   ├── test_api.py
│   ├── test_models.py
│   └── test_ml.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── docker-compose.yml
```

**Stack** : FastAPI, scikit-learn, pytest, Docker.

---

## Phase 1 : Entraînement du modèle — `scripts/train.py`

Écrivez un script autonome qui réalise le pipeline complet suivant :

1. Charger le dataset Iris depuis `sklearn.datasets`.
2. Splitter les données : 80 % entraînement / 20 % test, stratifié, `random_state=42`.
3. Entraîner un `RandomForestClassifier` (100 estimateurs, `random_state=42`, `n_jobs=-1`).
4. Évaluer le modèle sur le jeu de test (accuracy et F1-score weighted).
5. Créer le répertoire `models/` s'il n'existe pas, puis sauvegarder le modèle en pickle dans `models/iris_model.pkl`.
6. Générer un rapport JSON dans `models/training_report.json` contenant : date d'entraînement, accuracy, f1_score, nombre de samples train/test, classes, noms de features, importance de chaque feature, et le classification report complet.

Toutes les étapes doivent être loggées avec le module `logging`.

Le script doit être exécutable directement :
```bash
python scripts/train.py
```

---

## Phase 2 : Configuration — `src/config.py`

Créez une classe `Settings` héritant de `BaseSettings` (pydantic-settings) avec les champs :

| Champ | Type | Valeur par défaut |
|---|---|---|
| `app_name` | `str` | `"ML Iris API"` |
| `debug` | `bool` | `False` |
| `log_level` | `str` | `"INFO"` |
| `model_path` | `str` | `"models/iris_model.pkl"` |
| `report_path` | `str` | `"models/training_report.json"` |

Le fichier `.env` doit être supporté. Exposez une fonction `get_settings()` avec `@lru_cache`.

---

## Phase 3 : Modèles Pydantic — `src/models.py`

Définissez les modèles suivants :

**`IrisClass`** (enum str) : `setosa`, `versicolor`, `virginica`.

**`PredictionInput`** : les quatre mesures de la fleur, toutes `float > 0` sauf `petal_width` qui est `≥ 0`.

| Champ | Contrainte |
|---|---|
| `sepal_length` | `> 0` |
| `sepal_width` | `> 0` |
| `petal_length` | `> 0` |
| `petal_width` | `≥ 0` |

**`PredictionOutput`** : `prediction` (IrisClass), `confidence` (float entre 0 et 1), `probabilities` (dict str → float).

**`HealthResponse`** : `status` (str), `model_loaded` (bool), `accuracy` (float optionnel).

---

## Phase 4 : Utilitaires ML — `src/ml_utils.py`

Créez une classe `MLModel` instanciée avec le chemin du fichier pickle.

### `load_model(model_path)`

Charge le modèle depuis le fichier pickle. Lève `FileNotFoundError` si le fichier n'existe pas. Charge également le rapport JSON si `training_report.json` est présent dans le même répertoire.

### `predict(features: np.ndarray) → tuple`

Retourne un triplet `(prediction_class, confidence, probs_dict)` :
- `prediction_class` : nom de la classe prédite (str)
- `confidence` : probabilité de la classe prédite (float)
- `probs_dict` : dictionnaire `{classe: probabilité}` pour les trois classes

Lève `RuntimeError` si le modèle n'est pas chargé.

### `get_accuracy() → Optional[float]`

Retourne l'accuracy issue du rapport JSON, ou `None` si le rapport n'est pas disponible.

---

## Phase 5 : Application FastAPI — `src/main.py`

Instanciez l'application avec titre, description et version.

### Chargement du modèle

Utilisez l'événement `startup` pour charger le modèle via `MLModel`. En cas d'échec, loggez l'erreur sans faire crasher l'application.

### Endpoints

**`GET /health`** → `HealthResponse`  
Retourne le statut de l'API et si le modèle est chargé. Retourne HTTP 503 si le modèle n'est pas disponible.

**`POST /predict`** → `PredictionOutput`  
Accepte un `PredictionInput`, construit le tableau numpy, appelle `ml_model.predict()`, retourne le résultat. Retourne HTTP 503 si le modèle n'est pas chargé, HTTP 500 en cas d'erreur d'inférence.

**`GET /info`**  
Retourne les métadonnées du modèle : type, accuracy, f1_score, classes, features, date d'entraînement. Retourne HTTP 503 si le rapport n'est pas disponible.


---

## Phase 6 : Containerisation

### `requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
scikit-learn==1.3.2
numpy==1.24.3
pytest==7.4.3
pytest-cov==4.1.0
httpx==0.25.2
```

### `Dockerfile`

Rédigez un Dockerfile basé sur `python:3.11-slim` qui :
1. Définit `/app` comme répertoire de travail.
2. Copie et installe `requirements.txt` sans cache pip.
3. Copie `scripts/`, `src/` et `models/`.
4. Définit `PYTHONUNBUFFERED=1` et `PYTHONDONTWRITEBYTECODE=1`.
5. Expose le port 8000.
6. Lance l'API avec uvicorn sur `0.0.0.0:8000`.

### `.dockerignore`

Excluez : `__pycache__`, `*.pyc`, `*.pyo`, `.pytest_cache`, `.coverage`, `htmlcov`, `.DS_Store`, `.env`, `.git`, `.gitignore`, `README.md`.

### `docker-compose.yml`

Définissez un service `ml-api` qui :
- Build depuis le contexte local.
- Expose le port `8000:8000`.
- Passe les variables d'environnement `DEBUG=False` et `LOG_LEVEL=INFO`.
- Monte `./models:/app/models` pour persister le modèle.
- Déclare un healthcheck sur `GET http://localhost:8000/health` (interval 30s, timeout 10s, 3 retries, start_period 40s).

---

## Ordre d'exécution conseillé

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Entraîner le modèle
python scripts/train.py

# 3. Lancer les tests
pytest --cov=src tests/

# 4. Démarrer l'API en local
uvicorn src.main:app --reload

# 5. Containeriser
docker-compose up -d
```

---

## Checklist de rendu

- [ ] `scripts/train.py` génère `models/iris_model.pkl` et `models/training_report.json`
- [ ] `GET /health` retourne 200 avec `model_loaded: true`
- [ ] `POST /predict` retourne la classe, la confidence et les probabilités
- [ ] `GET /info` retourne les métadonnées du modèle
- [ ] L'image Docker se construit sans erreur
- [ ] `docker-compose up` démarre l'API accessible sur le port 8000
 
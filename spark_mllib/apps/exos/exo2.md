# Exercice Données Météo

## Contexte

Vous allez implémenter les trois grands types d'apprentissage avec Spark MLlib sur des données météorologiques :

- **Partie A — Régression** : prédire la température maximale journalière à partir de mesures atmosphériques
- **Partie B — Classification** : prédire si le lendemain sera pluvieux

## Partie A — Régression : Prédire la température maximale

### Description du dataset `weather_data.csv`

| Colonne           | Type   | Description                                         |
| ----------------- | ------ | --------------------------------------------------- |
| `station_id`      | string | Identifiant de la station météo                     |
| `month`           | int    | Mois de la mesure (1 à 12)                          |
| `humidity`        | float  | Humidité relative en % (peut être null)             |
| `pressure_hpa`    | float  | Pression atmosphérique en hPa (peut être null)      |
| `wind_speed_kmh`  | float  | Vitesse du vent en km/h                             |
| `cloud_cover_pct` | float  | Couverture nuageuse en %                            |
| `uv_index`        | float  | Indice UV (0 à 11)                                  |
| `season`          | string | Saison : `spring`, `summer`, `fall`, `winter`       |
| `region`          | string | Région : `north`, `south`, `east`, `west`, `center` |
| `temperature_max` | float  | **Cible** : température maximale du jour en °C      |

### Chargement et exploration

Charger le fichier `/data/weather_data.csv` avec `header=True` et `inferSchema=True`.

- Afficher le schéma du DataFrame.
- Afficher les statistiques descriptives de la colonne `temperature_max` (min, max, moyenne, écart-type).
- Afficher le nombre total de lignes.

### Analyse exploratoire

- Calculer la **température moyenne par saison**, triée par ordre décroissant.
- Calculer la **température moyenne par région**, triée par ordre décroissant.
- Compter le nombre de valeurs nulles dans `humidity` et dans `pressure_hpa`.

### Pipeline de prétraitement

Construire un pipeline de prétraitement comprenant les étapes suivantes dans l'ordre :

1. **Imputer** `humidity` et `pressure_hpa` par la **médiane** → colonnes `humidity_imp` et `pressure_imp`
2. **SQLTransformer** : créer la colonne `temp_humidity_interaction = humidity_imp * uv_index / 10.0`
3. **StringIndexer** sur `season` → `season_idx` (handleInvalid="keep")
4. **StringIndexer** sur `region` → `region_idx` (handleInvalid="keep")
5. **OneHotEncoder** sur `season_idx` → `season_ohe` (dropLast=True)
6. **OneHotEncoder** sur `region_idx` → `region_ohe` (dropLast=True)
7. **VectorAssembler** avec les colonnes : `month`, `humidity_imp`, `pressure_imp`, `wind_speed_kmh`, `cloud_cover_pct`, `uv_index`, `temp_humidity_interaction`, `season_ohe`, `region_ohe` → colonne `features`
8. **StandardScaler** sur `features` → `features_scaled` (withMean=True, withStd=True)

### Entraînement de 3 modèles de régression

Effectuer un split 80/20 (seed=42). Intégrer les étapes de prétraitement dans un pipeline complet pour chaque modèle.

| Modèle                  | Paramètres                                                                                               |
| ----------------------- | -------------------------------------------------------------------------------------------------------- |
| `LinearRegression`      | maxIter=100, regParam=0.1, featuresCol="features_scaled", labelCol="temperature_max"                     |
| `RandomForestRegressor` | numTrees=100, maxDepth=6, seed=42, featuresCol="features_scaled", labelCol="temperature_max"             |
| `GBTRegressor`          | maxIter=50, stepSize=0.1, maxDepth=4, seed=42, featuresCol="features_scaled", labelCol="temperature_max" |

### Évaluation et tableau comparatif

Pour chaque modèle, calculer sur le jeu de test :

- **RMSE** (Root Mean Squared Error)
- **R²** (coefficient de détermination)
- **MAE** (Mean Absolute Error)

Afficher un tableau comparatif des trois modèles.

### Interprétabilité du meilleur modèle

Identifier le meilleur modèle selon le RMSE le plus bas.

- Si c'est un **RandomForest** ou **GBT** : afficher les **5 features les plus importantes** (featureImportances).

## Classification : Prédire la pluie

### Description du dataset `rain_prediction.csv`

| Colonne               | Type   | Description                                         |
| --------------------- | ------ | --------------------------------------------------- |
| `humidity`            | float  | Humidité relative en % (peut être null)             |
| `pressure_hpa`        | float  | Pression atmosphérique en hPa (peut être null)      |
| `wind_speed_kmh`      | float  | Vitesse du vent en km/h                             |
| `cloud_cover_pct`     | float  | Couverture nuageuse en %                            |
| `temperature_morning` | float  | Température matinale en °C                          |
| `dew_point`           | float  | Point de rosée en °C (peut être null)               |
| `season`              | string | Saison : `spring`, `summer`, `fall`, `winter`       |
| `region`              | string | Région : `north`, `south`, `east`, `west`, `center` |
| `will_rain`           | int    | **Cible** : 1 = il pleuvra, 0 = pas de pluie        |

---

### Chargement et équilibre des classes

Charger le fichier `/data/rain_prediction.csv`.

- Afficher la distribution de la colonne `will_rain` (nombre et pourcentage de 0 et de 1).
- Conclure si les classes sont équilibrées ou déséquilibrées.

### Pipeline de prétraitement (10 min)

Construire un pipeline de prétraitement comprenant :

1. **Imputer** `humidity`, `pressure_hpa` et `dew_point` par la **médiane** → colonnes `humidity_imp`, `pressure_imp`, `dew_point_imp`
2. **StringIndexer** sur `season` → `season_idx` (handleInvalid="keep")
3. **StringIndexer** sur `region` → `region_idx` (handleInvalid="keep")
4. **OneHotEncoder** sur `season_idx` → `season_ohe` et `region_idx` → `region_ohe` (dropLast=True)
5. **VectorAssembler** avec : `humidity_imp`, `pressure_imp`, `wind_speed_kmh`, `cloud_cover_pct`, `temperature_morning`, `dew_point_imp`, `season_ohe`, `region_ohe` → `features`
6. **StandardScaler** sur `features` → `features_scaled`

---

### Entraînement de 3 classifieurs

Effectuer un split 80/20 (seed=42).

| Modèle                   | Paramètres                                                                                         |
| ------------------------ | -------------------------------------------------------------------------------------------------- |
| `LogisticRegression`     | maxIter=100, regParam=0.05, family="binomial", featuresCol="features_scaled", labelCol="will_rain" |
| `RandomForestClassifier` | numTrees=100, maxDepth=8, seed=42, featuresCol="features_scaled", labelCol="will_rain"             |
| `GBTClassifier`          | maxIter=50, stepSize=0.1, maxDepth=5, seed=42, featuresCol="features_scaled", labelCol="will_rain" |

### Évaluation multi-métriques (10 min)

Pour chaque modèle, calculer :

- **Accuracy** via `MulticlassClassificationEvaluator`
- **F1-score** via `MulticlassClassificationEvaluator`

### Matrice de confusion du meilleur modèle

Identifier le meilleur modèle.

Afficher sa **matrice de confusion** en croisant les colonnes `will_rain` (valeur réelle) et `prediction` sur le jeu de test.

---

### Tableau récapitulatif

Afficher un tableau comparatif des trois classifieurs :

| Modèle             | Accuracy | F1  |
| ------------------ | -------- | --- |
| LogisticRegression | ?        | ?   |
| RandomForest       | ?        | ?   |
| GBT                | ?        | ?   |
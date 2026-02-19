# TP Prédiction de Retards Aériens

**Thème :** Vous êtes Data Scientist chez **AirAnalytics**, un service d'analyse pour les compagnies aériennes. Votre mission est de prédire les retards de vols, classifier leur sévérité, et identifier des groupes de routes similaires par clustering.

## Contexte métier

AirAnalytics reçoit des données historiques sur les vols : compagnie, aéroport de départ, distance, conditions météo, heure du vol, etc.

1. **Régression** : prédire la durée du retard en minutes
2. **Classification** : prédire si le retard est sévère (> 30 min)

## Description du dataset `flights.csv`

| Colonne              | Type   | Description                                                           |
| -------------------- | ------ | --------------------------------------------------------------------- |
| `flight_id`          | string | Identifiant du vol                                                    |
| `airline`            | string | Compagnie : `AirFrance`, `Lufthansa`, `Ryanair`, `EasyJet`, `British` |
| `origin`             | string | Aéroport de départ : `CDG`, `LHR`, `FRA`, `MAD`, `AMS`, `FCO`         |
| `destination`        | string | Aéroport d'arrivée (mêmes codes)                                      |
| `departure_hour`     | int    | Heure de départ (0-23)                                                |
| `distance_km`        | float  | Distance du vol en km                                                 |
| `nb_passengers`      | int    | Nombre de passagers                                                   |
| `weather_score`      | float  | Score météo : 0 (terrible) à 10 (parfait) (peut être null)            |
| `runway_congestion`  | float  | Indice de congestion piste 0-1 (peut être null)                       |
| `aircraft_age_years` | int    | Âge de l'avion en années                                              |
| `delay_minutes`      | float  | **Cible régression** : retard en minutes (négatif = en avance)        |
| `severe_delay`       | int    | **Cible classification** : 1 si retard > 30 min, 0 sinon              |

## Partie A — Régression : Prédire la durée du retard

**A.1** Charger `/data/flights.csv`. Afficher le schéma, les dimensions et les statistiques descriptives de `delay_minutes`.

**A.2** Analyser le dataset :

- Distribution de `delay_minutes` (min, max, moyenne, médiane, % de vols en retard > 0)
- Retard moyen par `airline` (trier du plus ponctuel au plus en retard)
- Retard moyen par `origin`

**A.3** Construire un Pipeline de preprocessing :

- Imputer `weather_score` et `runway_congestion` par la **médiane**
- Créer via `SQLTransformer` la feature `is_peak_departure` : 1 si `departure_hour` IN (7, 8, 17, 18, 19), sinon 0
- Encoder `airline` et `origin` avec `StringIndexer` + `OneHotEncoder` (`dropLast=True`)
- Assembler dans `features` : `distance_km`, `nb_passengers`, `weather_score_imp`, `runway_congestion_imp`, `aircraft_age_years`, `departure_hour`, `is_peak_departure`, `airline_ohe`, `origin_ohe`
- Standardiser avec `StandardScaler`

**A.4** Entraîner 3 modèles de régression (split 80/20, `seed=42`) :

| Modèle                  | Paramètres                                            |
| ----------------------- | ----------------------------------------------------- |
| `LinearRegression`      | `maxIter=100`, `regParam=0.1`                         |
| `RandomForestRegressor` | `numTrees=100`, `maxDepth=8`, `seed=42`               |
| `GBTRegressor`          | `maxIter=50`, `stepSize=0.1`, `maxDepth=5`, `seed=42` |

**A.5** Évaluer chaque modèle avec `RegressionEvaluator` (RMSE, R², MAE). Afficher un tableau comparatif.

## Partie B — Classification : Retard sévère ou non ? (60 min)

**B.1** Vérifier la distribution de la cible `severe_delay` (équilibre des classes).

**B.2** Utiliser **le même Pipeline de preprocessing** que la Partie A (sans le modèle de régression).

**B.3** Entraîner 3 classifieurs (même split 80/20) :

| Modèle                   | Paramètres                                                              |
| ------------------------ | ----------------------------------------------------------------------- |
| `LogisticRegression`     | `maxIter=100`, `regParam=0.05`, `family='binomial'`                     |
| `RandomForestClassifier` | `numTrees=100`, `maxDepth=8`, `featureSubsetStrategy='sqrt'`, `seed=42` |
| `GBTClassifier`          | `maxIter=50`, `stepSize=0.1`, `maxDepth=5`, `seed=42`                   |

**B.4** Pour chaque modèle, calculer :

- Accuracy, F1-Score (`MulticlassClassificationEvaluator`)

**B.5** Afficher la **matrice de confusion** du meilleur modèle.

**B.6** Pour le `RandomForestClassifier` :

- Afficher les **features les plus importantes**
- Interpréter : quelle variable prédit le mieux un retard sévère ?

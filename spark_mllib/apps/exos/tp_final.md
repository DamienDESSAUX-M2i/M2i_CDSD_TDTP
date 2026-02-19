# TP — Comparaison Scikit-learn vs Spark MLlibs

**Thème :** Vous êtes Data Scientist chez **AgroPredict**, une startup AgriTech. Votre mission est de construire deux modèles prédictifs sur des données agricoles mondiales : un modèle de **régression** pour estimer le rendement des cultures, et un modèle de **classification** pour identifier si une culture sera rentable. Chaque modèle sera implémenté dans Scikit-learn **et** Spark MLlib, puis les deux frameworks seront comparés.

csv : https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset

## Organisation des scripts

Ce TP est découpé en **trois scripts Python indépendants** :

| Script                   | Rôle                                                     |
| ------------------------ | -------------------------------------------------------- |
| `partieA_sklearn.py`     | Implémentation complète Scikit-learn (parties A.1 à A.8) |
| `partieB_mllib.py`       | Implémentation complète Spark MLlib (parties B.1 à B.9)  |
| `partieC_comparaison.py` | Chargement des JSON et comparaison (partie C)            |

Les parties A et B sauvegardent chacune leurs métriques dans un fichier JSON (`sklearn_results.json` et `spark_results.json`). Le script de la partie C charge ces deux fichiers pour produire les tableaux et graphiques de comparaison.

## Contexte

La sécurité alimentaire mondiale dépend de la capacité à anticiper les rendements agricoles. Grâce aux données historiques (météo, intrants, superficie), il est possible de prédire le rendement en tonnes par hectare. Ce dataset couvre des dizaines de cultures et de pays sur plusieurs décennies.

**Objectifs :**

1. **Régression** : Prédire le rendement en tonnes/ha (`hg/ha_yield`)
2. **Classification** : Prédire si le rendement sera élevé ou faible (> médiane = `high_yield`, sinon `low_yield`)

## Description du dataset `crop_yield.csv`

| Colonne                         | Type   | Description                                                  |
| ------------------------------- | ------ | ------------------------------------------------------------ |
| `Area`                          | string | Pays ou région productrice                                   |
| `Item`                          | string | Type de culture (blé, maïs, riz, etc.)                       |
| `Year`                          | int    | Année de récolte                                             |
| `hg/ha_yield`                   | int    | **Cible régression** : Rendement en hectogrammes par hectare |
| `average_rain_fall_mm_per_year` | float  | Pluviométrie annuelle moyenne (mm)                           |
| `pesticides_tonnes`             | float  | Quantité de pesticides utilisés (tonnes)                     |
| `avg_temp`                      | float  | Température moyenne annuelle (°C)                            |

**Cible régression :** `hg/ha_yield`
**Cible classification :** `high_yield` (1 si `hg/ha_yield` > médiane, 0 sinon) — à créer lors du prétraitement

## Partie A — Implémentation Scikit-learn

### A.1 Chargement et exploration

Charger le fichier `crop_yield.csv` avec Pandas.

- Afficher les dimensions et les types de colonnes
- Identifier les valeurs manquantes (nombre et pourcentage par colonne)
- Afficher les statistiques descriptives (`describe()`)
- Afficher la distribution du rendement (`hg/ha_yield`) avec un histogramme
- Afficher le rendement moyen par type de culture (`Item`) — top 10
- Afficher le rendement moyen par pays (`Area`) — top 10

### A.2 Préparation des données

- **Créer la cible de classification :**

```python
median_yield = df["hg/ha_yield"].median()
df["high_yield"] = (df["hg/ha_yield"] > median_yield).astype(int)
print(f"Médiane du rendement : {median_yield:.0f} hg/ha")
print(df["high_yield"].value_counts())
```

- **Définir les features :**

- **Split train/test **

### A.3 Pipeline Scikit-learn — Régression

Construire un `Pipeline` avec `ColumnTransformer` :

**Transformer numérique :**

1. `SimpleImputer(strategy='median')`
2. `StandardScaler`

**Transformer catégoriel :**

1. `SimpleImputer(strategy='most_frequent')`
2. `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`

**Régresseur :** `RandomForestRegressor(n_estimators=100, random_state=42)`

### A.4 Pipeline Scikit-learn — Classification

Réutiliser le même `preprocessor` avec un `RandomForestClassifier` :

### A.5 Entraînement et mesure du temps

### A.6 Évaluation

**Régression :**

- MAE
- RMSE
- R²

**Classification :**

- Accuracy
- F1-score
- Matrice de confusion

### A.7 Feature Importances

Extraire et afficher les 10 features les plus importantes pour **chacun des deux modèles**

### A.8 Sauvegarde et export JSON

- Sauvegarder les deux pipelines avec `joblib.dump`
- Exporter les métriques dans un fichier `sklearn_results.json` au format suivant :

```json
{
  "regression": {
    "time": 0.0,
    "mae": 0.0,
    "rmse": 0.0,
    "r2": 0.0
  },
  "classification": {
    "time": 0.0,
    "accuracy": 0.0,
    "f1": 0.0
  }
}
```

---

## Partie B — Implémentation Spark MLlib

### B.1 SparkSession et chargement

### B.2 Analyse exploratoire Spark

### B.3 Création de la cible de classification

```python
median_yield_spark = df_spark.approxQuantile("hg/ha_yield", [0.5], 0.001)[0]
print(f"Médiane Spark : {median_yield_spark:.0f} hg/ha")

df_spark = df_spark.withColumn(
    "high_yield",
    F.when(F.col("hg/ha_yield") > median_yield_spark, 1).otherwise(0)
)

df_spark.groupBy("high_yield").count().show()
```

### B.4 Pipeline MLlib — Régression

### B.5 Pipeline MLlib — Classification

Réutiliser les mêmes étapes de prétraitement, changer uniquement le modèle final

### B.6 Split et entraînement avec mesure du temps

### B.7 Évaluation

**Régression :**

- MAE
- RMSE
- R²

**Classification :**

- Accuracy
- F1-score
- Matrice de confusion

### B.8 Feature Importances Spark

### B.9 Sauvegarde et export JSON

- Sauvegarder les deux modèles MLlib avec `.write().overwrite().save()`
- Exporter les métriques dans un fichier `spark_results.json` avec la même structure que `sklearn_results.json` (voir A.8)

---

## Partie C — Comparaison et Analyse

> **Ce script est indépendant des parties A et B.** Il charge uniquement `sklearn_results.json` et `spark_results.json` pour produire les tableaux et graphiques de comparaison.

### C.0 Chargement des résultats JSON

### C.1 Tableau comparatif — Régression

Construire un `DataFrame` Pandas à partir des deux dictionnaires chargés et l'afficher :

| Aspect               | Scikit-learn | Spark MLlib |
| -------------------- | ------------ | ----------- |
| Temps d'entraînement | ? s          | ? s         |
| MAE                  | ? hg/ha      | ? hg/ha     |
| RMSE                 | ? hg/ha      | ? hg/ha     |
| R²                   | ?            | ?           |

### C.2 Tableau comparatif — Classification

Faire de même pour la classification (Accuracy, F1-score, temps).

### C.3 Visualisation comparative

Produire un graphique à barres groupées comparant les métriques clés des deux frameworks (MAE, RMSE, R², Accuracy, F1)

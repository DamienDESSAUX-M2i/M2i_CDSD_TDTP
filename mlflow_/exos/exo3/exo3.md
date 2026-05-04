# Exercice

**Dataset :** Heart Disease (UCI Cleveland)  
**Objectif :** Prédire la présence ou absence de maladie cardiaque à partir de données cliniques, avec un `SVC` (Support Vector Classifier) optimisé via `GridSearchCV`, et tracer l'analyse exploratoire dans MLflow.

## Contexte

Le dataset **Heart Disease** de l'UCI est un classique en machine learning médical. Il contient 303 patients et 13 variables cliniques (âge, pression artérielle, cholestérol, fréquence cardiaque max, etc.) collectées à la Cleveland Clinic. La variable cible indique si le patient a une maladie cardiaque (1) ou non (0).

## Partie 1 — Setup et chargement des données

### Chargement et nommage des colonnes

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.sklearn
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, auc, RocCurveDisplay
)

url = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
)
columns = [
    "age", "sex", "cp", "trestbps", "chol",
    "fbs", "restecg", "thalach", "exang",
    "oldpeak", "slope", "ca", "thal", "target"
]
df = pd.read_csv(url, names=columns, na_values="?")

# Cible binaire : 0 = pas de maladie, 1 = maladie
df["target"] = (df["target"] > 0).astype(int)

print(df.shape)
print(df.isnull().sum())
print(df["target"].value_counts())
```

## Partie 2 — Nettoyage des données

```python
# 2.1 Suppression des lignes avec valeurs manquantes (6 lignes concernées)

# 2.2 Séparation features / cible

```

## Partie 3 — Analyse exploratoire loggée dans MLflow

```python
mlflow.set_experiment("heart_disease_eda")

with mlflow.start_run(run_name="EDA"):

    # --- Figure 1 : Distribution de la cible ---

    # --- Figure 2 : Distribution de l'âge par classe ---

    # --- Figure 3 : Heatmap des corrélations ---

```

## Partie 4 — Préparation du train/test split

## Partie 5 — GridSearchCV + logging MLflow

```python
# 5.1 Pipeline : StandardScaler → SVC

# 5.2 Grille — préfixe "svc__" pour cibler les params du SVC dans le pipeline


with mlflow.start_run(run_name="SVC_GridSearch"):

    # 5.3 Log des meilleurs hyperparamètres ---
    # On nettoie le préfixe "svc__" pour plus de lisibilité dans l'UI
    best_params_clean = {
        k.replace("svc__", ""): v for k, v in gs.best_params_.items()
    }

    # 5.4 Évaluation sur le test set

    # 5.5 Calcul de l'AUC-ROC

    # --- Figure 1 : Matrice de confusion ---

    # --- Figure 2 : Courbe ROC ---

    # 5.6 Log du modèle
```

## Partie 6 — Exploration de l'UI MLflow

Bonne pratique : pour des données médicales, surveille le recall sur la classe "Malade" : un faux négatif (malade prédit sain) est bien plus coûteux qu'un faux positif. Envisage d'optimiser `scoring="recall"` plutôt que `"accuracy"` dans le `GridSearchCV`.

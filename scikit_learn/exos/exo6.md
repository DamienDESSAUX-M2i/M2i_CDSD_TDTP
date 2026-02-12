## Prédiction des notes d'étudiants

## Dataset

**Variables disponibles :**

| Variable           | Description                                       | Type         |
| ------------------ | ------------------------------------------------- | ------------ |
| `age`              | Âge de l'élève (15-22 ans)                        | Numérique    |
| `study_time`       | Temps d'étude hebdomadaire (1-4)                  | Numérique    |
| `failures`         | Nombre d'échecs scolaires passés (0-4)            | Numérique    |
| `absences`         | Nombre d'absences (0-93)                          | Numérique    |
| `parental_support` | Soutien parental (none/low/medium/high/very high) | Catégorielle |
| `extracurricular`  | Activités extra-scolaires (yes/no)                | Catégorielle |
| `internet`         | Accès internet à la maison (yes/no)               | Catégorielle |
| `health`           | État de santé (1-5)                               | Numérique    |
| `freetime`         | Temps libre après l'école (1-5)                   | Numérique    |
| `goout`            | Sorties avec des amis (1-5)                       | Numérique    |
| **`passed`**       | **Variable cible : a réussi (1) ou échoué (0)**   | **Binaire**  |

---

## Partie 1 - Préparation des données

### Étape 1.1 : Chargement et exploration

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

np.random.seed(42)
n = 500

df = pd.DataFrame({
    'age':              np.random.randint(15, 23, n),
    'study_time':       np.random.randint(1, 5, n),
    'failures':         np.random.choice([0, 1, 2, 3], n, p=[0.6, 0.25, 0.1, 0.05]),
    'absences':         np.random.randint(0, 40, n),
    'parental_support': np.random.choice(['none','low','medium','high','very high'], n),
    'extracurricular':  np.random.choice(['yes', 'no'], n),
    'internet':         np.random.choice(['yes', 'no'], n, p=[0.7, 0.3]),
    'health':           np.random.randint(1, 6, n),
    'freetime':         np.random.randint(1, 6, n),
    'goout':            np.random.randint(1, 6, n),
})

df['passed'] = (
    (df['study_time'] >= 3) * 0.4 +
    (df['failures'] == 0) * 0.3 +
    (df['absences'] < 10) * 0.2 +
    (df['parental_support'].isin(['high', 'very high'])) * 0.1 +
    np.random.uniform(0, 0.3, n)
) > 0.5
df['passed'] = df['passed'].astype(int)

print(df.head())
print(f"\nDimensions : {df.shape}")
print(f"Taux de réussite : {df['passed'].mean():.1%}")
```

### Étape 1.2 : Prétraitement

```python
# Séparation features / target

# TODO : Identifiez les colonnes numériques et catégorielles

# TODO : Créez un pipeline de prétraitement

# TODO : Séparez en train/test
```

## Partie 2 - Entraînement du modèle

### Étape 2.1 : Random Forest

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# TODO : Créez un pipeline complet (preprocessor + RandomForestClassifier)

# TODO : Entraînez le modèle et évaluez-le sur le test set
```

---

## Partie 3 - Feature Importance

### Étape 3.1 : Extraction des importances

```python
# Récupération des noms de toutes les features après transformation
rf_clf = rf_pipeline.named_steps['classifier']
preprocessor_fitted = rf_pipeline.named_steps['preprocessor']

ohe = preprocessor_fitted.named_transformers_['cat'].named_steps['onehot']
cat_feature_names = ohe.get_feature_names_out(categorical_features).tolist()
all_feature_names = numeric_features + cat_feature_names

# TODO : Récupérez les importances et affichez-les triées par ordre décroissant
```

### Étape 3.2 : Visualisation des importances

```python
# TODO : Reproduisez un graphique en barres horizontales
```

---

### Étape 3.3 : Comparaison Decision Tree vs Random Forest

```python
from sklearn.tree import DecisionTreeClassifier

# TODO : Entraînez un Decision Tree avec le même preprocesseur

# TODO : Récupérez ses importances

# TODO : Affichez les deux bar charts côte à côte (1 ligne, 2 colonnes)
# pour comparer DT vs RF
```

## Partie 4 - Analyse SHAP

### Étape 4.1 : Calcul des valeurs SHAP

```python
import shap

# TODO : Transformez les données avec le preprocesseur

# TODO : Entraînez un Random Forest sans Pipeline sur les données transformées

# TODO : Créez un TreeExplainer et calculez les valeurs SHAP

# Gestion de la compatibilité SHAP
if shap_values_raw.ndim == 3:
    shap_values = [shap_values_raw[:, :, i] for i in range(shap_values_raw.shape[2])]
else:
    shap_values = shap_values_raw

print(f"Shape des valeurs SHAP (classe 1) : {shap_values[1].shape}")
```

---

### Étape 4.2 : Summary Plot (vue globale)

```python
# TODO : Affichez le summary plot SHAP pour la classe 1 (élève qui réussit)
```

### Étape 4.3 : Explication locale (Waterfall Plot)

```python
# TODO : Choisissez un élève du test set (par exemple sample_idx = 5)
# Affichez ses caractéristiques

# TODO : Créez et affichez le waterfall plot pour cet élève
```

### Étape 4.4 (Bonus) : Comparer deux élèves

```python
# TODO : Choisissez un élève ayant réussi et un ayant échoué
# Affichez leurs waterfall plots côte à côte
# Comparez les contributions de chaque feature pour les deux profils
```

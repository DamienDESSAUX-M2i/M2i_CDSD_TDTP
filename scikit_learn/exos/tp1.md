# TP Jour 1 : Pipeline Complet de Pretraitement

## Objectif

Construire un pipeline de pretraitement complet pour un dataset realiste de prediction de salaire.

## Competences mises en oeuvre

- Exploration et analyse des donnees
- Gestion des valeurs manquantes
- Encodage des variables categorielles
- Normalisation des donnees
- Construction de pipelines Scikit-learn
- Utilisation de ColumnTransformer

## Partie 1 : Chargement et exploration du dataset

### Dataset

Vous travaillez sur un dataset inspire du Census Income pour predire si une personne gagne plus de 50K euros/an.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

%matplotlib inline
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(42)

# Generation du dataset
n = 1000

education_levels = ['Sans diplome', 'Brevet', 'Bac', 'BTS/DUT', 'Licence', 'Master', 'Doctorat']
occupations = ['Administratif', 'Commercial', 'Technique', 'Cadre', 'Direction', 'Artisan', 'Ouvrier']
sectors = ['Public', 'Prive', 'Independant']
marital_status = ['Celibataire', 'Marie(e)', 'Divorce(e)', 'Veuf(ve)']
regions = ['Ile-de-France', 'PACA', 'Auvergne-Rhone-Alpes', 'Nouvelle-Aquitaine', 'Autres']

df = pd.DataFrame({
    'age': np.random.randint(18, 70, n),
    'education': np.random.choice(education_levels, n, p=[0.05, 0.10, 0.20, 0.20, 0.20, 0.20, 0.05]),
    'occupation': np.random.choice(occupations, n),
    'secteur': np.random.choice(sectors, n, p=[0.25, 0.60, 0.15]),
    'heures_semaine': np.random.randint(20, 60, n),
    'experience': np.random.randint(0, 45, n),
    'situation_familiale': np.random.choice(marital_status, n, p=[0.30, 0.50, 0.15, 0.05]),
    'nb_enfants': np.random.choice([0, 1, 2, 3, 4], n, p=[0.25, 0.25, 0.30, 0.15, 0.05]),
    'region': np.random.choice(regions, n, p=[0.25, 0.15, 0.15, 0.10, 0.35]),
    'teletravail': np.random.choice(['Jamais', 'Partiel', 'Complet'], n, p=[0.50, 0.35, 0.15]),
    'anciennete_poste': np.random.randint(0, 30, n),
    'satisfaction': np.random.uniform(1, 10, n).round(1)
})

# Variable cible basee sur des criteres realistes
education_score = df['education'].map({
    'Sans diplome': 0, 'Brevet': 1, 'Bac': 2, 'BTS/DUT': 3,
    'Licence': 4, 'Master': 5, 'Doctorat': 6
})

occupation_score = df['occupation'].map({
    'Ouvrier': 0, 'Artisan': 1, 'Administratif': 2, 'Technique': 3,
    'Commercial': 4, 'Cadre': 5, 'Direction': 6
})

salaire_score = (
    df['age'] * 0.02 +
    education_score * 0.8 +
    occupation_score * 0.6 +
    df['experience'] * 0.05 +
    df['heures_semaine'] * 0.03 +
    (df['secteur'] == 'Prive').astype(int) * 0.5 +
    (df['region'] == 'Ile-de-France').astype(int) * 0.8 +
    np.random.normal(0, 1, n)
)

df['salaire_50k'] = (salaire_score > np.percentile(salaire_score, 75)).astype(int)

# Valeurs manquantes
missing_cols = {
    'experience': 40,
    'heures_semaine': 25,
    'satisfaction': 50,
    'teletravail': 30,
    'nb_enfants': 20
}

for col, n_missing in missing_cols.items():
    df.loc[np.random.choice(n, n_missing, replace=False), col] = np.nan
```

### Tache 1.1 : Exploration initiale

1. Quelles sont les dimensions du dataset ?
2. Quels sont les types de chaque colonne ?
3. Combien de valeurs manquantes par colonne ?
4. Quelle est la distribution de la variable cible ?

### Tache 1.2 : Identifier les types de variables

Classifiez les variables en :

- **Numeriques** : variables continues ou discretes
- **Categorielles nominales** : sans ordre naturel
- **Categorielles ordinales** : avec un ordre logique

```python
numeric_features = []
nominal_features = []
ordinal_features = []
```

### Tache 1.3 : Visualisations exploratoires

Creez des visualisations pertinentes :

1. Distribution de l'age selon le salaire (>50k ou non)
2. Relation entre education et salaire
3. Heatmap des correlations numeriques

## Partie 2 : Preparation des donnees

### Tache 2.1 : Separation Train/Test

Separez les donnees en :

- Features (X) et target (y)
- Train (80%) et Test (20%)
- Utilisez `stratify=y` pour conserver la distribution de la cible

## Partie 3 : Construction du Pipeline

### Tache 3.1 : Pipeline pour variables numeriques

Creez un pipeline qui :

1. Impute les valeurs manquantes avec la mediane
2. Standardise les donnees

### Tache 3.2 : Pipeline pour variables nominales

Creez un pipeline qui :

1. Impute les valeurs manquantes avec le mode
2. Applique One-Hot Encoding

### Tache 3.3 : Pipeline pour variables ordinales

Creez un pipeline qui :

1. Impute les valeurs manquantes avec le mode
2. Applique Ordinal Encoding avec l'ordre correct

**Ordres a respecter :**

- `education` : Sans diplome < Brevet < Bac < BTS/DUT < Licence < Master < Doctorat
- `teletravail` : Jamais < Partiel < Complet

### Tache 3.4 : ColumnTransformer

Combinez les trois transformateurs dans un `ColumnTransformer`.

### Tache 3.5 : Pipeline complet avec modele

Creez le pipeline final avec :

1. Le preprocessor
2. Un classificateur (LogisticRegression)

## Partie 4 : Entrainement et Evaluation

### Tache 4.1 : Entrainement

Entrainez le pipeline sur les donnees d'entrainement.

### Tache 4.2 : Evaluation sur le test

1. Calculez l'accuracy sur le test

## Partie 5 : Sauvegarde et utilisation

### Tache 5.1 : Sauvegarder le pipeline

### Tache 5.2 : Faire une prediction sur de nouvelles donnees

Creez un nouvel individu et predisez s'il gagne plus de 50K

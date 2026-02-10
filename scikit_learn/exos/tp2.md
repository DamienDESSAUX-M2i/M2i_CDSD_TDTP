# TP : Prediction de Prix Immobiliers

## Contexte

Vous etes data scientist dans une agence immobiliere qui souhaite automatiser l'estimation des prix de vente des maisons. Un modele precis permettra d'aider les agents a proposer des prix competitifs et les acheteurs a evaluer la valeur des biens.

## Dataset

Vous utiliserez le dataset **California Housing**

```python
from sklearn.datasets import fetch_california_housing
import pandas as pd

# Chargement
housing = fetch_california_housing(as_frame=True)
df = housing.frame

print(f"Nombre d'observations : {df.shape[0]}")
print(f"Nombre de features : {df.shape[1] - 1}")
```

**Variables :**
| Variable | Description |
|----------|-------------|
| MedInc | Revenu median du bloc (en dizaines de milliers $) |
| HouseAge | Age median des maisons du bloc |
| AveRooms | Nombre moyen de pieces par menage |
| AveBedrms | Nombre moyen de chambres par menage |
| Population | Population du bloc |
| AveOccup | Nombre moyen d'occupants par menage |
| Latitude | Latitude du bloc |
| Longitude | Longitude du bloc |
| MedHouseVal | **Cible** : Valeur mediane des maisons (en centaines de milliers $) |

## Partie 1 : Exploration des Donnees

### 1.1 Chargement et apercu

- Identifiez les types de variables (numeriques, categorielles)
- Verifiez les valeurs manquantes
- Detectez les valeurs aberrantes

### 1.2 Analyse de la variable cible

1. La distribution est-elle normale ?
2. Y a-t-il des valeurs plafonnees ou aberrantes ?

### 1.3 Analyse des correlations

1. Quelles features sont les plus correlees avec le prix ?

### 1.4 Analyse spatiale (California Housing)

- Les zones cotieres sont-elles plus cheres ?

## Partie 2 : Preprocessing avec Pipeline

### 2.1 Strategie de preprocessing

Definissez une strategie pour chaque type de variable 

### 2.2 Creation des transformers

### 2.3 Feature Engineering (Bonus)

Creez des features supplementaires qui pourraient ameliorer le modele :

1. Implementez au moins 3 nouvelles features
2. Justifiez leur pertinence pour la prediction de prix

### 2.3 Évaluation du modèle

- R-squared (coefficient de determination)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)

### 3.0 Sauvegarde du modele

### 5.3 Fonction de prediction

- Créez une fonction qui prend en paramètre une maison et prédit le prix.

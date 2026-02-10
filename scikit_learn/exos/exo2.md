# Exercice 1 : Regression Lineaire - Prediction de Consommation de Carburant

## Contexte

Vous travaillez pour un constructeur automobile qui souhaite predire la consommation de carburant de ses vehicules en fonction de leurs caracteristiques techniques. Cette prediction permettra d'optimiser la conception des futurs modeles et d'informer les clients sur les performances attendues.

## Dataset

Vous utiliserez le dataset **Auto MPG** disponible dans scikit-learn ou telechargeable depuis UCI ML Repository.

```python
import pandas as pd
from sklearn.datasets import fetch_openml

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
columns = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight',
           'acceleration', 'model_year', 'origin', 'car_name']
df = pd.read_csv(url, sep='\s+', names=columns, na_values='?')
```

### Description des variables

| Variable     | Description                                          | Type         |
| ------------ | ---------------------------------------------------- | ------------ |
| mpg          | Miles par gallon (consommation) - **Variable cible** | Continue     |
| cylinders    | Nombre de cylindres                                  | Discrete     |
| displacement | Cylindree (cu. inches)                               | Continue     |
| horsepower   | Puissance (chevaux)                                  | Continue     |
| weight       | Poids du vehicule (lbs)                              | Continue     |
| acceleration | Temps pour atteindre 60 mph (secondes)               | Continue     |
| model_year   | Annee du modele (70-82)                              | Discrete     |
| origin       | Origine (1=USA, 2=Europe, 3=Japon)                   | Categorielle |

---

## Partie 1 : Exploration des Donnees

### Question 1.1

Chargez le dataset et affichez ses informations de base :

- Nombre d'observations et de variables
- Types de donnees
- Presence de valeurs manquantes
- Statistiques descriptives

### Question 1.2

Gerez les valeurs manquantes :

- Identifiez les colonnes avec des valeurs manquantes
- Choisissez une strategie appropriee (suppression ou imputation)
- Justifiez votre choix

### Question 1.3

Analysez la distribution de la variable cible (mpg) :

- Tracez un histogramme
- Calculez les statistiques de centralite et dispersion
- La distribution est-elle normale ? Faut-il la transformer ?

### Question 1.4

Explorez les correlations :

- Creez une matrice de correlation
- Identifiez les variables les plus correlees avec mpg
- Y a-t-il des problemes de multicolinearite entre les features ?

## Partie 2 : Preprocessing

### Question 2.1

Preparez les features pour la modelisation :

- Separez la variable cible des features
- Traitez la variable categorielle `origin` (encodage)

### Question 2.2

Divisez les donnees en ensembles d'entrainement et de test :

- Utilisez 80% pour l'entrainement
- Fixez random_state=42 pour la reproductibilite

### Question 2.3

Standardisez les features numeriques :

- Appliquez StandardScaler sur les donnees d'entrainement
- Transformez les donnees de test avec le meme scaler

## Partie 3 : Entrainement du Modele

### Question 3.1

Entrainez un modele de regression lineaire simple

Evaluez le modele avec :

- R-squared (coefficient de determination)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)

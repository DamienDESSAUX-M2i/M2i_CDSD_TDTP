# Exercice 2 : Conteneurisation d'un modèle ML

## Objectif

Créer un conteneur Docker pour entraîner un modèle de classification et sauvegarder le résultat.

## Contexte

Vous travaillez sur un projet de prédiction de la qualité du vin. Vous devez conteneuriser le processus d'entraînement pour que n'importe qui puisse reproduire vos résultats.

## Données

Utilisez le dataset de qualité du vin (synthétique pour l'exercice).

**Créer `wine_data.csv`** :

```csv
fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,quality
7.4,0.7,0.0,1.9,0.076,11,34,0.9978,3.51,0.56,9.4,5
7.8,0.88,0.0,2.6,0.098,25,67,0.9968,3.2,0.68,9.8,5
7.8,0.76,0.04,2.3,0.092,15,54,0.997,3.26,0.65,9.8,5
11.2,0.28,0.56,1.9,0.075,17,60,0.998,3.16,0.58,9.8,6
7.4,0.7,0.0,1.9,0.076,11,34,0.9978,3.51,0.56,9.4,5
7.9,0.6,0.06,1.6,0.069,15,59,0.9964,3.3,0.46,9.4,5
8.9,0.62,0.18,3.8,0.176,52,145,0.9988,3.16,0.88,9.2,5
7.6,0.39,0.31,2.3,0.082,23,71,0.9982,3.52,0.65,9.7,5
8.5,0.28,0.56,1.8,0.092,35,103,0.9969,3.3,0.75,10.5,7
8.1,0.56,0.28,1.7,0.368,16,56,0.9968,3.11,1.28,9.3,5
7.4,0.59,0.08,4.4,0.086,6,29,0.9974,3.38,0.5,9.0,4
7.9,0.32,0.51,1.8,0.341,17,56,0.9969,3.04,1.08,9.2,6
8.9,0.22,0.48,1.8,0.077,29,60,0.9969,3.39,0.53,9.4,6
7.6,0.39,0.31,2.3,0.082,23,71,0.9982,3.52,0.65,9.7,5
7.9,0.43,0.21,1.6,0.106,10,37,0.9966,3.17,0.91,9.5,5
8.5,0.49,0.11,2.3,0.084,9,67,0.9968,3.17,0.53,9.4,5
6.9,0.4,0.14,2.4,0.085,21,40,0.9968,3.43,0.63,9.7,6
6.3,0.39,0.16,1.4,0.08,11,23,0.9955,3.34,0.56,9.3,5
7.6,0.41,0.24,1.8,0.08,4,11,0.9962,3.28,0.59,9.5,5
7.9,0.43,0.21,1.6,0.106,10,37,0.9966,3.17,0.91,9.5,5
```

---

## Tâches à réaliser

### Partie 1 : Créer le script d'entraînement

Créez un fichier `train_model.py` qui :

1. Charge les données depuis `wine_data.csv`
2. Sépare les features (X) et la target (y = quality)
3. Divise en train/test (80/20)
4. Entraîne un modèle RandomForest
5. Affiche les métriques (accuracy, classification report)
6. Sauvegarde le modèle dans `model.pkl`

### Partie 2 : Créer le Dockerfile

Créez un `Dockerfile` qui :

1. Part de `python:3.9-slim`
2. Installe les dépendances
3. Crée un dossier `/app/models` pour sauvegarder le modèle
4. Copie les fichiers nécessaires
5. Exécute le script d'entraînement

### Partie 3 : Structure du projet

Organisez votre projet comme ceci :

```
exercice2/
├── Dockerfile
├── requirements.txt
├── wine_data.csv
├── train_model.py
└── models/
```

---

### Partie 4 : Build et Run

- Construire l'image
- Exécuter l'entraînement
 
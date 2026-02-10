# TP : Classification Multi-classes de Chiffres Manuscrits

## Contexte

Vous travaillez sur un projet de reconnaissance automatique de chiffres manuscrits. L'objectif est de creer un systeme capable de classifier des images de chiffres (0-9) a partir de leurs caracteristiques pixeliques.

Ce type de probleme est a la base de nombreuses applications :

- Lecture automatique de cheques bancaires
- Tri postal automatique
- Reconnaissance de formulaires

## Dataset

Vous utiliserez le dataset **Digits** de scikit-learn :

```python
from sklearn.datasets import load_digits
digits = load_digits()
X, y = digits.data, digits.target
```

Ce dataset contient :

- 1797 images de chiffres (0-9)
- Chaque image fait 8x8 pixels = 64 features
- Valeurs des pixels entre 0 et 16

## Partie 1 : Exploration et Preparation des Donnees

### 1.1 Chargement et exploration

- Chargez le dataset et affichez ses caracteristiques principales
- Combien y a-t-il d'echantillons par classe ?
- Les classes sont-elles equilibrees ?

### 1.2 Visualisation des images

- Affichez une grille de 25 images (5x5) avec leurs labels
- Utilisez `plt.imshow()` avec `cmap='gray'`
- Les images `digits.images` sont de dimension 8x8

```python
# Exemple pour afficher une image
plt.imshow(digits.images[0], cmap='gray')
plt.title(f"Label: {digits.target[0]}")
```

### 1.3 Preparation

- Divisez les donnees en train (80%) et test (20%)
- Utilisez `stratify=y` pour conserver la distribution des classes
- Normalisez les donnees avec `StandardScaler`

## Partie 2 : Classification avec KNN

### 2.1 Premier modele

- Entrainez un KNN avec K=5, n_jobs=-1, algorithm='kd_tree'
- Evaluez avec accuracy et rapport de classification

### 2.2 Optimisation de K

- Testez K de 1 a 20
- Tracez la courbe du score en fonction de K
- Quel est le K optimal ?

### 2.3 Analyse des erreurs

- Creez la matrice de confusion
- Visualisez-la avec `seaborn.heatmap()`

## Partie 3 : Classification avec Arbres de Decision

### 3.1 Arbre de base

- Entrainez un arbre sans contrainte
- Comparez accuracy train et test

### 3.2 Comparaison avec KNN

- Quelle methode est meilleure sur ce probleme ?
- Quels sont les avantages et inconvenients de chaque approche ?

## Partie 4 : Methodes d'Ensemble

### 4.1 Random Forest

- Entrainez un Random Forest avec 100 arbres
- Comparez avec l'arbre simple et KNN

### 4.2 Gradient Boosting

- Entrainez un GradientBoostingClassifier
- Attention : peut etre lent sur ce dataset
- Comparez avec Random Forest

### 4.4 Voting Classifier

- Combinez vos 3 meilleurs modeles dans un VotingClassifier
- Testez `voting='hard'` et `voting='soft'`
- Le voting bat-il les modeles individuels ?

## Partie 5 : Pipeline Final

### 5.1 Meilleur modele

- Choisissez le meilleur algorithme base sur vos experimentations

### 5.2 Pipeline complet

- Creez un pipeline incluant :
  - Le preprocessing (StandardScaler si necessaire)
  - Le modele optimise
- Evaluez le pipeline final sur le jeu de test

### 5.4 Rapport de performance

Creez un tableau recapitulatif :

| Modele                  | Accuracy | Temps (s) | Meilleur pour |
| ----------------------- | -------- | --------- | ------------- |
| KNN (K=?)               |          |           |               |
| Decision Tree (depth=?) |          |           |               |
| Random Forest (n=?)     |          |           |               |
| Gradient Boosting       |          |           |               |
| Voting                  |          |           |               |

### 5.6 Modele sauvegarde

- Sauvegardez votre meilleur modele avec `joblib`
- Incluez le code pour charger et utiliser le modele

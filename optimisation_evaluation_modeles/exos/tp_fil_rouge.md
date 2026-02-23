# TP Fil Rouge

## Partie 1 — Fondamentaux de l'évaluation des modèles

## Contexte

Vous travaillez pour une entreprise de e-commerce britannique. Vous disposez d'un dataset de **~500 000 transactions** issues d'une plateforme de vente en ligne entre 2010 et 2011.

**Dataset** : [E-Commerce Data — UK Retail (Kaggle)](https://www.kaggle.com/datasets/carrie1/ecommerce-data)

L'objectif final de ce fil rouge est de construire un modèle capable de **prédire si un client est à risque de churn**, en partant des données brutes jusqu'à un pipeline ML production-ready.

## Split Train/Test

### Chargement des données

1. Chargez le fichier `data.csv` avec pandas et affichez les premières lignes.
2. Vérifiez les types de colonnes, les valeurs manquantes et les doublons.
3. Créez une colonne `churn` binaire : `1` si le client n'a pas commandé depuis plus de 90 jours, `0` sinon. Affichez la distribution de cette variable cible.

### Split des données

4. Séparez les features `X` et la cible `y`.
5. Réalisez un **split simple** (80% train / 20% test) et affichez les proportions de chaque classe dans le train et le test.
6. Réalisez un **split stratifié** et comparez les proportions obtenues avec le split simple.
7. Visualisez la distribution des classes dans les deux cas sous forme d'histogrammes côte à côte.

## Pipeline sklearn et prévention du Data Leakage

### Construction de la pipeline

Le dataset UK Retail contient des colonnes numériques et catégorielles avec des valeurs manquantes. Vous devez construire une pipeline complète qui prend en charge tout le preprocessing.

1. Identifiez les colonnes numériques et catégorielles pertinentes pour la prédiction.
2. Construisez un `ColumnTransformer` avec :
   - Pour les colonnes **numériques** : imputation par la médiane + standardisation
   - Pour les colonnes **catégorielles** : imputation par la valeur la plus fréquente + encodage one-hot
3. Intégrez ce preprocessor dans une `Pipeline` complète avec un premier modèle de votre choix.

## Cross-Validation

### Mise en place

1. Instanciez **plusieurs modèles de classification**.
2. Appliquez une **KFold** (5 splits) et une **StratifiedKFold** (5 splits) sur les données.
3. Calculez l'accuracy moyenne et l'écart-type pour chaque méthode.
4. Comparez les résultats et visualisez les scores par fold sous forme de barres groupées.
5. Utilisez `cross_validate` avec la StratifiedKFold pour récupérer simultanément l'accuracy, le F1-score macro, la précision et le rappel, sur le train **et** le test.
6. Affichez les résultats et identifiez si les modèles présentent des signes de surapprentissage.
7. Comparez les performances de chaque modèle dans un tableau de synthèse et identifiez le meilleur candidat.

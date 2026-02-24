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

## Partie 2 — Optimisation des hyperparamètres

## Contexte

Vous avez identifié le meilleur modèle candidat lors de la phase d'évaluation. Il est maintenant temps d'en tirer le maximum en optimisant ses hyperparamètres de manière systématique. Vous comparerez deux approches : la recherche exhaustive par grille (**GridSearchCV**) et la recherche aléatoire (**RandomizedSearchCV**).

## RandomizedSearchCV

### Mise en place

1. Reprenez la pipeline complète (preprocessor + modèle) identifiée à la partie précédente.
2. Définissez un espace de recherche large pour les hyperparamètres du modèle.

3. Instanciez un `RandomizedSearchCV` avec :
   - `n_iter=20` (nombre de combinaisons testées)
   - une `StratifiedKFold` à 5 folds comme stratégie de validation
   - le F1-score macro comme métrique de scoring
   - `random_state=42` pour la reproductibilité
4. Entraînez la recherche sur le jeu d'entraînement et mesurez le temps d'exécution avec `time.time()`.

### Analyse des résultats

5. Affichez les meilleurs hyperparamètres trouvés et le meilleur score de validation croisée associé.
6. Récupérez le `cv_results_` et visualisez la distribution des scores F1 obtenus selon les différentes combinaisons testées (histogramme ou scatter plot `mean_test_score` vs rang).
7. Évaluez le meilleur modèle sur le jeu de test et affichez le classification report complet.

## GridSearchCV

### Mise en place

1. À partir des meilleurs hyperparamètres trouvés par RandomizedSearch, **affinez l'espace de recherche** en définissant une grille restreinte autour de ces valeurs.

2. Instanciez un `GridSearchCV` avec la même `StratifiedKFold` à 5 folds et le même scoring F1 macro.
3. Entraînez la recherche sur le jeu d'entraînement et mesurez le temps d'exécution.

### Analyse des résultats

4. Affichez les meilleurs hyperparamètres trouvés et le meilleur score de validation croisée associé.
5. Évaluez le meilleur modèle sur le jeu de test et affichez le classification report complet.

## Comparaison RandomSearch vs GridSearch

### Tableau de synthèse

7. Construisez un tableau comparatif récapitulant pour chaque méthode : le meilleur score F1 en validation croisée, le score F1 sur le jeu de test, le nombre de combinaisons testées et le temps d'exécution.

| Méthode            | Meilleur F1 (CV) | F1 test | Combinaisons testées | Temps (s) |
| ------------------ | ---------------- | ------- | -------------------- | --------- |
| RandomizedSearchCV |                  |         |                      |           |
| GridSearchCV       |                  |         |                      |           |

### Visualisation

8. Tracez un graphique en barres côte à côte comparant le F1-score en validation croisée et sur le jeu de test pour les deux méthodes.
# Exercice : Comparaison de Modèles

## Objectif

Comparer plusieurs algorithmes ML avec MLflow et identifier le meilleur.

## Énoncé

Créez un script qui compare 4 algorithmes différents sur le même dataset :

- RandomForest
- GradientBoosting
- LogisticRegression
- SVM

Trouvez automatiquement le meilleur et générez un rapport.

## Critères de validation

- 4 runs créés (un par modèle)
- Chaque run a un nom explicite
- Métriques : accuracy, f1, precision, recall, training_time
- Tags : model_type, algorithm_family
- Le meilleur modèle est identifié automatiquement
- Rapport comparatif généré

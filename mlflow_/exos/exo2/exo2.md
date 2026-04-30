# Exercice  : Tracking d'un Modèle Simple

## Objectif

Implémenter le tracking MLflow pour un projet de classification complet.

## Énoncé

Vous devez créer un projet de classification de la qualité du vin avec tracking MLflow complet :

- Paramètres
- Métriques multiples
- Sauvegarde du modèle
- Visualisations

## Niveau 1 : Basique

### Tâche : Tracking simple

Créez un script `train_wine_quality.py` qui :

1. Charge le dataset Wine Quality (scikit-learn)
2. Entraîne un RandomForestClassifier
3. Log les paramètres suivants :
   - n_estimators
   - max_depth
   - random_state
   - test_size
4. Log les métriques :
   - accuracy
   - f1_score
5. Sauvegarde le modèle avec MLflow

## Niveau 2 : Intermédiaire

### Tâche : Métriques avancées et visualisations

Améliorez votre script pour ajouter :

1. **Métriques supplémentaires** :
   - precision
   - recall
   - Temps d'entraînement

2. **Matrice de confusion** :
   - Créer et sauvegarder comme artifact

3. **Feature importance** :
   - Graphique des features les plus importantes

4. **Tags** :
   - model_type
   - developer
   - dataset

## Niveau 3 : Avancé

### Tâche : Pipeline complet avec multiple runs

Créez un script qui :

1. **Teste plusieurs configurations** :
   - n_estimators: [50, 100, 150, 200]
   - max_depth: [3, 5, 7, 10]

2. **Pour chaque configuration** :
   - Logger tous les paramètres
   - Logger toutes les métriques
   - Sauvegarder les visualisations
   - Ajouter un nom de run explicite

3. **Analyse post-training** :
   - Utiliser MlflowClient pour trouver le meilleur run
   - Afficher les paramètres du meilleur modèle
   - Logger un fichier summary.txt avec les résultats

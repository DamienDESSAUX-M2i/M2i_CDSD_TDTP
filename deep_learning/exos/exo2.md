# Exercice 3 : Régression avec MLP

## Objectif
Implémenter un MLP pour la régression et maîtriser l'ajustement de modèles continus.

## Contexte
Prédiction de prix d'immobilier sur le dataset Boston Housing (ou alternative Kaggle).

## Tâches

### Tâche 1 : Chargement et Exploration
- Chargez le dataset de régression
- Explorez les features et la target
- Analysez les distributions, correlations
- Identifiez les outliers

### Tâche 2 : Préparation
- Normalisez les features (StandardScaler)
- Split train/val/test
- Gestion des valeurs manquantes si applicable

### Tâche 3 : Architecture MLP
- Construisez un MLP pour régression :
  - 3-4 couches hidden
  - Activation ReLU
  - Output : 1 unité, activation linéaire (pas sigmoid!)
- Loss : MSE ou MAE
- Optimizer : Adam

### Tâche 4 : Entraînement
- Entraînez 100 epochs
- Visualisez train/val loss
- Évaluez sur test set (MSE, RMSE, MAE, R²)

### Tâche 5 : Analyse des Prédictions
- Comparez prédictions vs vraies valeurs
- Visualisez residuals (prédiction - réel)
- Analysez l'erreur par plage de prix
- Identifiez les prédictions les plus mauvaises

### Tâche 6 : Amélioration
- Testez différentes architectures
- Ajoutez régularisation (L2, dropout)
- Tuning learning rate
- Mesurez l'amélioration quantitativement

## Critères d'évaluation

- Données préparées correctement
- Architecture MLP appropriée (output linéaire!)
- Métriques correctes (MSE, MAE, R²)
- Visualisations des residuals
- Tuning systématique

## Bonus

- Implémentez une loss function personnalisée
- Utilisez Huber loss pour robustesse
- Testez ensemble methods (moyenne de modèles)

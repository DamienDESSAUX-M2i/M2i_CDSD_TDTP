# TP Final : Classification de Sentiments Avancée

## Objectif Global
Construire un classifieur de sentiments end-to-end en utilisant des techniques ML avancées sur un corpus réaliste de critiques, intégrant toutes les étapes : prétraitement, feature engineering, ensembling et évaluation complète.

## Contexte
Vous êtes data scientist dans une startup de recommandation. Le projet : analyser des critiques cinématographiques pour automatiser la classification sentiment. Vous utiliserez des techniques ML avancées (ensemble learning, optimisation d'hyperparamètres, validation croisée) pour atteindre haute performance.

## Dataset
Utilisez un corpus de critiques :
- Minimum 500 critiques (ou IMDB dataset complet)
- Labels binaires : 1 (positif), 0 (négatif)
- Critiques textuelles brutes (à nettoyer)
- Distribution équilibrée si possible

## Livrables attendus

1. Notebook Jupyter complet avec code commenté
2. Rapport d'analyse (markdown) avec conclusions
3. Pickled models et scalers
4. Graphiques : confusion matrix, courbes ROC, feature importance
5. Réflexion : forces/faiblesses, améliorations futures

## Phase 1 : Exploration et Préparation

### 1.1 - Chargement et exploration des données
- Chargez un corpus de critiques
- Explorez la structure : nombre de données, label distribution
- Analysez la longueur des critiques
- Vérifiez l'équilibre des classes

### 1.2 - Nettoyage des données
- Appliquez le nettoyage de texte complet (exercice 1)
- Normalisez les longueurs
- Vérifiez qu'il n'y a pas de missing values
- Analysez la qualité des données

### 1.3 - Analyse exploratoire
- Statistiques par classe
- Mots les plus fréquents positifs vs négatifs
- Word clouds par sentiment
- Longueur moyenne par classe

## Phase 2 : Feature Engineering

### 2.1 - Vectorisation (rappel exercice 2)
- Appliquez TF-IDF Vectorizer
- Paramètres : max_features=5000, min_df=2
- Normalisez avec L2

### 2.2 - Features Word2Vec (rappel exercice 3)
- Entraînez Word2Vec sur le corpus
- Générez des embeddings de documents (moyenne)
- Approche alternative à TF-IDF

### 2.3 - Feature Selection
- Analysez l'importance des features
- Testez différentes dimensionnalités
- Utilisez SelectKBest si nécessaire

## Phase 3 : Modélisation Avancée

### 3.1 - Modèle 1 : Logistic Regression avec optimisation
- Tuning avec GridSearchCV
- Paramètres : C, penalty, solver
- Baseline pour comparaison

### 3.2 - Modèle 2 : SVM
- Kernel tuning : linear, rbf
- Paramètres : C, gamma
- Comparaison avec Logistic Regression

### 3.3 - Modèle 3 : Random Forest
- Tuning : n_estimators, max_depth, min_samples_split
- Feature importance
- Out-of-bag validation

### 3.4 - Modèle 4 : Ensemble Learning
- Voting Classifier (LR + SVM + RF)
- Stacking avec meta-learner
- Bagging/Boosting

## Phase 4 : Validation et Optimisation

### 4.1 - Validation Croisée
- K-Fold CV (k=5)
- Stratified CV pour données déséquilibrées
- Métriques : accuracy, F1, AUC

### 4.2 - Hyperparameter Tuning
- GridSearchCV ou RandomizedSearchCV
- Pipeline ML complet (scaling + model)
- Cross-validation intégrée

### 4.3 - Gestion du déséquilibre
- Class weights si applicable
- SMOTE pour augmentation synthétique
- Métriques adaptées (F1, AUC plutôt qu'accuracy)

### 4.4 - Sélection du meilleur modèle
- Comparez tous les modèles
- Entraînez sur train set
- Évaluez sur test set

## Phase 5 : Évaluation Complète

### 5.1 - Métriques globales
- Accuracy, Precision, Recall, F1 sur test set
- ROC-AUC score
- Matrice de confusion détaillée

### 5.2 - Analyse des erreurs
- Faux positifs et faux négatifs
- Analysez 10 critiques mal classifiées
- Identifiez les patterns d'erreur

### 5.3 - Visualisations
- Confusion matrix (heatmap)
- ROC curve avec AUC
- Feature importance
- Précision-Recall curve

### 5.4 - Robustesse
- Testez sur données réelles nouvelles
- Identifiez les cas limites
- Évaluez la généralisation

## Phase 6 : Déploiement

### 6.1 - Pipeline de prédiction
- Créez une fonction `predict_sentiment(texte)`
- Vectorisation automatique
- Gestion des cas edge

### 6.2 - Prédictions sur données nouvelles
- Testez sur 10 critiques (5 positives, 5 négatives)
- Affichez confiance et probabilités
- Analyse des prédictions

### 6.3 - Sérialisation
- Sauvegardez le modèle (pickle)
- Sauvegardez le vectorizer (pickle)
- Testez rechargement

## Phase 7 : Rapport et Conclusions

### 7.1 - Rapport d'analyse
- Résumé exécutif (2-3 paragraphes)
- Méthodologie et choix
- Résultats comparatifs
- Meilleur modèle et justification
- Analyse des erreurs
- Limitations et perspectives

### 7.2 - Conclusions
- Performance atteinte
- Modèle prêt pour production?
- Recommandations d'amélioration
- Insights pour le business

## Critères d'évaluation

### Code et Implémentation (40 points)
- Prétraitement robuste et complète
- Modélisation variée (4+ modèles)
- Tuning d'hyperparamètres systématique
- Sérialisation et chargement

### Expérimentation et Analyse (35 points)
- Comparaison quantifiée des modèles
- Métriques complètes et justifiées
- Visualisations claires
- Analyse d'erreurs détaillée

### Documentation et Réflexion (25 points)
- Code commenté
- Rapport complet et clair
- Justification des choix
- Honnêteté sur les limitations
- Propositions réalistes

## Conseils et Ressources

### Imports recommandés
```python
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
import pickle
```

### Bonnes pratiques
- Utilisez `random_state=42` partout pour reproductibilité
- Toujours utiliser Pipeline avec scaling
- Cross-validation avant évaluation finale
- Sauvegarder le vectorizer ET le modèle
- Documenter chaque décision

### Optimisations possibles
- Ensemble methods (Voting, Stacking, Bagging)
- SMOTE pour données déséquilibrées
- Feature selection avancée
- Hyperparameter tuning exhaustif
- Stratégie de validation appropriée

## Remise
- Un notebook Jupyter complet (.ipynb)
- Un rapport d'analyse (markdown ou PDF)
- Les modèles sauvegardés (pickle ou joblib)
- Le vectorizer sauvegardé
- Optionnel : code de déploiement API

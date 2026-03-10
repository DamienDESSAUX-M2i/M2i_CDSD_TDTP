# Exercice 4 : Analyse de Sentiments - Approche Classique

## Objectif
Construire un classifieur de sentiments en utilisant des techniques de vectorisation et des modèles ML classiques (Logistic Regression, SVM, Naive Bayes).

## Contexte
Vous travaillez pour une plateforme e-commerce. Vous devez analyser automatiquement les avis clients pour déterminer s'ils sont positifs ou négatifs. Cet exercice vous propose une approche classique utilisant ML standard avant d'explorer le deep learning dans le TP final.

## Données

### Corpus d'entraînement
Utilisez ce dataset équilibré d'avis clients :

```python
reviews = [
    "Excellent produit, très satisfait! Livraison rapide, je recommande!",
    "Pourquoi ce produit est-il si cher pour une si mauvaise qualité?",
    "Parfait! Exactement ce que j'attendais. Très bon rapport qualité-prix.",
    "Horrible expérience. Le produit est cassé à la réception.",
    "Magnifique! Dépassé mes attentes. Un incontournable.",
    "Décevant. Les photos du site ne correspondaient pas au produit réel.",
    "Super ! Très content de mon achat. Je rachèterai!",
    "Pire achat de ma vie. Service client inexistant.",
    "Bon produit pour le prix. Pas extraordinaire mais correct.",
    "Absolument terrible. Qualité déplorable et défaut de fabrication.",
    "Sympa ! Livré rapidement et bien emballé.",
    "Vraiment nul. Ça ne fonctionne pas du tout.",
    "Très bien! Produit conforme à la description.",
    "Complètement inutile, j'ai demandé le remboursement.",
    "Excellent service et produit de qualité!",
    "Déception totale. N'achetez pas ce produit."
]

labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1 = positif, 0 = négatif
```

## Tâches

### Tâche 1 : Préparation des données
1. Nettoyez les avis (utilisez l'exercice 1)
2. Vectorisez avec TF-IDF (utilisez l'exercice 2)
3. Divisez en ensemble d'entraînement et de test (80/20)
4. Vérifiez l'équilibre des classes dans train et test

**Attendus** : Données propres et vectorisées, split train/test validé

### Tâche 2 : Logistic Regression
1. Entraînez une Logistic Regression sur l'ensemble d'entraînement
2. Prédisez sur l'ensemble de test
3. Calculez les métriques :
   - Accuracy
   - Precision
   - Recall
   - F1-score
4. Affichez une matrice de confusion

**Attendus** : Modèle entraîné, métriques calculées, matrice de confusion

### Tâche 3 : Support Vector Machine (SVM)
1. Entraînez un SVM avec kernel 'linear'
2. Comparez les performances avec Logistic Regression
3. Testez différents kernels : 'rbf', 'poly'
4. Quel kernel donne les meilleures performances?

**Attendus** : SVM entraîné, comparaison kernels, recommandation

### Tâche 4 : Naive Bayes
1. Entraînez un Naive Bayes Multinomial
2. Comparez avec les modèles précédents
3. Analysez les probabilités de classe pour 3 avis de test
4. Avantages/inconvénients de Naive Bayes?

**Attendus** : Naive Bayes entraîné, analyse comparée, recommandation

### Tâche 5 : Feature importance et interprétabilité
1. Extractez les coefficients de Logistic Regression
2. Identifiez les 10 termes les plus positifs et les 10 plus négatifs
3. Visualisez-les (graphique en barres)
4. Analysez : ces termes ont-ils du sens?

**Attendus** : Feature importance visualisée, analyse critique

### Tâche 6 : Tuning et optimisation
1. Utilisez GridSearchCV pour optimiser les paramètres de SVM
2. Paramètres à tester : C=[0.1, 1, 10], kernel=['linear', 'rbf']
3. Affichez le meilleur modèle et ses paramètres
4. Comparez les performances avant/après tuning

**Attendus** : Modèle optimisé, comparaison avant/après, meilleurs paramètres

### Tâche 7 : Évaluation sur données réelles
1. Testez sur 5 nouveaux avis non vus (positifs et négatifs mélangés)
2. Affichez :
   - Le texte brut
   - La prédiction
   - La probabilité de confiance
3. Analysez les erreurs : pourquoi les faux positifs/négatifs?
4. Comment améliorer le modèle?

**Attendus** : Prédictions sur données nouvelles, analyse d'erreurs

## Critères d'évaluation

- Données correctement préparées et vectorisées
- Logistic Regression, SVM et Naive Bayes implémentés
- Métriques calculées correctement (accuracy, precision, recall, F1)
- Feature importance extraite et analysée
- Tuning de paramètres réalisé
- Prédictions sur données nouvelles avec analyse

## Conseils

- Importez : `from sklearn.linear_model import LogisticRegression`
- Importez : `from sklearn.svm import SVC`
- Importez : `from sklearn.naive_bayes import MultinomialNB`
- `train_test_split` de sklearn avec `random_state=42` pour la reproductibilité
- `classification_report` pour un résumé complet des métriques
- `GridSearchCV` pour l'optimisation automatique

## Bonus (Optionnel)

- Testez d'autres classifieurs : Random Forest, XGBoost
- Implémentez une validation croisée (K-Fold CV)
- Créez une ROC curve et AUC score
- Utilisez Word2Vec embeddings à la place de TF-IDF
- Appliquez du SMOTE pour gérer un déséquilibre de classes

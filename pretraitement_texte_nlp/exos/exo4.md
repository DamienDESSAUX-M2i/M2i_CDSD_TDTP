# Exercice 2 : Tokenization et Vectorisation

## Objectif

Maîtriser les techniques de vectorisation de texte (Bag of Words, TF-IDF, Count Vectorizer) et comprendre leur impact sur la représentation des documents.

## Contexte

Vous travaillez sur la classification de critiques de films. Chaque critique doit être transformée en vecteur numérique pour alimenter des modèles ML. Vous explorerez différentes techniques de vectorisation et leurs avantages/inconvénients.

## Données

Utilisez ce corpus de critiques courts :

```python
critiques = [
    "Ce film est absolument fantastique! La cinématographie est magnifique.",
    "Quel ennui... le scénario est prévisible et les acteurs sans charisme.",
    "Un excellent film! Très émouvant et bien réalisé. À voir!",
    "Décevant. Les effets spéciaux sont bons mais l'histoire manque de profondeur.",
    "Masterpiece! Un incontournable. Brillant du début à la fin.",
    "Horrible film. Perte de temps totale. Pas recommandé."
]

labels = [1, 0, 1, 0, 1, 0]  # 1 = positif, 0 = négatif
```

## Tâches

### Tâche 1 : Count Vectorizer (Bag of Words)

1. Utilisez `CountVectorizer` de scikit-learn sur le corpus
2. Configurez-le pour :
   - Convertir en minuscules
   - Supprimer les stopwords français
   - Ignorer les termes qui apparaissent dans moins de 1 document
   - Limiter à 100 termes maximum
3. Affichez :
   - La forme de la matrice (nombre de documents x nombre de features)
   - Les noms des features (vocabulaire)
   - La matrice de densité

**Attendus** : Matrice Bag of Words, visualisation du vocabulaire

### Tâche 2 : Analyse du vocabulaire

1. Calculez la fréquence de chaque term dans le corpus
2. Identifiez les 10 termes les plus fréquents
3. Affichez-les avec leurs comptes
4. Analysez : ces termes sont-ils pertinents pour la classification sentiments?

**Attendus** : Ranking des termes, analyse critique

### Tâche 3 : TF-IDF Vectorizer

1. Utilisez `TfidfVectorizer` sur le même corpus
2. Configurez-le avec les mêmes paramètres que CountVectorizer
3. Comparez :
   - La matrice TF-IDF avec la matrice Bag of Words
   - Les scores TF-IDF des 5 premiers documents
4. Démontrez pourquoi TF-IDF est supérieur à BoW pour identifier les termes discriminants

**Attendus** : Matrice TF-IDF, comparaison quantifiée BoW vs TF-IDF

### Tâche 4 : Densité et Sparsité

1. Calculez le pourcentage d'éléments non-nuls dans chaque matrice
2. Comparez la mémoire utilisée par une matrice dense vs une matrice creuse (sparse)
3. Créez une visualisation (heatmap) montrant la sparsité
4. Quelle matrice utiliserait-on pour un corpus massif? Pourquoi?

**Attendus** : Analyse quantifiée, visualisation, recommandations

### Tâche 5 : Influence de la normalisation

1. Entraînez deux `TfidfVectorizer` :
   - L1 norm (L1)
   - L2 norm (L2)
2. Comparez les scores TF-IDF obtenus
3. Visualisez les différences sur les 3 premiers documents
4. Expliquez : quelle norme utiliser et pourquoi?

**Attendus** : Comparaison L1/L2, recommandations justifiées

### Tâche 6 : Application pratique

1. Créez une pipeline :
   - Nettoyage du texte (réutilisez l'exercice 1)
   - Vectorisation TF-IDF
2. Entraînez un classifieur simple (LogisticRegression)
3. Évaluez la performance (accuracy, precision, recall)

**Attendus** : Pipeline fonctionnel, prédiction sur nouveau texte

## Critères d'évaluation

- CountVectorizer configuré et compris
- Vocabulaire extrait et analysé
- TF-IDF implémenté et comparé
- Concepts de densité/sparsité maîtrisés
- Pipeline complet fonctionnel

## Conseils

- Importez : `from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer`
- `.get_feature_names_out()` retourne le vocabulaire
- `.toarray()` convertit en matrice dense (attention à la mémoire!)
- Utilisez `scipy.sparse` pour les opérations sur matrices creuses
- Visualisez avec `matplotlib` ou `seaborn`

## Bonus (Optionnel)

- Utilisez `max_features` pour comparer l'impact du vocabulaire réduit
- Testez différents `ngram_range` (unigrammes vs bigrammes)
- Implémentez votre propre TF-IDF depuis zéro
- Comparez les performances avec d'autres classifieurs (SVM, Random Forest)

# Exercice 3 : Word2Vec et Embeddings

## Objectif
Comprendre et implémenter Word2Vec (Skip-gram et CBOW), générer des embeddings denses, et exploiter la similarité sémantique pour des applications pratiques.

## Contexte
Au lieu de vecteurs creux (BoW, TF-IDF), vous apprendrez à générer des embeddings denses qui capturent le contexte sémantique des mots. Ces embeddings permettent des calculs plus riches : similarité, analogies, visualisation 2D, etc.

## Données

### Corpus d'entraînement
Utilisez ce corpus pour entraîner Word2Vec :

```python
corpus = [
    "Le machine learning est une branche de l'intelligence artificielle",
    "L'intelligence artificielle révolutionne les technologies modernes",
    "Les réseaux de neurones sont au cœur du deep learning",
    "Le deep learning utilise les réseaux de neurones profonds",
    "Les algorithmes d'apprentissage automatique traitent les données",
    "L'apprentissage profond demande beaucoup de données et de puissance calcul",
    "Les embeddings denses représentent les mots dans un espace continu",
    "La similarité cosinus mesure la proximité entre vecteurs",
    "Les modèles pré-entraînés accélèrent le développement",
    "Word2Vec génère des embeddings en capturant le contexte sémantique"
]
```

## Tâches

### Tâche 1 : Préparation des données
1. Nettoyez le corpus (utilisez l'exercice 1)
2. Tokenisez en phrases et tokens
3. Créez une liste de listes de tokens
4. Explorez la structure : nombre de phrases, moyenne de tokens par phrase

**Attendus** : Corpus préparé prêt pour Word2Vec

### Tâche 2 : Entraînement Skip-gram
1. Entraînez un modèle Word2Vec avec :
   - `sg=1` (Skip-gram)
   - `vector_size=100` (dimension des embeddings)
   - `window=5` (contexte)
   - `min_count=1` (accepter les mots uniques)
   - `epochs=20`
2. Affichez les paramètres du modèle
3. Extrayez l'embedding du mot "apprentissage"
4. Visualisez la forme : (nombre de mots, 100)

**Attendus** : Modèle Skip-gram entraîné, embedding d'un mot

### Tâche 3 : Entraînement CBOW
1. Entraînez un modèle Word2Vec avec :
   - `sg=0` (CBOW)
   - Mêmes paramètres que Skip-gram
2. Comparez les embeddings avec Skip-gram :
   - Embeddings identiques?
   - Performances différentes?
   - Avantages/inconvénients de chaque approche?

**Attendus** : Modèle CBOW, comparaison avec Skip-gram

### Tâche 4 : Similarité et opérations sémantiques
1. Calculez la similarité cosinus entre :
   - "machine learning" et "apprentissage automatique"
   - "deep learning" et "réseaux neuronaux"
   - "apprentissage" et "données"
2. Trouvez les 5 mots les plus similaires à "intelligence artificielle"
3. Trouvez les 5 mots les plus dissimilaires
4. Testez les analogies Word2Vec : "intelligence" - "artificielle" + "machine" ≈ ?

**Attendus** : Scores de similarité, mots similaires, analogies sémantiques

### Tâche 5 : Visualisation des embeddings
1. Réduisez les embeddings en 2D avec t-SNE ou PCA
2. Visualisez les mots :
   - Coloriez par thème (ML, IA, données, etc.)
   - Annotez les points
3. Observez les clusters
4. Interprétez la disposition spatiale : mots proches = similaires?

**Attendus** : Visualisation 2D annotée, interprétation

### Tâche 6 : Embeddings de documents
1. Créez des embeddings de documents par moyenne des embeddings de tokens :
   ```python
   doc_embedding = moyenne(embeddings[tokens])
   ```
2. Calculez la similarité entre les 6 documents du corpus
3. Créez une matrice de similarité (heatmap)
4. Identifiez les paires de documents les plus similaires

**Attendus** : Embeddings de documents, matrice de similarité, visualisation

### Tâche 7 : Comparaison Word2Vec vs TF-IDF
1. Créez deux représentations d'un même document :
   - Vecteur TF-IDF (exercice 2)
   - Vecteur Word2Vec (moyenne des embeddings)
2. Calculez la similarité cosinus entre deux documents avec chaque méthode
3. Comparez : qu'apporte Word2Vec que TF-IDF n'a pas?
4. Quand utiliser l'une vs l'autre?

**Attendus** : Comparaison quantifiée, recommandations

## Critères d'évaluation

- Modèles Skip-gram et CBOW entraînés
- Similarité sémantique calculée et validée
- Embeddings visualisés en 2D
- Analogies sémantiques explorées
- Documents représentés par embeddings
- Comparaison Word2Vec vs TF-IDF réalisée

## Conseils

- Utilisez Gensim : `from gensim.models import Word2Vec`
- `.most_similar()` retourne les mots les plus proches
- `.similarity()` calcule la similarité cosinus
- `sklearn.manifold.TSNE` pour la réduction 2D
- Sauvegardez le modèle : `.save("word2vec.model")`

## Bonus (Optionnel)

- Entraînez sur un corpus plus grand (Wikipedia, news, etc.)
- Explorez GloVe comme alternative à Word2Vec
- Implémentez le contexte personnalisé (skip-gram manuel)
- Utilisez des embeddings pré-entraînés (FastText, Word2Vec Google)
- Comparez l'impact de `vector_size` (50, 100, 300) sur la qualité

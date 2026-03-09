# Exercice 1 : Nettoyage du Texte

## Objectif
Maîtriser les techniques de prétraitement du texte en appliquant le nettoyage, la tokenization, la suppression des stopwords et la lemmatisation.

## Contexte
Vous travaillez sur un projet d'analyse de tweets. Les données brutes contiennent du bruit : URL, mentions, hashtags, ponctuation excessive, etc. Votre tâche est de nettoyer ces textes pour les rendre exploitables.

## Données
Vous travaillerez avec ce corpus de tweets :

```python
tweets = [
    "Just finished my breakfast!! Check out https://t.co/xyz #goodMorning ☀️😊",
    "Loving the new #Python3.10 features... performance is amazing!!!",
    "@john_doe The movie was REALLY bad... waste of time :(",
    "Don't miss our special offer!!! Visit our website: https://example.com",
    "I can't believe it's Friday!!! #TGIF #Weekend",
    "Machine Learning & Deep Learning are the future of tech!!! 🚀🚀🚀"
]
```

## Tâches

### Tâche 1 : Conversion et gestion de base
1. Convertissez tous les tweets en minuscules
2. Supprimez les URLs (identifiez-les avec une regex)
3. Supprimez les mentions (@user) et les hashtags
4. Supprimez les emojis
5. Remplacez les caractères dupliqués excessifs (!!!, ???, ...) par un seul exemplaire

**Attendus** : Un texte propre sans bruit, en minuscules

### Tâche 2 : Gestion de la ponctuation et des caractères spéciaux
1. Supprimez la ponctuation inutile, SAUF les apostrophes qui doivent être conservées pour les contractions
2. Supprimez les espaces multiples
3. Gérez les cas particuliers :
   - "can't" doit rester "can't" (contraction)
   - "don't" doit rester "don't"
4. Testez votre logique sur : `"I can't believe... it's AMAZING!!!"`

**Attendus** : Texte normalité avec ponctuation gérée correctement

### Tâche 3 : Tokenization et stopwords
1. Tokenisez le texte nettoyé (utilisez NLTK ou une approche simple split)
2. Créez une liste personnalisée de stopwords en français ET en anglais
3. Supprimez les stopwords
4. Gardez les contractions comme "can't", "don't" comme tokens entiers

**Attendus** : Liste de tokens significatifs

### Tâche 4 : Lemmatisation
1. Implémentez la lemmatisation avec NLTK WordNetLemmatizer
2. Appliquez-la sur les tokens filtrés
3. Comparez avant/après (montrez des exemples)
4. Optionnel : Utilisez SpaCy pour un résultat amélioré

**Attendus** : Tokens lemmatisés

### Tâche 5 : Pipeline complet
1. Créez une fonction `clean_tweet(text)` qui applique TOUTES les étapes précédentes
2. Testez-la sur l'ensemble du corpus
3. Affichez avant/après pour 3 tweets
4. Mesurez la réduction du vocabulaire (nombre de tokens uniques avant/après)

## Critères d'évaluation

- Toutes les URLs supprimées
- Emojis et caractères spéciaux supprimés
- Contractions conservées (can't, don't)
- Stopwords supprimés
- Lemmatisation appliquée correctement
- Pipeline réutilisable et testé

## Conseils

- Utilisez `re` (regex) pour les suppressions complexes
- NLTK propose `nltk.corpus.stopwords.words('english')` et `'french'`
- `WordNetLemmatizer` nécessite le POS tagging pour être vraiment efficace
- SpaCy est plus puissant que NLTK pour la lemmatisation
- Testez régulièrement pour voir l'impact de chaque étape

## Bonus (Optionnel)

- Implémentez le stemming avec PorterStemmer et comparez avec la lemmatisation
- Gérez les cas spéciaux français : accents, traits d'union
- Créez une classe `TextCleaner` réutilisable avec configuration

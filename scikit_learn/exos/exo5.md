# Exercice : Détection de Spam avec Ensemble Learning

## Contexte

Vous êtes data scientist pour un fournisseur de messagerie email. Chaque jour, des millions de spams arrivent dans les boîtes de réception. Votre mission est de créer le système de filtrage anti-spam le plus performant possible en combinant intelligemment plusieurs algorithmes de machine learning.

## Dataset

Utilisez le célèbre Spambase Dataset de l'UCI :

```python
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml

# Chargement du dataset Spambase
# Alternative si fetch_openml ne fonctionne pas : utiliser le code de génération ci-dessous
try:
    spam_data = fetch_openml('spambase', version=1, parser='auto')
    X = pd.DataFrame(spam_data.data, columns=spam_data.feature_names)
    y = spam_data.target.astype(int)
except:
    # Génération d'un dataset synthétique réaliste
    from sklearn.datasets import make_classification

    np.random.seed(42)
    X_base, y = make_classification(
        n_samples=4601,
        n_features=57,
        n_informative=45,
        n_redundant=12,
        n_classes=2,
        weights=[0.6, 0.4],  # 40% de spam
        flip_y=0.05,
        random_state=42
    )

    # Création de noms de features réalistes
    feature_names = (
        [f'word_freq_{w}' for w in ['make', 'address', 'all', 'free', 'business',
                                      'email', 'you', 'credit', 'money', 'order']] +
        [f'word_freq_generic_{i}' for i in range(1, 38)] +
        [f'char_freq_{c}' for c in ['semicolon', 'parenthesis', 'bracket',
                                      'exclamation', 'dollar', 'hashtag']] +
        ['capital_run_avg', 'capital_run_longest', 'capital_run_total']
    )

    X = pd.DataFrame(X_base, columns=feature_names)
    # Assurer des valeurs positives (fréquences)
    X = X.abs()

print(f"Dataset : {X.shape[0]} emails, {X.shape[1]} caractéristiques")
print(f"Proportion de spam : {y.mean():.1%}")
```

## Caractéristiques du dataset

Le dataset contient 57 features calculées pour chaque email :

### 1. Fréquences de mots (48 features)

- Pourcentage d'apparition de mots-clés suspects : "free", "money", "credit", "winner", etc.
- Exemple : `word_freq_free` = 2.5 signifie que le mot "free" apparaît dans 2.5% du texte

### 2. Fréquences de caractères (6 features)

- Fréquence de caractères spéciaux : `;`, `(`, `[`, `!`, `$`, `#`
- Les spams abusent souvent de `!` et `$`

### 3. Caractéristiques des majuscules (3 features)

- `capital_run_avg` : Longueur moyenne des séquences de majuscules
- `capital_run_longest` : Plus longue séquence de majuscules
- `capital_run_total` : Nombre total de majuscules
- Les spams utilisent souvent BEAUCOUP DE MAJUSCULES !!!

### Variable cible

- **y** : 0 = Email légitime (ham), 1 = Spam

## Étapes à réaliser

### 1. Exploration et préparation

- Vérifiez les valeurs manquantes
- Divisez en train/test (80/20) avec `stratify=y`
- Standardisez les données avec `StandardScaler`

### 2. Modèles de base (Baseline)

Entraînez 4 modèles simples pour avoir une référence :

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
```

- Quel modèle baseline est le meilleur ?
- Quelle métrique est la plus importante pour un filtre anti-spam ? (Accuracy, Precision, Recall ?)
  - **Precision** : Parmi les emails classés comme spam, combien sont vraiment des spams ?
  - **Recall** : Parmi tous les spams, combien sont détectés ?

### 3. Voting Classifier

**Questions** :

- Comparez hard et soft voting
- Lequel performe le mieux ?
- Le voting surpasse-t-il les modèles individuels ?

### 4. Tableau comparatif et analyse

Créez un tableau résumant TOUS vos résultats :

### 5. Matrice de confusion du meilleur modèle

**Analyse de la matrice** :

- Combien d'emails légitimes sont bloqués par erreur (Faux Positifs) ?
- Combien de spams passent à travers (Faux Négatifs) ?
- Quel type d'erreur est le plus problématique pour l'utilisateur ?

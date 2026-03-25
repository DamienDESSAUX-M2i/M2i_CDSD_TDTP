# Exercice NLP — Classification de Textes : Offres d'Emploi & CV

## Contexte

Une startup spécialisée dans le recrutement souhaite automatiser la **catégorisation de documents textuels** issus de sa plateforme. Elle reçoit chaque jour des centaines de textes mélangés — des offres d'emploi publiées par des entreprises et des résumés de profils issus de CV — et a besoin d'un modèle capable de les distinguer automatiquement.

Vous êtes mandaté(e) pour construire un **pipeline NLP de bout en bout** :

- Génération et nettoyage du corpus textuel
- Représentation vectorielle des textes
- Entraînement d'un modèle de classification binaire
- Évaluation et analyse des résultats

## Partie 0 — Génération du Dataset

En l'absence d'un dataset public fourni, vous allez **simuler un corpus réaliste** à l'aide du code ci-dessous.

```python
import pandas as pd
import random

random.seed(42)

offres = [
    "Nous recherchons un développeur Python expérimenté pour rejoindre notre équipe. CDI, télétravail partiel, salaire selon profil.",
    "Poste de Data Scientist à pourvoir immédiatement. Maîtrise de scikit-learn et SQL indispensable. Bac+5 requis.",
    "Offre d'emploi : Chef de projet digital, 5 ans d'expérience minimum, secteur e-commerce, Paris 75008.",
    "Recrutement urgent : technicien réseau, habilitation sécurité souhaitée, contrat 12 mois renouvelable.",
    "Rejoignez notre cabinet comptable : poste de comptable senior, maîtrise de Sage, déplacements occasionnels.",
    "Nous recrutons un ingénieur DevOps. Expérience Kubernetes et CI/CD requise. Startup en forte croissance.",
    "Offre : Responsable RH, gestion de 200 collaborateurs, connaissance du droit social impérative.",
    "Recherche commercial terrain BtoB, véhicule de fonction fourni, variable attractif, secteur PACA.",
    "CDI à pourvoir : UX Designer, maîtrise de Figma, portfolio exigé, environnement agile.",
    "Poste ouvert : analyste financier junior, formation assurée, diplôme grande école apprécié.",
]

cvs = [
    "Ingénieur logiciel avec 7 ans d'expérience en Python et Java. Diplômé de l'INSA Lyon. Passionné par l'IA.",
    "Data Analyst junior, maîtrise de Power BI et Excel avancé. À la recherche d'une opportunité en CDI sur Paris.",
    "Profil polyvalent : marketing digital, gestion de communauté, création de contenu. 3 ans d'expérience.",
    "Développeur fullstack React/Node.js, freelance depuis 2 ans, disponible pour mission longue durée.",
    "Comptable confirmé, 10 ans en cabinet d'expertise, maîtrise de Cegid et des normes IFRS.",
    "Chargée de communication, bilingue anglais-espagnol, expérience ONG et secteur privé.",
    "Technicien informatique, certifié CISCO CCNA, disponible immédiatement, mobilité nationale.",
    "Chef de projet IT, certifié PMP, expérience en transformation digitale dans le secteur bancaire.",
    "Juriste d'entreprise, spécialité droit des contrats et propriété intellectuelle, 5 ans en startup.",
    "Graphiste freelance, maîtrise Adobe Suite, portfolio disponible sur demande, ouvert au CDI.",
]

# Duplication pour enrichir le corpus
data = []
for _ in range(10):
    for texte in offres:
        data.append({"texte": texte + f" (réf. {random.randint(1000,9999)})", "label": "offre"})
    for texte in cvs:
        data.append({"texte": texte + f" (id {random.randint(1000,9999)})", "label": "cv"})

df = pd.DataFrame(data).sample(frac=1, random_state=42).reset_index(drop=True)
print(df["label"].value_counts())
df.to_csv("corpus_emploi.csv", index=False)
```

**Résultat attendu** : un fichier `corpus_emploi.csv` contenant 200 entrées équilibrées (100 offres / 100 CV).

## Partie 1 — Extraction et Nettoyage des Données

### 1.1 Chargement et exploration

**Questions :**

- Combien de textes contient le dataset ?
- Les classes sont-elles équilibrées ?

### 1.2 Nettoyage du texte

Implémentez la fonction `nettoyer_texte(texte)` qui réalise les opérations suivantes :

1. Conversion en minuscules
2. Suppression des chiffres et des références entre parenthèses
3. Suppression de la ponctuation
4. Suppression des stopwords français
5. Lemmatisation

### 1.3 Analyse exploratoire

Réalisez les analyses suivantes :

- **Distribution de la longueur des textes** (en nombre de mots) pour chaque classe
- **Top 15 des mots les plus fréquents** dans les offres vs dans les CV (utilisez `Counter`)
- **Nuage de mots** (avec `wordcloud`) pour chaque catégorie

## Partie 2 — Vectorisation des Textes avec TensorFlow

### 2.1 Préparation du tokenizer

Utilisez `tensorflow.keras.preprocessing.text.Tokenizer` pour convertir les textes en séquences :

```python
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Tokenisation
max_words = 5000  # Taille du vocabulaire
max_len = 50      # Longueur maximale des séquences

tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
tokenizer.fit_on_texts(X_train)

# Conversion en séquences
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Padding
X_train_pad = pad_sequences(X_train_seq, maxlen=max_len, padding='post', truncating='post')
X_test_pad = pad_sequences(X_test_seq, maxlen=max_len, padding='post', truncating='post')
```

### 2.2 Encodage des labels

## Partie 3 — Entraînement de Réseaux de Neurones avec TensorFlow

Vous allez construire et comparer **plusieurs architectures** de réseaux de neurones.

### 3.1 Modèle Dense Simple

Créez un réseau avec embedding + couches denses :

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, Flatten, Dropout

embedding_dim = 128

model_dense = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Flatten(),
    # Vos couches...
])
```

Entraînez le modèle

### 3.2 Modèle avec GlobalAveragePooling1D

Alternative au Flatten, plus légère :

```python
from tensorflow.keras.layers import GlobalAveragePooling1D

model_gap = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    GlobalAveragePooling1D(),
    # Vos couches...
])
```

### 3.3 Modèle CNN (Convolutional Neural Network)

Les CNN capturent des patterns locaux dans le texte :

```python
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D

model_cnn = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Conv1D(128, 5, activation='relu'),
    GlobalMaxPooling1D(),
    # Vos couches...
])
```

### 3.4 Modèle LSTM (Recurrent Neural Network)

Les LSTM capturent les dépendances séquentielles :

```python
from tensorflow.keras.layers import LSTM

model_lstm = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    LSTM(64, dropout=0.2, recurrent_dropout=0.2),
    # Vos couches...
])
```

### 3.5 Modèle Bidirectionnel LSTM

Version améliorée qui lit le texte dans les deux sens :

```python
from tensorflow.keras.layers import Bidirectional

model_bilstm = Sequential([
    Embedding(max_words, embedding_dim, input_length=max_len),
    Bidirectional(LSTM(64, dropout=0.2, recurrent_dropout=0.2)),
    # Vos couches...
])
```

## Partie 4 — Évaluation et Comparaison

### 4.1 Visualisation de l'entraînement

Pour chaque modèle, visualisez les courbes d'apprentissage :

### 4.2 Métriques de classification

### 4.3 Tableau de synthèse

Complétez le tableau suivant avec vos résultats :

| Modèle       | Accuracy | F1 (offre) | F1 (cv) | AUC | Temps d'entraînement |
| ------------ | -------- | ---------- | ------- | --- | -------------------- |
| Dense Simple | ?        | ?          | ?       | ?   | ?                    |
| GAP          | ?        | ?          | ?       | ?   | ?                    |
| CNN          | ?        | ?          | ?       | ?   | ?                    |
| LSTM         | ?        | ?          | ?       | ?   | ?                    |
| Bi-LSTM      | ?        | ?          | ?       | ?   | ?                    |

## Partie 5 : Prédiction sur de Nouveaux Textes

Utilisez votre meilleur modèle pour prédire la catégorie de ces textes inédits

# Exercice 1 : Créer un Space Streamlit Multi-Modèles

## Objectif

Créer et déployer une application Streamlit sur Hugging Face Spaces avec plusieurs modèles NLP.

## Énoncé

Vous devez créer une application Streamlit qui propose **3 fonctionnalités NLP** :

1. **Résumé de texte** (Text Summarization)
2. **Traduction** (EN → FR)
3. **Classification d'émotions** (6 émotions)

L'application doit être déployée sur Hugging Face Spaces et accessible publiquement.

## Niveau 1 : Basique

### Tâche 1 : Créer l'application Streamlit

**Fichiers à créer** :

```
exercice_streamlit/
├── app.py
├── requirements.txt
└── README.md
```

**Spécifications** :

**app.py** (template de départ) :

```python
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="NLP Suite", page_icon="🤖", layout="wide")

st.title("Suite NLP Multi-Tâches")

# TODO: Charger les modèles
# summarizer = pipeline("summarization", model="...")
# translator = pipeline("translation", model="...")
# emotion_classifier = pipeline("text-classification", model="...")

# TODO: Créer des onglets avec st.tabs()

# TODO: Onglet 1 : Résumé de texte
#   - Input: st.text_area pour le texte long
#   - Button: "Résumer"
#   - Output: Afficher le résumé

# TODO: Onglet 2 : Traduction
#   - Input: st.text_area pour texte anglais
#   - Button: "Traduire"
#   - Output: Afficher la traduction française

# TODO: Onglet 3 : Classification d'émotions
#   - Input: st.text_input pour une phrase
#   - Button: "Analyser"
#   - Output: Afficher l'émotion détectée
```

**requirements.txt** :

```
streamlit==1.28.0
transformers==4.35.0
torch==2.1.0
```

**README.md** :

```markdown
---
title: NLP Multi-Tasks
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
---

# NLP Multi-Tasks Suite

Application Streamlit avec 3 fonctionnalités NLP.
```

### Modèles à utiliser :

1. **Résumé** : `facebook/bart-large-cnn`
2. **Traduction** : `Helsinki-NLP/opus-mt-en-fr`
3. **Émotions** : `j-hartmann/emotion-english-distilroberta-base`

### Aide :


doc streamlit : https://docs.streamlit.io/
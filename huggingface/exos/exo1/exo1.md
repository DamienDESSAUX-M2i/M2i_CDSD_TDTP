# Exercice 1 : Dockeriser un Modèle NLP

## Objectif

Créer une image Docker pour un modèle de classification de texte Hugging Face.

## Énoncé

Vous devez créer une API de classification de texte qui peut détecter la langue d'un texte et classifier son sujet.

## Partie 1 : Détection de langue

### Tâche 1 : Créer l'API de base

Créez une API Flask qui utilise le modèle `papluca/xlm-roberta-base-language-detection` pour détecter la langue d'un texte.

**Fichiers à créer** :

```
exercice1/
├── Dockerfile
├── requirements.txt
├── app.py
└── test_requests.sh
```

**Spécifications** :

L'API doit avoir :

- `GET /health` : Retourne le statut de l'API
- `POST /detect` : Détecte la langue d'un texte
- `POST /detect/batch` : Détecte la langue pour plusieurs textes

**Format de requête** :

```json
{
  "text": "Bonjour, comment allez-vous?"
}
```

**Format de réponse attendu** :

```json
{
  "text": "Bonjour, comment allez-vous?",
  "language": "fr",
  "confidence": 0.9987
}
```

### Niveau 1 : Basique

**app.py** (template de départ) :

```python
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# TODO: Charger le modèle de détection de langue
# model_name = "papluca/xlm-roberta-base-language-detection"
# detector = pipeline("text-classification", model=model_name)

@app.route('/health')
def health():
    # TODO: Implémenter
    pass

@app.route('/detect', methods=['POST'])
def detect():
    # TODO: Implémenter la détection pour un texte
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Dockerfile** (à compléter) :

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# TODO: Copier requirements.txt et installer les dépendances

# TODO: Copier le code

# TODO: Télécharger le modèle au build time

EXPOSE 8000

CMD ["python", "app.py"]
```

**requirements.txt** :

```
flask==2.3.0
transformers==4.35.0
torch==2.1.0
```

### Niveau 2 : Intermédiaire

Ajoutez les fonctionnalités suivantes :

1. **Endpoint batch** :

```python
@app.route('/detect/batch', methods=['POST'])
def detect_batch():
    # Accepter une liste de textes
    # Retourner les résultats pour chaque texte
    pass
```

2. **Gestion d'erreurs** :

- Texte vide
- Texte trop long (> 500 caractères)
- Format JSON invalide

3. **Optimisation Docker** :

- Utiliser multi-stage build
- Réduire la taille de l'image

# Exercice 3 : Persistance des données avec les Volumes

## Objectif

Comprendre et maîtriser les volumes Docker pour persister les données d'un projet ML.

## Contexte

Vous développez un système d'entraînement de modèles ML qui doit :

1. Sauvegarder les modèles entraînés
2. Logger les métriques d'entraînement
3. Garder une trace des expérimentations

Le problème : chaque fois que le conteneur s'arrête, tout est perdu ! Vous devez implémenter une solution de persistance.

## Partie 1 : Démonstration du problème

### Étape 1 : Créer un script qui génère des données

**train_with_logs.py** :

```python
import json
import os
from datetime import datetime
import random

def train_model():
    # Simuler un entraînement
    accuracy = random.uniform(0.7, 0.95)
    loss = random.uniform(0.1, 0.5)

    # Créer un log
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'accuracy': accuracy,
        'loss': loss,
        'model_version': 'v1.0'
    }

    # Sauvegarder dans un fichier
    os.makedirs('logs', exist_ok=True)
    log_file = f'logs/training_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

    with open(log_file, 'w') as f:
        json.dump(log_entry, f, indent=2)

    print(f"Modèle entraîné!")
    print(f"   Accuracy: {accuracy:.2%}")
    print(f"   Loss: {loss:.4f}")
    print(f"Log sauvegardé: {log_file}")

    # Lister tous les logs
    logs = os.listdir('logs')
    print(f"Total de {len(logs)} entraînements enregistrés")

if __name__ == '__main__':
    train_model()
```

### Étape 2 : Créer le Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY train_with_logs.py .

ENTRYPOINT ["python", "train_with_logs.py"]
```

### Étape 3 : Constater le problème

```bash
# Construire l'image
docker build -t ml-logger .

# Premier entraînement
docker run ml-logger
# Résultat : 1 entraînement enregistré

# Deuxième entraînement
docker run ml-logger
# Résultat : 1 entraînement enregistré (pas 2 !)

# Problème : Les données sont perdues entre chaque exécution
```

## Partie 2 : Solution avec Bind Mount

### Tâche 1 : Utiliser un bind mount

Montez un dossier local pour persister les logs.

```bash
docker run -it -v ${PWD}/logs:/app/logs ml-logger
```

## Partie 3 : Solution avec Named Volume

### Tâche 2 : Utiliser un volume nommé

```bash
docker volume create v_logs

docker run -it -v v_logs:/app/logs ml-logger
```

## Partie 4 : Projet complet avec multiples volumes

### Tâche 4 : Créer une architecture avec plusieurs volumes

Créez un script qui :

1. Lit des données d'entrée
2. Entraîne un modèle
3. Sauvegarde le modèle
4. Sauvegarde les métriques

**Structure souhaitée** :

```
/app/data/      → Volume pour les données d'entrée
/app/models/    → Volume pour les modèles entraînés
/app/logs/      → Volume pour les logs
```

**requirements.txt** :

```
pandas==2.0.0
scikit-learn==1.3.0
```

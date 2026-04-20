# Exercice 2 : Configuration avec Variables d'Environnement

## Objectif

Apprendre à configurer des conteneurs Docker avec des variables d'environnement pour gérer différents environnements (dev/prod).

## Contexte

Vous devez déployer un système de prédiction ML qui fonctionne différemment selon l'environnement :

**Développement** :

- Mode verbose (logs détaillés)
- Modèle simple (rapide à entraîner)
- Petites données de test

**Production** :

- Logs minimaux
- Modèle optimisé
- Vraies données
- Monitoring activé

---

## Partie 1 : Configuration basique

### Tâche 1 : Créer un script configurable

**model_trainer.py** :

```python
import os
import json
from datetime import datetime

# Récupérer la configuration depuis l'environnement
ENV = os.getenv('ENVIRONMENT', 'development')
MODEL_TYPE = os.getenv('MODEL_TYPE', 'simple')
N_ESTIMATORS = int(os.getenv('N_ESTIMATORS', '10'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ENABLE_MONITORING = os.getenv('ENABLE_MONITORING', 'false').lower() == 'true'

def log(message, level='INFO'):
    """Log avec niveau de détail configurable"""
    if LOG_LEVEL == 'DEBUG' or level != 'DEBUG':
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")

def train_model():
    log(f"CONFIGURATION - Environnement: {ENV}")

    log(f"Model Type: {MODEL_TYPE}")
    log(f"N Estimators: {N_ESTIMATORS}")
    log(f"Log Level: {LOG_LEVEL}")
    log(f"Monitoring: {'Enabled' if ENABLE_MONITORING else 'Disabled'}")

    log("\nDémarrage de l'entraînement...", 'INFO')

    # Simuler un entraînement
    if MODEL_TYPE == 'simple':
        log("Utilisation d'un modèle simple (rapide)", 'DEBUG')
        training_time = 2
    else:
        log("Utilisation d'un modèle optimisé (lent)", 'DEBUG')
        training_time = 10

    log(f"Temps d'entraînement estimé: {training_time}s", 'DEBUG')

    # Simuler des étapes
    for i in range(N_ESTIMATORS // 10):
        log(f"Entraînement de l'arbre {i+1}...", 'DEBUG')

    log("Entraînement terminé!", 'INFO')

    # Monitoring
    if ENABLE_MONITORING:
        log("\nMONITORING", 'INFO')
        metrics = {
            'environment': ENV,
            'model_type': MODEL_TYPE,
            'n_estimators': N_ESTIMATORS,
            'timestamp': datetime.now().isoformat()
        }
        log(f"Metrics: {json.dumps(metrics, indent=2)}", 'DEBUG')

if __name__ == '__main__':
    train_model()
```

1. Créez le **Dockerfile**
2. testez différentes configurations

## Partie 2 : Utiliser des fichiers .env

### Tâche 2 : Créer des configurations par environnement

**dev.env** :

```env
ENVIRONMENT=development
MODEL_TYPE=simple
N_ESTIMATORS=10
LOG_LEVEL=DEBUG
ENABLE_MONITORING=false
DATA_PATH=/app/data/sample.csv
MODEL_OUTPUT=/app/models/dev/
```

**prod.env** :

```env
ENVIRONMENT=production
MODEL_TYPE=optimized
N_ESTIMATORS=200
LOG_LEVEL=WARNING
ENABLE_MONITORING=true
DATA_PATH=/app/data/production.csv
MODEL_OUTPUT=/app/models/prod/
```

**staging.env** :

```env
ENVIRONMENT=staging
MODEL_TYPE=optimized
N_ESTIMATORS=100
LOG_LEVEL=INFO
ENABLE_MONITORING=true
DATA_PATH=/app/data/staging.csv
MODEL_OUTPUT=/app/models/staging/
```

1. Testez avec les fichiers .env

## Partie 3 : Projet complet avec configuration avancée

### Tâche 3 : Créer un système complet

**advanced_trainer.py** :

```python
import os
import json
import pickle
from datetime import datetime
from pathlib import Path
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class Config:
    """Classe de configuration centralisée"""

    def __init__(self):
        # Environnement
        self.environment = os.getenv('ENVIRONMENT', 'development')

        # Chemins
        self.data_path = os.getenv('DATA_PATH', '/app/data/dataset.csv')
        self.model_output = os.getenv('MODEL_OUTPUT', '/app/models/')

        # Modèle
        self.model_type = os.getenv('MODEL_TYPE', 'logistic')
        self.n_estimators = int(os.getenv('N_ESTIMATORS', '100'))
        self.test_size = float(os.getenv('TEST_SIZE', '0.2'))
        self.random_state = int(os.getenv('RANDOM_STATE', '42'))

        # Logging
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.enable_monitoring = os.getenv('ENABLE_MONITORING', 'false').lower() == 'true'

        # Données
        self.n_samples = int(os.getenv('N_SAMPLES', '1000'))
        self.n_features = int(os.getenv('N_FEATURES', '20'))

    def validate(self):
        """Valider la configuration"""
        errors = []

        if self.model_type not in ['logistic', 'random_forest']:
            errors.append(f"Invalid MODEL_TYPE: {self.model_type}")

        if self.test_size <= 0 or self.test_size >= 1:
            errors.append(f"Invalid TEST_SIZE: {self.test_size}")

        if self.n_estimators <= 0:
            errors.append(f"Invalid N_ESTIMATORS: {self.n_estimators}")

        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors))

    def display(self):
        """Afficher la configuration"""
        print(f"CONFIGURATION - {self.environment.upper()}")
        print(f"Environment:       {self.environment}")
        print(f"Model Type:        {self.model_type}")
        print(f"N Estimators:      {self.n_estimators}")
        print(f"Test Size:         {self.test_size}")
        print(f"Random State:      {self.random_state}")
        print(f"Data Path:         {self.data_path}")
        print(f"Model Output:      {self.model_output}")
        print(f"Log Level:         {self.log_level}")
        print(f"Monitoring:        {self.enable_monitoring}")

class Logger:
    def __init__(self, level='INFO'):
        self.level = level
        self.levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}

    def log(self, message, level='INFO'):
        if self.levels.get(level, 1) >= self.levels.get(self.level, 1):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] [{level}] {message}")

def main():
    # Charger et valider la configuration
    config = Config()

    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error:\n{e}")
        return

    config.display()

    # Logger
    logger = Logger(config.log_level)

    # Charger ou générer les données
    logger.log("Chargement des données...", 'INFO')

    if Path(config.data_path).exists():
        logger.log(f"Lecture depuis {config.data_path}", 'DEBUG')
        df = pd.read_csv(config.data_path)
        X = df.drop('target', axis=1).values
        y = df['target'].values
    else:
        logger.log("Génération de données synthétiques", 'DEBUG')
        X, y = make_classification(
            n_samples=config.n_samples,
            n_features=config.n_features,
            random_state=config.random_state
        )

    logger.log(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features", 'INFO')

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.test_size,
        random_state=config.random_state
    )

    logger.log(f"Train: {len(X_train)}, Test: {len(X_test)}", 'DEBUG')

    # Entraîner le modèle
    logger.log("Entraînement du modèle...", 'INFO')

    if config.model_type == 'logistic':
        model = LogisticRegression(random_state=config.random_state, max_iter=1000)
    else:  # random_forest
        model = RandomForestClassifier(
            n_estimators=config.n_estimators,
            random_state=config.random_state
        )

    model.fit(X_train, y_train)
    logger.log("Entraînement terminé", 'DEBUG')

    # Évaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    logger.log(f"Accuracy: {accuracy:.2%}", 'INFO')

    if config.log_level == 'DEBUG':
        logger.log("\n" + classification_report(y_test, y_pred), 'DEBUG')

    # Sauvegarder le modèle
    os.makedirs(config.model_output, exist_ok=True)
    model_filename = f"model_{config.environment}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    model_path = os.path.join(config.model_output, model_filename)

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    logger.log(f"Modèle sauvegardé: {model_path}", 'INFO')

    # Monitoring
    if config.enable_monitoring:
        logger.log("Génération des métriques de monitoring", 'INFO')

        metrics = {
            'timestamp': datetime.now().isoformat(),
            'environment': config.environment,
            'model_type': config.model_type,
            'accuracy': accuracy,
            'n_samples': X.shape[0],
            'n_features': X.shape[1],
            'model_path': model_path
        }

        metrics_path = os.path.join(config.model_output, 'metrics.json')
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)

        logger.log(f"Métriques sauvegardées: {metrics_path}", 'DEBUG')

    print("\nProcessus terminé avec succès!\n")

if __name__ == '__main__':
    main()
```

**requirements.txt** :

```
pandas==2.0.0
scikit-learn==1.3.0
```

**Dockerfile** :

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configuration par défaut
ENV ENVIRONMENT=development
ENV MODEL_TYPE=logistic
ENV N_ESTIMATORS=100
ENV TEST_SIZE=0.2
ENV RANDOM_STATE=42
ENV LOG_LEVEL=INFO
ENV ENABLE_MONITORING=false
ENV DATA_PATH=/app/data/dataset.csv
ENV MODEL_OUTPUT=/app/models/
ENV N_SAMPLES=1000
ENV N_FEATURES=20

COPY advanced_trainer.py .

CMD ["python", "advanced_trainer.py"]
```

---

### Tâche 4 : Tester avec différentes configurations

**dev.env** :

```env
ENVIRONMENT=development
MODEL_TYPE=logistic
N_ESTIMATORS=10
TEST_SIZE=0.3
LOG_LEVEL=DEBUG
ENABLE_MONITORING=false
N_SAMPLES=500
N_FEATURES=10
```

**prod.env** :

```env
ENVIRONMENT=production
MODEL_TYPE=random_forest
N_ESTIMATORS=200
TEST_SIZE=0.2
LOG_LEVEL=WARNING
ENABLE_MONITORING=true
N_SAMPLES=10000
N_FEATURES=50
```

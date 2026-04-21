# Exercice Final : Projet ML Complet avec Docker Compose

## Objectif

Créer un système complet de prédiction ML avec API, base de données et interface utilisateur, orchestré par Docker Compose.

## Cahier des charges

Vous devez créer un système de **prédiction de la qualité du vin** avec :

1. **API Flask** : Entraînement et prédiction
2. **Base de données PostgreSQL** : Stockage des résultats
3. **Frontend Streamlit** : Interface utilisateur
4. **Volumes** : Persistance des modèles et données
5. **Configuration** : Variables d'environnement pour dev/prod

## Architecture cible

```
┌─────────────────────────────────┐
│   Frontend Streamlit            │  Port 8501
│   - Interface utilisateur       │
│   - Formulaire de prédiction    │
│   - Historique                  │
└───────────────┬─────────────────┘
                │
                │ HTTP
                │
┌───────────────▼─────────────────┐
│   API Flask                     │  Port 5000
│   - POST /train                 │
│   - POST /predict               │
│   - GET /history                │
│   - GET /metrics                │
└───────────────┬─────────────────┘
                │
                │ SQL
                │
┌───────────────▼─────────────────┐
│   PostgreSQL                    │  Port 5432
│   - Table: predictions          │
│   - Table: training_runs        │
└─────────────────────────────────┘
```

## Structure du projet

```
wine-ml-system/
├── docker-compose.yml
├── .env.example
├── .env
├── .gitignore
├── README.md
│
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── train.py
│   └── database.py
│
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
│
├── data/
│   └── wine_data.csv
│
└── models/
    └── (sera créé automatiquement)
```

## Partie 1 : Configuration de base

### Tâche 1.1 : Créer les fichiers de configuration

**docker-compose.yml** :

```yaml
version: "3.8"

services:
  # TODO: Définir les services database, api, frontend

volumes:
  # TODO: Définir les volumes nécessaires

networks:
  # TODO: Définir le réseau
```

**.env.example** :

```env
# Database
DB_USER=wineuser
DB_PASSWORD=CHANGE_ME
DB_NAME=winedb

# API
API_PORT=5000
MODEL_PATH=/app/models

# Frontend
FRONTEND_PORT=8501
```

**.gitignore** :

```
.env
__pycache__/
*.pyc
models/*.pkl
*.log
```

## Partie 2 : Service Database

### Tâche 2.1 : Configurer PostgreSQL dans le docker compose

## Partie 3 : Service API

### Tâche 3.1 : Créer le Dockerfile de l'API

**api/requirements.txt** :

```
flask==2.3.0
flask-cors==4.0.0
scikit-learn==1.3.0
pandas==2.0.0
psycopg2-binary==2.9.6
joblib==1.3.0
```

### Tâche 3.2 : Créer le module database

**api/database.py** :

```python
import psycopg2
import os
from contextlib import contextmanager

# Récupérer l'URL de connexion depuis les variables d'environnement
DATABASE_URL = os.getenv('DATABASE_URL')

@contextmanager
def get_db_connection():
    """Context manager pour les connexions DB"""
    # TODO: Créer la connexion à PostgreSQL
    # TODO: Fermer la connexion
    pass

def init_database():
    """Créer les tables nécessaires pour Streamlit"""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # TODO: Créer la table predictions
        # Colonnes nécessaires pour Streamlit:
        # - id (SERIAL PRIMARY KEY)
        # - fixed_acidity, volatile_acidity, citric_acid, residual_sugar (FLOAT)
        # - chlorides, free_sulfur_dioxide, total_sulfur_dioxide (FLOAT)
        # - density, ph, sulphates, alcohol (FLOAT)
        # - predicted_quality (INTEGER)
        # - timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

        # TODO: Créer la table training_runs
        # Colonnes nécessaires pour Streamlit:
        # - id (SERIAL PRIMARY KEY)
        # - model_type (VARCHAR)
        # - accuracy (FLOAT)
        # - n_samples (INTEGER)
        # - timestamp (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

        cursor.close()
        print("Database initialized")

def save_prediction(features, prediction):
    """Sauvegarder une prédiction - appelé par l'API lors d'une prédiction"""
    # TODO: Insérer les 11 features + prediction dans la table predictions
    pass

def save_training_run(model_type, accuracy, n_samples):
    """Sauvegarder un entraînement - appelé par l'API après training"""
    # TODO: Insérer model_type, accuracy, n_samples dans training_runs
    pass

def get_recent_predictions(limit=10):
    """Récupérer les dernières prédictions - utilisé par l'onglet Historique de Streamlit"""
    # TODO: SELECT * FROM predictions ORDER BY timestamp DESC LIMIT limit
    # TODO: Retourner les résultats
    pass

def get_training_history():
    """Récupérer l'historique des entraînements - utilisé par l'onglet Métriques de Streamlit"""
    # TODO: SELECT * FROM training_runs ORDER BY timestamp DESC LIMIT 20
    # TODO: Retourner les résultats
    pass
```

---

### Tâche 3.3 : Créer le module d'entraînement

**api/train.py** :

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def train_model(data_path, model_path, n_estimators=100):
    """
    Entraîner un modèle de prédiction de qualité du vin
    Appelé par l'endpoint POST /train depuis l'onglet Entraînement de Streamlit
    """

    # TODO: Charger les données CSV
    # df = pd.read_csv(...)

    # TODO: Séparer features (X) et target (y)
    # X = colonnes sauf 'quality'
    # y = colonne 'quality'

    # TODO: Split train/test (80/20, random_state=42)

    # TODO: Créer et entraîner le RandomForestClassifier
    # Paramètres: n_estimators, random_state=42, n_jobs=-1

    # TODO: Calculer l'accuracy sur le test set

    # TODO: Sauvegarder le modèle avec joblib.dump()

    # Retourner les métriques pour Streamlit (onglet Entraînement)
    return {
        'accuracy': 0.0,      # TODO: accuracy calculée
        'n_samples': 0,       # TODO: len(df)
        'n_features': 0,      # TODO: nombre de features
        'model_path': model_path
    }
```

---

### Tâche 3.4 : Créer l'application Flask

**api/app.py** :

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from datetime import datetime
import database as db
import train

app = Flask(__name__)
CORS(app)  # Nécessaire pour que Streamlit puisse appeler l'API

# Configuration des chemins
MODEL_PATH = os.getenv('MODEL_PATH', '/app/models/model.pkl')
DATA_PATH = os.getenv('DATA_PATH', '/app/data/wine_data.csv')

# Initialiser la base de données au démarrage
db.init_database()

@app.route('/health', methods=['GET'])
def health():
    """Healthcheck - appelé par la sidebar de Streamlit pour vérifier la connexion"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/train', methods=['POST'])
def train_model_endpoint():
    """
    Entraîner un nouveau modèle
    Appelé depuis l'onglet Entraînement de Streamlit
    """
    try:
        # TODO: Récupérer n_estimators depuis request.json (défaut: 100)

        # TODO: Appeler train.train_model() pour entraîner

        # TODO: Sauvegarder dans la DB avec db.save_training_run()

        # Retourner les résultats pour Streamlit
        return jsonify({
            'success': True,
            'accuracy': 0.0,           # TODO: mettre l'accuracy du résultat
            'n_samples': 0,            # TODO: mettre n_samples du résultat
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Faire une prédiction
    Appelé depuis l'onglet Prédiction de Streamlit avec les 11 caractéristiques
    """
    try:
        # Vérifier que le modèle existe
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                'success': False,
                'error': 'Model not found. Please train first.'
            }), 404

        # TODO: Charger le modèle avec joblib.load()

        # Récupérer les features depuis Streamlit (format attendu par l'app Streamlit)
        data = request.json
        features = [
            data['fixed_acidity'],
            data['volatile_acidity'],
            data['citric_acid'],
            data['residual_sugar'],
            data['chlorides'],
            data['free_sulfur_dioxide'],
            data['total_sulfur_dioxide'],
            data['density'],
            data['pH'],
            data['sulphates'],
            data['alcohol']
        ]

        # TODO: Faire la prédiction avec model.predict()

        # TODO: Sauvegarder dans la DB avec db.save_prediction()

        # Retourner le résultat pour Streamlit
        return jsonify({
            'success': True,
            'prediction': 0,  # TODO: mettre la vraie prédiction
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    """
    Récupérer l'historique des prédictions
    Appelé depuis l'onglet Historique de Streamlit
    """
    try:
        # TODO: Récupérer les prédictions avec db.get_recent_predictions(limit=20)

        # Formater pour Streamlit (attend: id, quality, timestamp)
        return jsonify({
            'success': True,
            'predictions': [
                # TODO: formater chaque prédiction p en dictionnaire
                # {'id': p[0], 'quality': p[12], 'timestamp': p[13].isoformat()}
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """
    Récupérer les métriques d'entraînement
    Appelé depuis l'onglet Métriques de Streamlit
    """
    try:
        # TODO: Récupérer les runs avec db.get_training_history()

        # Formater pour Streamlit (attend: id, model_type, accuracy, n_samples, timestamp)
        return jsonify({
            'success': True,
            'training_runs': [
                # TODO: formater chaque training run t en dictionnaire
                # {'id': t[0], 'model_type': t[1], 'accuracy': t[2],
                #  'n_samples': t[3], 'timestamp': t[4].isoformat()}
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

### Tâche 3.5 : Ajouter le service API dans docker-compose.yml

## Partie 4 : Service Frontend

### Tâche 4.1 : Créer le Dockerfile

**frontend/requirements.txt** :

```
streamlit==1.28.0
requests==2.31.0
pandas==2.0.0
plotly==5.17.0
```

### Tâche 4.2 : Créer l'application Streamlit

**frontend/app.py** :

```python
import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px

API_URL = os.getenv('API_URL', 'http://api:5000')

st.set_page_config(page_title="Wine Quality Prediction", page_icon="🍷", layout="wide")

st.title('Système de Prédiction de Qualité du Vin')

# Sidebar - Status
st.sidebar.header('Système')
try:
    health = requests.get(f'{API_URL}/health', timeout=5).json()
    st.sidebar.success(f"API: {health['status']}")
except:
    st.sidebar.error("API: Déconnectée")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Prédiction", "Entraînement", "Historique", "Métriques"])

# TAB 1: Prédiction
with tab1:
    st.header("Prédire la qualité d'un vin")

    col1, col2 = st.columns(2)

    with col1:
        fixed_acidity = st.number_input('Fixed Acidity', value=7.4, step=0.1)
        volatile_acidity = st.number_input('Volatile Acidity', value=0.7, step=0.01)
        citric_acid = st.number_input('Citric Acid', value=0.0, step=0.01)
        residual_sugar = st.number_input('Residual Sugar', value=1.9, step=0.1)
        chlorides = st.number_input('Chlorides', value=0.076, step=0.001)
        free_sulfur_dioxide = st.number_input('Free Sulfur Dioxide', value=11.0, step=1.0)

    with col2:
        total_sulfur_dioxide = st.number_input('Total Sulfur Dioxide', value=34.0, step=1.0)
        density = st.number_input('Density', value=0.9978, step=0.0001)
        pH = st.number_input('pH', value=3.51, step=0.01)
        sulphates = st.number_input('Sulphates', value=0.56, step=0.01)
        alcohol = st.number_input('Alcohol', value=9.4, step=0.1)

    if st.button('🔮 Prédire', type='primary'):
        payload = {
            'fixed_acidity': fixed_acidity,
            'volatile_acidity': volatile_acidity,
            'citric_acid': citric_acid,
            'residual_sugar': residual_sugar,
            'chlorides': chlorides,
            'free_sulfur_dioxide': free_sulfur_dioxide,
            'total_sulfur_dioxide': total_sulfur_dioxide,
            'density': density,
            'pH': pH,
            'sulphates': sulphates,
            'alcohol': alcohol
        }

        try:
            response = requests.post(f'{API_URL}/predict', json=payload)
            result = response.json()

            if result.get('success'):
                st.success(f"### Qualité prédite: {result['prediction']}/10")
            else:
                st.error(f"Erreur: {result.get('error')}")
        except Exception as e:
            st.error(f"Erreur de connexion: {e}")

# TAB 2: Entraînement
with tab2:
    st.header("Entraîner un nouveau modèle")

    n_estimators = st.slider('Nombre d\'estimateurs', 10, 500, 100, step=10)

    if st.button('Lancer l\'entraînement', type='primary'):
        with st.spinner('Entraînement en cours...'):
            try:
                response = requests.post(f'{API_URL}/train', json={'n_estimators': n_estimators})
                result = response.json()

                if result.get('success'):
                    st.success('Entraînement terminé!')
                    st.metric('Précision', f"{result['accuracy']:.2%}")
                    st.metric('Échantillons', result['n_samples'])
                else:
                    st.error(f"Erreur: {result.get('error')}")
            except Exception as e:
                st.error(f"Erreur: {e}")

# TAB 3: Historique
with tab3:
    st.header("Historique des prédictions")

    if st.button('Rafraîchir'):
        try:
            response = requests.get(f'{API_URL}/history')
            result = response.json()

            if result.get('success'):
                predictions = result['predictions']
                if predictions:
                    df = pd.DataFrame(predictions)
                    st.dataframe(df, use_container_width=True)
                    st.metric('Total de prédictions', len(predictions))
                else:
                    st.info('Aucune prédiction enregistrée')
            else:
                st.error(f"Erreur: {result.get('error')}")
        except Exception as e:
            st.error(f"Erreur: {e}")

# TAB 4: Métriques
with tab4:
    st.header("Métriques d'entraînement")

    try:
        response = requests.get(f'{API_URL}/metrics')
        result = response.json()

        if result.get('success'):
            training_runs = result['training_runs']
            if training_runs:
                df = pd.DataFrame(training_runs)

                # Graphique de l'évolution de l'accuracy
                fig = px.line(df, x='timestamp', y='accuracy',
                             title='Évolution de la précision',
                             labels={'accuracy': 'Précision', 'timestamp': 'Date'})
                st.plotly_chart(fig, use_container_width=True)

                # Tableau
                st.dataframe(df, use_container_width=True)
            else:
                st.info('Aucun entraînement enregistré')
        else:
            st.error(f"Erreur: {result.get('error')}")
    except Exception as e:
        st.error(f"Erreur: {e}")
```

---

### Tâche 4.3 : Ajouter le service frontend dans docker-compose.yml

## Partie 5 : Données de test

### Tâche 5.1 : Créer le fichier de données

**data/wine_data.csv** : (utilisez le dataset du Jour 1 ou téléchargez un vrai dataset)

## Partie 6 : Lancement et tests

### Tâche 6.1 : Créer le fichier .env

### Tâche 6.2 : Lancer le système

### Tâche 6.3 : Tester

1. **API Health**: http://localhost:5000/health
2. **Frontend**: http://localhost:8501
3. **Entraîner un modèle** via le frontend
4. **Faire des prédictions**
5. **Voir l'historique**

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime
from train import train_model
from predict import Predictor

app = Flask(__name__)
CORS(app)

# Configuration
DATA_PATH = os.getenv('DATA_PATH', '/data/wine_quality.csv')
MODEL_DIR = os.getenv('MODEL_DIR', '/models')
DB_URL = os.getenv('DATABASE_URL')

predictor = Predictor(MODEL_DIR)

def get_db():
    return psycopg2.connect(DB_URL)

def init_db():
    """Initialiser la base de données"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_runs (
            id SERIAL PRIMARY KEY,
            accuracy FLOAT,
            n_samples INTEGER,
            n_features INTEGER,
            model_path TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            features JSONB,
            prediction INTEGER,
            confidence FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/train', methods=['POST'])
def train():
    """Entraîner un nouveau modèle"""
    try:
        data = request.json or {}
        n_estimators = data.get('n_estimators', 100)

        # Entraîner
        result = train_model(DATA_PATH, MODEL_DIR, n_estimators)

        # Sauvegarder dans la DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO training_runs (accuracy, n_samples, n_features, model_path)
            VALUES (%s, %s, %s, %s)
        ''', (result['accuracy'], result['n_samples'], result['n_features'], result['model_path']))
        conn.commit()
        cursor.close()
        conn.close()

        # Recharger le modèle
        predictor.load_latest_model()

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Faire une prédiction"""
    try:
        data = request.json
        features = data['features']

        # Prédire
        result = predictor.predict(features)

        # Sauvegarder dans la DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (features, prediction, confidence)
            VALUES (%s, %s, %s)
        ''', (str(features), result['prediction'], result['confidence']))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/models')
def models():
    """Lister les modèles disponibles"""
    try:
        models_list = predictor.list_models()
        return jsonify({
            'success': True,
            'models': models_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/history/training')
def training_history():
    """Historique des entraînements"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM training_runs ORDER BY timestamp DESC LIMIT 20')
        runs = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'runs': [
                {
                    'id': r[0],
                    'accuracy': r[1],
                    'n_samples': r[2],
                    'n_features': r[3],
                    'timestamp': r[5].isoformat()
                }
                for r in runs
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/history/predictions')
def prediction_history():
    """Historique des prédictions"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 50')
        preds = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'predictions': [
                {
                    'id': p[0],
                    'prediction': p[2],
                    'confidence': p[3],
                    'timestamp': p[4].isoformat()
                }
                for p in preds
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Initialisation de l'API...")
    init_db()
    print("Base de données initialisée")

    try:
        predictor.load_latest_model()
    except FileNotFoundError:
        print("Aucun modèle trouvé. Entraînez-en un via /train")

    app.run(host='0.0.0.0', port=5000, debug=True)
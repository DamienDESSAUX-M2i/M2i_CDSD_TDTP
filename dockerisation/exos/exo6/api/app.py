import os
from datetime import datetime

import database as db
import joblib
import train
from flask import Flask, jsonify, request
from flask_cors import CORS

import numpy as np

app = Flask(__name__)
CORS(app)  # Nécessaire pour que Streamlit puisse appeler l'API

# Configuration des chemins
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/model.pkl")
DATA_PATH = os.getenv("DATA_PATH", "/app/data/wine_data.csv")

# Initialiser la base de données au démarrage
db.init_database()


@app.route("/health", methods=["GET"])
def health():
    """Healthcheck - appelé par la sidebar de Streamlit pour vérifier la connexion"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/train", methods=["POST"])
def train_model_endpoint():
    """
    Entraîner un nouveau modèle
    Appelé depuis l'onglet Entraînement de Streamlit
    """
    try:
        # TODO: Récupérer n_estimators depuis request.json (défaut: 100)
        if not request.is_json:
            return jsonify({"success": False, "error": "JSON required"}), 400

        data = request.get_json()

        n_estimators = 100
        try:
            n_estimators = int(data.get("n_estimators", "100"))
        except Exception:
            pass

        # TODO: Appeler train.train_model() pour entraîner
        metrics = train.train_model(DATA_PATH, MODEL_PATH, n_estimators)

        # TODO: Sauvegarder dans la DB avec db.save_training_run()
        db.save_training_run(
            model_type="random_forest",
            accuracy=metrics["accuracy"],
            n_samples=metrics["n_samples"],
        )

        # Retourner les résultats pour Streamlit
        return jsonify(
            {
                "success": True,
                "accuracy": metrics["accuracy"],  # TODO: mettre l'accuracy du résultat
                "n_samples": metrics["n_samples"],  # TODO: mettre n_samples du résultat
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Faire une prédiction
    Appelé depuis l'onglet Prédiction de Streamlit avec les 11 caractéristiques
    """
    try:
        # Vérifier que le modèle existe
        if not os.path.exists(MODEL_PATH):
            return jsonify(
                {"success": False, "error": "Model not found. Please train first."}
            ), 404

        # TODO: Charger le modèle avec joblib.load()
        model = joblib.load(MODEL_PATH)

        # Récupérer les features depuis Streamlit (format attendu par l'app Streamlit)
        data = request.json
        features = {
            "fixed_acidity": float(data["fixed_acidity"]),
            "volatile_acidity": float(data["volatile_acidity"]),
            "citric_acid": float(data["citric_acid"]),
            "residual_sugar": float(data["residual_sugar"]),
            "chlorides": float(data["chlorides"]),
            "free_sulfur_dioxide": float(data["free_sulfur_dioxide"]),
            "total_sulfur_dioxide": float(data["total_sulfur_dioxide"]),
            "density": float(data["density"]),
            "pH": float(data["pH"]),
            "sulphates": float(data["sulphates"]),
            "alcohol": float(data["alcohol"]),
        }

        # TODO: Faire la prédiction avec model.predict()
        x_new = np.array(
            [
                features["fixed_acidity"],
                features["volatile_acidity"],
                features["citric_acid"],
                features["residual_sugar"],
                features["chlorides"],
                features["free_sulfur_dioxide"],
                features["total_sulfur_dioxide"],
                features["density"],
                features["pH"],
                features["sulphates"],
                features["alcohol"],
            ]
        )
        x_new = x_new.reshape(1, -1)
        y_pred = int(model.predict(x_new)[0])

        # TODO: Sauvegarder dans la DB avec db.save_prediction()
        db.save_prediction(features, y_pred)

        # Retourner le résultat pour Streamlit
        return jsonify(
            {
                "success": True,
                "prediction": y_pred,  # TODO: mettre la vraie prédiction
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/history", methods=["GET"])
def history():
    """
    Récupérer l'historique des prédictions
    Appelé depuis l'onglet Historique de Streamlit
    """
    try:
        # TODO: Récupérer les prédictions avec db.get_recent_predictions(limit=20)
        predictions = db.get_recent_predictions(limit=20)

        # Formater pour Streamlit (attend: id, quality, timestamp)
        return jsonify(
            {
                "success": True,
                "predictions": [
                    # TODO: formater chaque prédiction p en dictionnaire
                    # {'id': p[0], 'quality': p[12], 'timestamp': p[13].isoformat()}
                    {"id": p[0], "quality": p[12], "timestamp": p[13].isoformat()}
                    for p in predictions
                ],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Récupérer les métriques d'entraînement
    Appelé depuis l'onglet Métriques de Streamlit
    """
    try:
        # TODO: Récupérer les runs avec db.get_training_history()
        trainings = db.get_training_history()

        # Formater pour Streamlit (attend: id, model_type, accuracy, n_samples, timestamp)
        return jsonify(
            {
                "success": True,
                "training_runs": [
                    # TODO: formater chaque training run t en dictionnaire
                    # {'id': t[0], 'model_type': t[1], 'accuracy': t[2], 'n_samples': t[3], 'timestamp': t[4].isoformat()}
                    {
                        "id": t[0],
                        "model_type": t[1],
                        "accuracy": t[2],
                        "n_samples": t[3],
                        "timestamp": t[4].isoformat(),
                    }
                    for t in trainings
                ],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

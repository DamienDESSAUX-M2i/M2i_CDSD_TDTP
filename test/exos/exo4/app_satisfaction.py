"""
API Flask pour la prédiction de satisfaction client

Cette API permet de :
- Vérifier la santé de l'API
- Faire des prédictions de satisfaction client (1-10)
- Faire des prédictions batch
- Consulter l'historique des prédictions
"""

import pickle
from datetime import datetime

from flask import Flask, jsonify, request

import numpy as np

app = Flask(__name__)

# Chargement du modèle
try:
    with open("satisfaction_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print(
        "Attention: satisfaction_model.pkl non trouvé. Exécutez train_satisfaction_model.py d'abord."
    )

# Stockage en mémoire de l'historique
prediction_history = []


@app.route("/health", methods=["GET"])
def health():
    """
    Endpoint de santé de l'API

    Retourne:
        JSON avec le statut de l'API et du modèle
    """
    return jsonify(
        {
            "status": "ok",
            "model_loaded": model is not None,
            "timestamp": datetime.now().isoformat(),
        }
    ), 200


@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint de prédiction simple

    Payload JSON attendu:
    {
        "features": [age, temps_abonnement, nb_interactions, nb_reclamations]
    }

    Retourne:
        JSON avec la satisfaction prédite (1-10)
    """
    data = request.get_json()

    # Validation
    if "features" not in data:
        return jsonify({"error": 'Le champ "features" est requis'}), 400

    features = data["features"]

    if not isinstance(features, list):
        return jsonify({"error": "features doit être une liste"}), 400

    if len(features) != 4:
        return jsonify({"error": "features doit contenir exactement 4 valeurs"}), 400

    # Vérification que ce sont des nombres
    try:
        features = [float(f) for f in features]
    except (ValueError, TypeError):
        return jsonify({"error": "Toutes les features doivent être des nombres"}), 400

    if model is None:
        return jsonify({"error": "Modèle non chargé"}), 500

    try:
        # Prédiction
        features_array = np.array([features])
        prediction = model.predict(features_array)[0]

        # Arrondir à 1 décimale
        satisfaction = round(float(prediction), 1)

        # Sauvegarder dans l'historique
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "features": features,
            "satisfaction": satisfaction,
            "type": "single",
        }
        prediction_history.append(history_entry)

        return jsonify(
            {"satisfaction": satisfaction, "timestamp": history_entry["timestamp"]}
        ), 200

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la prédiction: {str(e)}"}), 500


@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    """
    Endpoint de prédiction batch

    Payload JSON attendu:
    {
        "features_list": [
            [age1, temps_abonnement1, nb_interactions1, nb_reclamations1],
            [age2, temps_abonnement2, nb_interactions2, nb_reclamations2],
            ...
        ]
    }

    Retourne:
        JSON avec les satisfactions prédites
    """
    data = request.get_json()

    # Validation
    if "features_list" not in data:
        return jsonify({"error": 'Le champ "features_list" est requis'}), 400

    features_list = data["features_list"]

    if not isinstance(features_list, list):
        return jsonify({"error": "features_list doit être une liste"}), 400

    if len(features_list) == 0:
        return jsonify({"error": "features_list ne peut pas être vide"}), 400

    # Validation de chaque entrée
    for i, features in enumerate(features_list):
        if not isinstance(features, list):
            return jsonify({"error": f"L'entrée {i} doit être une liste"}), 400

        if len(features) != 4:
            return jsonify(
                {"error": f"L'entrée {i} doit contenir exactement 4 valeurs"}
            ), 400

        try:
            [float(f) for f in features]
        except (ValueError, TypeError):
            return jsonify(
                {"error": f"L'entrée {i} contient des valeurs non numériques"}
            ), 400

    if model is None:
        return jsonify({"error": "Modèle non chargé"}), 500

    try:
        # Conversion et prédiction
        features_array = np.array(
            [[float(f) for f in features] for features in features_list]
        )
        predictions = model.predict(features_array)

        # Arrondir à 1 décimale
        satisfactions = [round(float(p), 1) for p in predictions]

        # Sauvegarder dans l'historique
        timestamp = datetime.now().isoformat()
        for features, satisfaction in zip(features_list, satisfactions):
            history_entry = {
                "timestamp": timestamp,
                "features": features,
                "satisfaction": satisfaction,
                "type": "batch",
            }
            prediction_history.append(history_entry)

        return jsonify(
            {
                "satisfactions": satisfactions,
                "count": len(satisfactions),
                "timestamp": timestamp,
            }
        ), 200

    except Exception as e:
        return jsonify({"error": f"Erreur lors de la prédiction batch: {str(e)}"}), 500


@app.route("/history", methods=["GET"])
def history():
    """
    Endpoint pour consulter l'historique des prédictions

    Paramètres query:
        - limit: nombre maximum de résultats (défaut: 10, max: 100)

    Retourne:
        JSON avec l'historique des prédictions
    """
    try:
        # Récupérer le paramètre limit
        limit = request.args.get("limit", default=10, type=int)

        # Valider limit
        if limit < 1:
            return jsonify({"error": "limit doit être >= 1"}), 400

        if limit > 100:
            return jsonify({"error": "limit ne peut pas dépasser 100"}), 400

        # Retourner les dernières prédictions
        history_slice = prediction_history[-limit:]

        return jsonify(
            {
                "history": history_slice,
                "total": len(prediction_history),
                "returned": len(history_slice),
            }
        ), 200

    except Exception as e:
        return jsonify(
            {"error": f"Erreur lors de la récupération de l'historique: {str(e)}"}
        ), 500


@app.route("/stats", methods=["GET"])
def stats():
    """
    Endpoint pour obtenir des statistiques sur les prédictions

    Retourne:
        JSON avec des statistiques globales
    """
    if len(prediction_history) == 0:
        return jsonify(
            {"total_predictions": 0, "message": "Aucune prédiction disponible"}
        ), 200

    satisfactions = [entry["satisfaction"] for entry in prediction_history]

    return jsonify(
        {
            "total_predictions": len(prediction_history),
            "average_satisfaction": round(np.mean(satisfactions), 2),
            "min_satisfaction": round(min(satisfactions), 1),
            "max_satisfaction": round(max(satisfactions), 1),
            "std_satisfaction": round(np.std(satisfactions), 2),
        }
    ), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)

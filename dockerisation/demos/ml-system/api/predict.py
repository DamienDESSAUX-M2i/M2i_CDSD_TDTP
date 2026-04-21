import joblib
import numpy as np
import os

class Predictor:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.model = None

    def load_latest_model(self):
        """Charger le modèle le plus récent"""
        models = [f for f in os.listdir(self.model_dir) if f.endswith('.pkl')]

        if not models:
            raise FileNotFoundError("Aucun modèle trouvé. Entraînez d'abord un modèle.")

        latest_model = sorted(models)[-1]
        model_path = os.path.join(self.model_dir, latest_model)

        self.model = joblib.load(model_path)
        print(f"Modèle chargé: {latest_model}")

        return latest_model

    def predict(self, features):
        """Faire une prédiction"""
        if self.model is None:
            self.load_latest_model()

        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]

        return {
            'prediction': int(prediction),
            'confidence': float(max(probabilities))
        }

    def list_models(self):
        """Lister tous les modèles disponibles"""
        models = [f for f in os.listdir(self.model_dir) if f.endswith('.pkl')]
        return sorted(models, reverse=True)
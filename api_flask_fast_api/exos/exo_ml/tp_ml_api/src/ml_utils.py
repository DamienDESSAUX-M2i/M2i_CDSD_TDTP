"""Chargement du modèle ML et inférence."""

import json
import pickle
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np


class MLModel:
    """Wrapper autour du modèle scikit-learn."""

    def __init__(self, model_path: str):
        self.model = None
        self.classes = ["setosa", "versicolor", "virginica"]
        self.report: Optional[dict] = None
        self.load_model(model_path)

    def load_model(self, model_path: str) -> None:
        """Charge le modèle depuis un fichier pickle."""
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Fichier modèle introuvable : {model_path}")

        with open(path, "rb") as f:
            self.model = pickle.load(f)

        # Charger le rapport JSON si disponible
        report_path = path.parent / "training_report.json"
        if report_path.exists():
            with open(report_path, "r") as f:
                self.report = json.load(f)

    def predict(self, features: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """
        Retourne (classe_prédite, confiance, dict_probabilités).

        Raises:
            RuntimeError: si le modèle n'est pas chargé.
        """
        if self.model is None:
            raise RuntimeError("Le modèle n'est pas chargé.")

        prediction_idx = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]

        prediction_class = self.classes[prediction_idx]
        confidence = float(probabilities[prediction_idx])
        probs_dict = {
            self.classes[i]: float(probabilities[i])
            for i in range(len(self.classes))
        }

        return prediction_class, confidence, probs_dict

    def get_accuracy(self) -> Optional[float]:
        """Retourne l'accuracy issue du rapport d'entraînement."""
        if self.report:
            return self.report.get("accuracy")
        return None

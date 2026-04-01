"""
Script d'entraînement du modèle Iris.

Exécution :
    python scripts/train.py
"""

import pickle
import os
import json
import logging
from datetime import datetime

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def train_model():
    """Pipeline d'entraînement complet."""

    # 1. Charger les données
    logger.info("Chargement du dataset Iris...")
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 2. Splitter
    logger.info("Split 80/20 stratifié...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Entraîner
    logger.info("Entraînement du RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # 4. Évaluer
    logger.info("Évaluation du modèle...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    logger.info(f"Accuracy : {accuracy:.4f}")
    logger.info(f"F1-Score : {f1:.4f}")

    # 5. Sauvegarder le modèle
    os.makedirs("models", exist_ok=True)
    model_path = "models/iris_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"Modèle sauvegardé dans {model_path}")

    # 6. Générer le rapport JSON
    report = {
        "trained_at": datetime.now().isoformat(),
        "accuracy": float(accuracy),
        "f1_score": float(f1),
        "n_samples_train": len(X_train),
        "n_samples_test": len(X_test),
        "n_classes": len(iris.target_names),
        "classes": iris.target_names.tolist(),
        "features": list(iris.feature_names),
        "feature_importance": {
            iris.feature_names[i]: float(model.feature_importances_[i])
            for i in range(len(iris.feature_names))
        },
        "classification_report": classification_report(
            y_test, y_pred, target_names=iris.target_names, output_dict=True
        ),
    }

    report_path = "models/training_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Rapport sauvegardé dans {report_path}")

    return model, report


if __name__ == "__main__":
    train_model()

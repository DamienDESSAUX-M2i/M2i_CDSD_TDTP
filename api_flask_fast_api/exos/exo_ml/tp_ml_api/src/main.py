"""Application FastAPI — API de classification Iris."""

import logging

import numpy as np
from fastapi import FastAPI, HTTPException, status

from src.config import get_settings
from src.ml_utils import MLModel
from src.models import HealthResponse, PredictionInput, PredictionOutput

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Iris API",
    description="API production-ready pour la classification de fleurs Iris.",
    version="1.0.0",
)

# État global
ml_model: MLModel | None = None


@app.on_event("startup")
async def startup_event() -> None:
    """Charge le modèle ML au démarrage de l'application."""
    global ml_model
    try:
        settings = get_settings()
        ml_model = MLModel(settings.model_path)
        logger.info("Modèle chargé avec succès.")
    except Exception as e:
        logger.error(f"Impossible de charger le modèle : {e}")


@app.get("/health", response_model=HealthResponse)
async def health_check() -> dict:
    """Vérifie l'état de l'API et du modèle."""
    if ml_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé.",
        )
    return {
        "status": "healthy",
        "model_loaded": True,
        "accuracy": ml_model.get_accuracy(),
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput) -> dict:
    """Effectue une prédiction à partir des mesures de la fleur."""
    if ml_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé.",
        )
    try:
        features = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width,
        ]])
        prediction, confidence, probabilities = ml_model.predict(features)
        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
        }
    except Exception as e:
        logger.error(f"Erreur d'inférence : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Échec de la prédiction.",
        )


@app.get("/info")
async def model_info() -> dict:
    """Retourne les métadonnées du modèle entraîné."""
    if ml_model is None or ml_model.report is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Informations du modèle non disponibles.",
        )
    return {
        "model_type": "RandomForestClassifier",
        "accuracy": ml_model.report.get("accuracy"),
        "f1_score": ml_model.report.get("f1_score"),
        "classes": ml_model.report.get("classes"),
        "features": ml_model.report.get("features"),
        "trained_at": ml_model.report.get("trained_at"),
    }

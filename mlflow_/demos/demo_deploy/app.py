import logging
import os
from typing import List

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configuration
app = FastAPI(title="IRIS prediction API", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Charger modèle
MODEL_NAME = os.getenv("MODEL_NAME", "iris-api-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")

try:
    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
    logger.info(f"Modèle chargé: {MODEL_NAME}")
except Exception as e:
    logger.error(f"Erreur : {e}")
    model = None


# Schémas Pydantic
class PredictionRequest(BaseModel):
    instances: List[List[float]]

    class Config:
        schema_extra = {
            "exemple": {"instances": [[5.1, 3.5, 1.4, 0.2], [5.0, 4.5, 2.0, 0.2]]}
        }


class PredictionResponse(BaseModel):
    predictions: List[int]


class HealthResponse(BaseModel):
    status: str
    model: str
    stage: str


@app.get("/")
def root():
    return {"message": "API Iris", "docs": "/docs", "health": "/health"}


@app.get("/health", response_model=HealthResponse)
def health():
    status = "healthy" if model is not None else "unhealthy"
    return {"status": status, "model": MODEL_NAME, "stage": MODEL_STAGE}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model non chargé")

    try:
        df = pd.DataFrame(request.instances)
        predictions = model.predict(df)
        logger.info(f"Prédiction pour {len(df)} échantillons")

        return {"predictions": predictions.tolist()}

    except Exception as e:
        logger.error(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

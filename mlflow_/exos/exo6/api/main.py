import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from model_loader import ModelLoader
from schemas import HealthResponse, PredictionRequest, PredictionResponse, RiskLevel

REGISTERED_MODEL_NAME = os.getenv("REGISTRY_MODEL_NAME", "predictive-maintenance-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Metrics:
    def __init__(self):
        self.total_predictions = 0
        self.failure_predictions = 0

    def update(self, preds):
        self.total_predictions += len(preds)
        self.failure_predictions += sum(preds)

    def to_dict(self):
        rate = (
            self.failure_predictions / self.total_predictions
            if self.total_predictions > 0
            else 0
        )
        return {
            "total_predictions": self.total_predictions,
            "failure_predictions": self.failure_predictions,
            "failure_rate": rate,
        }


def probabilities_to_risk(p: float) -> RiskLevel:
    if p < 0.2:
        return RiskLevel.LOW
    elif p < 0.5:
        return RiskLevel.MEDIUM
    elif p < 0.75:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


def get_model_loader(app: FastAPI) -> ModelLoader:
    return app.state.model_loader


def get_metrics(app: FastAPI) -> Metrics:
    return app.state.metrics


ModelDep = Annotated[ModelLoader, Depends(get_model_loader)]
MetricsDep = Annotated[Metrics, Depends(get_metrics)]


def predict_internal(model: ModelLoader, metrics: Metrics, df: pd.DataFrame):
    preds = model.predict(df)
    probas = model.predict_proba(df)[:, 1]

    risks = [probabilities_to_risk(p) for p in probas]

    metrics.update(preds)

    return preds.tolist(), risks


def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Loading model...")

        app.state.model_loader = ModelLoader()
        app.state.metrics = Metrics()

        if not app.state.model_loader.is_loaded:
            logger.error("Model failed to load")
        else:
            logger.info("Model loaded successfully")

        yield

        logger.info("Shutting down API")

    app = FastAPI(
        title="Predictive Maintenance API", version="1.0.0", lifespan=lifespan
    )

    @app.get("/health", response_model=HealthResponse)
    def health(model: ModelDep):
        status = "healthy" if model.is_loaded else "unhealthy"

        return {"status": status, "model": REGISTERED_MODEL_NAME, "stage": MODEL_STAGE}

    @app.get("/metrics")
    def metrics(metrics: MetricsDep):
        return metrics.to_dict()

    @app.post("/predict", response_model=PredictionResponse)
    def predict(request: PredictionRequest, model: ModelDep, metrics: MetricsDep):
        if not model.is_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")

        try:
            df = pd.DataFrame([r.model_dump() for r in request.instances])

            preds, risks = predict_internal(model, metrics, df)

            return {"predictions": preds, "risks_levels": risks}

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/predict/batch", response_model=PredictionResponse)
    def predict_batch(request: PredictionRequest, model: ModelDep, metrics: MetricsDep):
        if not model.is_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")

        if len(request.instances) > 100:
            raise HTTPException(status_code=400, detail="Max batch size is 100")

        try:
            df = pd.DataFrame([r.model_dump() for r in request.instances])

            preds, risks = predict_internal(model, metrics, df)

            return {"predictions": preds, "risks_levels": risks}

        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    return app


app = create_app()

import os
import time
import logging
from contextlib import asynccontextmanager
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from schemas import PredictionRequest, PredictionResponse, HealthResponse, MetricsResponse
from model_loader import model_loader

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

START_TIME = time.time()
counters = {"total_predictions": 0, "failure_predictions": 0}
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Demarrage de l'API - chargement du modele...")
    model_loader.load()
    if model_loader.is_loaded:
        logger.info(f"Modele pret (version {model_loader.version})")
    else:
        logger.warning("Modele non charge")
    yield
    logger.info("Arret de l'API")

app = FastAPI(
    title="Predictive Maintenance API",
    description=(
        "Predit la defaillance imminente d'une machine CNC "
        "a partir de ses donnees capteurs (dataset AI4I 2020)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# utils
def build_dataframe(req: PredictionRequest) -> pd.DataFrame:
    data = {
        "type": [req.type],
        "air_temperature": [req.air_temperature],
        "process_temperature": [req.process_temperature],
        "rotational_speed": [req.rotational_speed],
        "torque": [req.torque],
        "tool_wear": [req.tool_wear],
    }
    df = pd.DataFrame(data)
    df["temp_delta"] = df["process_temperature"] - df["air_temperature"]
    df["power_proxy"] = df["rotational_speed"] * df["torque"]
    df["wear_per_rpm"] = df["tool_wear"] / (df["rotational_speed"] + 1e-6)
    return df


def compute_risk_level(probability: float) -> tuple[str, str]:

    if probability < 0.2:
        return "LOW", "Aucune action requise. Prochaine inspection planifiee."
    if probability < 0.5:
        return "MEDIUM", "Surveiller de pres. Planifier une inspection preventive."
    if probability < 0.75:
        return "HIGH", "Inspection recommandee dans les 24h. Reduire la cadence."
    return "CRITICAL", "Arret immediat recommande. Maintenance urgente requise."


def _assert_model_ready() -> None:
    if not model_loader.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modele non disponible. Verifiez MLflow et relancez l'API.",
        )


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
async def health():
    return HealthResponse(
        status="healthy" if model_loader.is_loaded else "degraded",
        model_loaded=model_loader.is_loaded,
        model_version=model_loader.version,
        mlflow_uri=MLFLOW_URI,
    )


@app.get("/metrics", response_model=MetricsResponse, tags=["Monitoring"])
async def metrics():
    total = counters["total_predictions"]
    failures = counters["failure_predictions"]
    return MetricsResponse(
        total_predictions=total,
        failure_predictions=failures,
        failure_rate=round(failures / total, 4) if total > 0 else 0.0,
        uptime_seconds=round(time.time() - START_TIME, 1),
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    _assert_model_ready()

    try:
        df = build_dataframe(request)
        failure_proba = float(model_loader.predict_proba(df)[0])
        is_failure = failure_proba >= 0.5
        risk_level, recommendation = compute_risk_level(failure_proba)

        counters["total_predictions"] += 1
        if is_failure:
            counters["failure_predictions"] += 1

        logger.info(
            "Prediction : failure=%s | proba=%.3f | risk=%s | type=%s",
            is_failure, failure_proba, risk_level, request.type,
        )

        return PredictionResponse(
            machine_failure=is_failure,
            failure_probability=round(failure_proba, 4),
            risk_level=risk_level,
            recommendation=recommendation,
            model_version=model_loader.version,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Erreur lors de la prediction : %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur de prediction : {exc}",
        )


@app.post("/predict/batch", response_model=List[PredictionResponse], tags=["Prediction"])
async def predict_batch(requests: List[PredictionRequest]):
    _assert_model_ready()

    if len(requests) > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Maximum 100 predictions par appel batch.",
        )

    results = []
    for req in requests:
        df = build_dataframe(req)
        failure_proba = float(model_loader.predict_proba(df)[0])
        is_failure = failure_proba >= 0.5
        risk_level, recommendation = compute_risk_level(failure_proba)

        counters["total_predictions"] += 1
        if is_failure:
            counters["failure_predictions"] += 1

        results.append(PredictionResponse(
            machine_failure=is_failure,
            failure_probability=round(failure_proba, 4),
            risk_level=risk_level,
            recommendation=recommendation,
            model_version=model_loader.version,
        ))

    return results


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Predictive Maintenance API - voir /docs"}

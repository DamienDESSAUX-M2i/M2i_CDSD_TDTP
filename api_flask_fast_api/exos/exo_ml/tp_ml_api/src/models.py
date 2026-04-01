"""Modèles Pydantic pour l'API Iris."""

from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class IrisClass(str, Enum):
    SETOSA = "setosa"
    VERSICOLOR = "versicolor"
    VIRGINICA = "virginica"


class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=0)
    sepal_width: float = Field(..., gt=0)
    petal_length: float = Field(..., gt=0)
    petal_width: float = Field(..., ge=0)


class PredictionOutput(BaseModel):
    prediction: IrisClass
    confidence: float = Field(..., ge=0, le=1)
    probabilities: Dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    accuracy: Optional[float] = None

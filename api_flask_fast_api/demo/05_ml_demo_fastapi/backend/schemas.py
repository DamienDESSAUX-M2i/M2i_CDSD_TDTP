from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=1000)


class PredictionResponse(BaseModel):
    id: int
    first_name: str
    text: str
    predicted_label: str
    confidence: float
    all_scores: Dict[str, float]
    created_at: datetime


class PredictionHistoryItem(BaseModel):
    id: int
    first_name: str
    message: str
    predicted_label: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True

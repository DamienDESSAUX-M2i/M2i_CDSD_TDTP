from pydantic import BaseModel, Field
from typing import Literal


class PredictionRequest(BaseModel):
    type: Literal["L", "M", "H"] = Field(
        ...,
        description="Qualite du produit fabrique : L=Low, M=Medium, H=High",
    )
    air_temperature: float = Field(
        ..., ge=295.0, le=305.0,
        description="Temperature ambiante en Kelvin",
    )
    process_temperature: float = Field(
        ..., ge=305.0, le=315.0,
        description="Temperature du process en Kelvin",
    )
    rotational_speed: float = Field(
        ..., ge=1168.0, le=2886.0,
        description="Vitesse de rotation en RPM",
    )
    torque: float = Field(
        ..., ge=3.8, le=76.6,
        description="Couple moteur en Nm",
    )
    tool_wear: float = Field(
        ..., ge=0.0, le=253.0,
        description="Duree d'usure outil en minutes",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "M",
                "air_temperature": 298.1,
                "process_temperature": 308.6,
                "rotational_speed": 1551,
                "torque": 42.8,
                "tool_wear": 0,
            }
        }
    }


class PredictionResponse(BaseModel):
    machine_failure: bool = Field(..., description="True si panne predite")
    failure_probability: float = Field(..., description="Probabilite de panne (0-1)")
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        ..., description="Niveau de risque calcule selon les seuils metier",
    )
    recommendation: str = Field(..., description="Action recommandee")
    model_version: str = Field(..., description="Version du modele utilise")


class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    model_loaded: bool
    model_version: str
    mlflow_uri: str


class MetricsResponse(BaseModel):
    total_predictions: int
    failure_predictions: int
    failure_rate: float
    uptime_seconds: float

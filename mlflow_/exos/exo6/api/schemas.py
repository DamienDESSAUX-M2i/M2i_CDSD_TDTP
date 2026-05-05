from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class MachineFeatures(BaseModel):
    type: Literal["L", "M", "H"] = Field(..., description="Product type")
    air_temperature: float = Field(..., description="Air temperature (K)", gt=0)
    process_temperature: float = Field(..., description="Process temperature (K)", gt=0)
    rotational_speed: float = Field(..., description="Rotational speed (rpm)", gt=0)
    torque: float = Field(..., description="Torque (Nm)")
    tool_wear: float = Field(..., description="Tool wear (min)", ge=0)


class PredictionRequest(BaseModel):
    instances: list[MachineFeatures]

    model_config = {
        "json_schema_extra": {
            "example": {
                "instances": [
                    {
                        "type": "M",
                        "air_temperature": 298.1,
                        "process_temperature": 308.6,
                        "rotational_speed": 1551,
                        "torque": 42.8,
                        "tool_wear": 0,
                    }
                ]
            }
        }
    }


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PredictionResponse(BaseModel):
    predictions: list[int] = Field(..., description="Predicted class (0 or 1)")
    risks_levels: list[RiskLevel] = Field(..., description="Risk level")


class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    model: str = Field(..., description="Model name")
    stage: Literal["None", "Staging", "Production", "Archived"]

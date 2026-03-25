from datetime import datetime, timezone
from typing import Generic, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(
        ...,
        title="Success",
        description="APIResponse's success",
        example=True,
    )
    data: T = Field(
        ...,
        title="Data",
        description="APIResponse's data",
        example={},
    )
    message: str = Field(
        ...,
        title="Message",
        description="APIResponse's message",
        example="message",
    )
    timestamp: datetime = Field(
        ...,
        title="Timestamp",
        description="APIResponse's timestamp",
        example=datetime.now(timezone.utc),
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "success": True,
                "data": {},
                "message": "message",
                "timestamp": datetime.now(timezone.utc),
            }
        }
    }


class Model1(BaseModel):
    attribute: int


class Model2(BaseModel):
    attribute: str


router = APIRouter(prefix="/generic", tags=["generic"])


@router.post("/model1", response_model=ApiResponse[Model1], status_code=201)
def create_model1(model: Model1):
    return ApiResponse(
        success=True,
        data=model,
        message="Model1 created",
        timestamp=datetime.now(timezone.utc),
    )


@router.post("/model2", response_model=ApiResponse[Model2], status_code=201)
def create_model2(model: Model2):
    return ApiResponse(
        success=True,
        data=model,
        message="Model2 created",
        timestamp=datetime.now(timezone.utc),
    )

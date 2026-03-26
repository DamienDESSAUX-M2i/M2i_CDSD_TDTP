from datetime import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(..., description="Succès de l'opération")
    data: Optional[T] = Field(None, description="Données de réponse")
    message: str = Field(..., description="Message descriptif")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": None,
                "message": "Operation completed successfully",
                "timestamp": "2024-01-01T10:00:00"
            }
        }
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    is_active: bool = True
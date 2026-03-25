from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, description="Username unique")
    email: EmailStr = Field(..., description="Email valide")
    age: Optional[int] = Field(None, ge=0, le=150, description="Age optionnel")
    is_active: bool = Field(True, description="Utilisateur actif par défaut")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "age": 25,
                "is_active": True
            }
        }
    )


class User(UserCreate):
    id: int = Field(..., description="ID unique auto-généré")
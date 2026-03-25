from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator, model_validator


class Password(BaseModel):
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")

    @field_validator("password")
    def validate_password(cls, v):
        if not any(c.islower() for c in v):
            raise ValueError("Must contain a lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain a digit")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Must contain a symbol")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self):
        """
        Root validator - validate across multiple fields
        Checks that password and confirm_password match
        """
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


passwords_db = {}
next_password_id = 1

router = APIRouter(prefix="/passwords", tags=["passwords"])


@router.post("/", response_model=Password, status_code=201)
def create_password(password: Password):
    """Create new password with automatic validation"""
    global next_password_id

    new_password = {
        "id": next_password_id,
        "password": password.password,
        "confirm_password": password.confirm_password,
        "created_at": datetime.now().isoformat() + "Z",
    }

    passwords_db[next_password_id] = new_password
    next_password_id += 1

    return new_password

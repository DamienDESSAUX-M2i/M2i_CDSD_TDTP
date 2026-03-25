from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
import re


class PasswordValidation(BaseModel):
    password: str = Field(..., min_length=8, description="Mot de passe sécurisé")
    confirm_password: str = Field(..., description="Confirmation du mot de passe")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!"
            }
        }
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")

        special_chars = r"""[!@#$%^&*(),.?":{}|<>\-_=+\[\]\\;:'"]"""
        if not re.search(special_chars, v):
            raise ValueError("Password must contain at least one special character")

        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
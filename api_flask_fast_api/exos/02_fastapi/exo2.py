from datetime import datetime

import uvicorn
from fastapi import FastAPI
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

app = FastAPI(title="Mon API", version="1.0.0")


@app.post("/passwords", response_model=Password, status_code=201, tags=["passwords"])
def create_password(password: Password):
    """
    Create new password with automatic validation
    """
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


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)

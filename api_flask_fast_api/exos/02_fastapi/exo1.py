from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int = Field(..., frozen=True, description="User's ID")
    username: str = Field(
        ..., min_length=2, max_length=50, description="User's full name"
    )
    email: EmailStr = Field(..., description="User's email address")
    age: int | None = Field(None, ge=0, le=150, description="User's age (0-150)")
    is_active: bool = Field(default=True, description="Is user active?")


class UserResponse(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=50, description="User's full name"
    )
    email: EmailStr = Field(..., description="User's email address")
    age: int | None = Field(None, ge=0, le=150, description="User's age (0-150)")
    is_active: bool = Field(default=True, description="Is user active?")


users_db = {}
next_user_id = 1

app = FastAPI(title="Mon API", version="1.0.0")


@app.get("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return users_db[user_id]


@app.post("/users", response_model=UserResponse, status_code=201, tags=["Users"])
def create_user(user: UserResponse):
    """
    Create new user with automatic validation
    """
    global next_user_id

    new_user = {
        "id": next_user_id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "is_active": user.is_active,
        "created_at": datetime.now().isoformat() + "Z",
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return new_user


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)

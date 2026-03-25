from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    birthday: datetime = Field(..., le=datetime.now(timezone.utc))
    is_active: bool = True


class User(UserCreate):
    id: int
    created_at: datetime = datetime.now(timezone.utc)


class UserResponse(BaseModel):
    username: str
    age: int

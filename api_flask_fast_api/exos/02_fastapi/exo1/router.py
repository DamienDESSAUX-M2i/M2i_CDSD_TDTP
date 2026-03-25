from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from .db import next_user_id, users_db
from .models import User, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def calculate_age(birthday: datetime) -> int:
    today = datetime.now(timezone.utc)
    return (
        today.year
        - birthday.year
        - ((today.month, today.day) < (birthday.month, birthday.day))
    )


@router.get("/", response_model=list[UserResponse])
def get_all_users():
    result = []

    for user in users_db.values():
        result.append(
            {
                "username": user["username"],
                "age": calculate_age(user["birthday"]),
            }
        )

    return result


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    user = users_db[user_id]

    return {
        "username": user["username"],
        "age": calculate_age(user["birthday"]),
    }


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global next_user_id

    new_user = {
        "id": next_user_id,
        "username": user.username,
        "email": user.email,
        "birthday": user.birthday,
        "is_active": user.is_active,
        "created_at": datetime.now(timezone.utc),
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return new_user

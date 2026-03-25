from fastapi import APIRouter, HTTPException, status
from typing import List

from models.user import UserCreate, User
from db import user_db



router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):


    for existing_user in user_db.users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user.email} already registered"
            )

    user_dict = user.model_dump()
    user_dict["id"] = user_db.next_user_id
    user_db.users_db[user_db.next_user_id] = user_dict
    user_db.next_user_id += 1


    return user_dict


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    if user_id not in user_db.users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user_db.users_db[user_id]


@router.get("", response_model=List[User])
async def list_users():
    return list(user_db.users_db.values())
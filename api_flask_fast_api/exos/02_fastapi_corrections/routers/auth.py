from fastapi import APIRouter

from models.password import PasswordValidation


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/validate-password")
async def validate_password(pwd_model: PasswordValidation):
    return {"message": "Password is valid and secure"}
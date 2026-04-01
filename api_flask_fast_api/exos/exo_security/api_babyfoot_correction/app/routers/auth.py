"""
Routes d'authentification :
- inscription
- connexion
- endpoint /me
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.dependencies.auth import get_current_user
from app.models.schemas import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Crée un nouveau compte utilisateur.
    Le mot de passe est hashé avant l'enregistrement.
    """
    existing_user = db.execute(
        select(User).where(User.username == payload.username)
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Ce username existe déjà")

    user = User(
        username=payload.username,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    """
    Vérifie les identifiants puis renvoie un JWT signé.
    """
    user = db.execute(
        select(User).where(User.username == payload.username)
    ).scalar_one_or_none()

    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )

    token = create_access_token({"sub": str(user.id), "username": user.username})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """
    Permet de tester simplement que le JWT fonctionne.
    """
    return current_user

"""
Endpoints liés à l'authentification :
- inscription
- connexion
- refresh
- logout
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.dependencies.auth import get_current_user
from app.models.schemas import UserRegister, UserLogin, UserPublic, LoginResponse, MessageResponse
from app.models.user import UserRole
from app.services import get_user_by_username, create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.

    Étapes :
    1. vérifier que le username n'existe pas déjà
    2. créer l'utilisateur avec mot de passe hashé
    3. attribuer le rôle 'user' par défaut
    4. retourner seulement les données publiques
    """
    existing_user = get_user_by_username(db, payload.username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce nom d'utilisateur existe déjà.",
        )

    created_user = create_user(
        db=db,
        username=payload.username,
        full_name=payload.full_name,
        password=payload.password,
        role=UserRole.USER.value,
    )

    return created_user


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authentifie l'utilisateur et retourne un JWT si les identifiants sont valides.
    """
    user = get_user_by_username(db, payload.username)

    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
        )

    access_token = create_access_token(
        data={
            "sub": user.username,
            "full_name": user.full_name,
            "role": user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user,
    }


@router.post("/refresh", response_model=LoginResponse)
def refresh(current_user=Depends(get_current_user)):
    """
    Génère un nouveau token pour l'utilisateur déjà authentifié.

    Cette démo reste simple :
    - on ne gère pas de refresh token séparé
    - on redonne simplement un nouveau token d'accès
    """
    access_token = create_access_token(
        data={
            "sub": current_user.username,
            "full_name": current_user.full_name,
            "role": current_user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": current_user,
    }


@router.post("/logout", response_model=MessageResponse)
def logout(current_user=Depends(get_current_user)):
    """
    Simule une déconnexion.

    Dans une vraie application, un logout côté JWT nécessite souvent :
    - une blacklist de tokens
    - ou une durée de vie très courte
    - ou des refresh tokens invalidables

    Ici, on renvoie seulement un message pour expliquer le concept.
    """
    return {"message": f"Déconnexion simulée pour l'utilisateur {current_user.username}."}

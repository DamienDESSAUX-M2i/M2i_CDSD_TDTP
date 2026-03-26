"""
Dépendances liées à l'authentification et aux rôles.
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import UserRole
from app.services import get_user_by_username

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    """
    Récupère l'utilisateur courant à partir du token Bearer.

    Exemple attendu dans l'en-tête HTTP :
        Authorization: Bearer <token>
    """
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide : sujet manquant.",
            )

        user = get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur introuvable.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Utilisateur inactif.",
            )

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide.",
        )


def require_roles(*allowed_roles: UserRole):
    """
    Fabrique une dépendance FastAPI qui refuse l'accès si le rôle courant n'est
    pas dans la liste autorisée.

    Exemple :
        current_user = Depends(require_roles(UserRole.ADMIN))
    """
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Accès refusé. Rôles autorisés : "
                    + ", ".join(role.value for role in allowed_roles)
                ),
            )
        return current_user

    return role_checker

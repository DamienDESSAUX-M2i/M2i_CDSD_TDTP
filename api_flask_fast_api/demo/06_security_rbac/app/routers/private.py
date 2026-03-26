"""
Endpoints protégés : nécessitent un token JWT valide.
Certaines routes exigent aussi un rôle précis.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import UserRole
from app.services import get_all_users, delete_user_by_id

router = APIRouter(prefix="/private", tags=["Private"])


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    return {
        "message": "Vous êtes authentifié.",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "is_active": current_user.is_active,
        },
    }


@router.get("/secret")
def read_secret(current_user=Depends(get_current_user)):
    """
    Exemple de ressource protégée accessible à tout utilisateur authentifié.
    """
    return {
        "message": f"Bonjour {current_user.full_name}, ceci est un endpoint sécurisé.",
        "role": current_user.role,
    }


@router.get("/users")
def list_users(
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.USER)),
    db: Session = Depends(get_db),
):
    """
    Liste tous les utilisateurs.

    Accessible uniquement aux rôles :
    - admin
    - user
    """
    users = get_all_users(db)
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]


@router.get("/admin/users")
def admin_list_users(
    current_user=Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """
    Liste tous les utilisateurs, mais réservé aux administrateurs.
    """
    users = get_all_users(db)
    return {
        "message": f"Bienvenue {current_user.username}, vous êtes administrateur.",
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active,
            }
            for user in users
        ],
    }


@router.delete("/admin/users/{user_id}")
def admin_delete_user(
    user_id: int,
    current_user=Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """
    Supprime un utilisateur par son identifiant.

    Cette route est réservée au rôle admin.
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrateur ne peut pas se supprimer lui-même dans cette démo.",
        )

    deleted_user = delete_user_by_id(db, user_id)
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable.",
        )

    return {
        "message": "Utilisateur supprimé.",
        "deleted_user": {
            "id": deleted_user.id,
            "username": deleted_user.username,
            "role": deleted_user.role,
        },
    }

"""
Schémas Pydantic utilisés pour valider les entrées/sorties de l'API.
"""

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """
    Données attendues pour l'inscription d'un nouvel utilisateur.
    """
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    """
    Données attendues pour la connexion.
    """
    username: str
    password: str


class UserPublic(BaseModel):
    """
    Représentation publique d'un utilisateur.
    Aucun mot de passe ni hash ne doit sortir ici.
    """
    id: int
    username: str
    full_name: str
    role: str
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """
    Réponse renvoyée après un login ou un refresh.
    """
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """
    Petit schéma utilitaire pour les réponses simples.
    """
    message: str


class LoginResponse(TokenResponse):
    """
    Variante un peu plus riche de la réponse de login, pour que l'utilisateur
    sache immédiatement quel compte il vient d'authentifier.
    """
    user: UserPublic
    expires_in: int

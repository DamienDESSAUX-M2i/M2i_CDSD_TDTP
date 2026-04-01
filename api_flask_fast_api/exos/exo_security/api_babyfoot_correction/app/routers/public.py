"""
Endpoints publics de test et d'information.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/ping")
def ping():
    return {"message": "pong"}


@router.get("/info")
def info():
    return {
        "project": "Babyfoot API",
        "description": "API sécurisée de gestion de scores de babyfoot"
    }

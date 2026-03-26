"""
Endpoints publics : pas besoin d'être authentifié.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/ping")
def ping():
    """
    Endpoint de test très simple.
    """
    return {"message": "pong"}


@router.get("/info")
def public_info():
    """
    Endpoint public pour montrer la différence avec les routes protégées.
    """
    return {
        "message": "Ceci est un endpoint public.",
        "hint": "Pour accéder aux routes privées, connectez-vous et envoyez un token Bearer.",
    }


@router.get("/security-info")
def security_info():
    """
    Fournit un résumé simple de ce que montre la démo.
    """
    return {
        "authentication": "JWT Bearer",
        "password_storage": "PBKDF2-HMAC-SHA256",
        "roles": ["admin", "user", "guest"],
        "public_endpoints": ["/public/ping", "/public/info", "/public/security-info", "/auth/login", "/auth/register"],
        "authenticated_endpoints": ["/private/me", "/private/secret", "/auth/refresh", "/auth/logout"],
        "role_protected_endpoints": {
            "admin_or_user": ["/private/users"],
            "admin_only": ["/private/admin/users", "/private/admin/users/{user_id}"],
        },
    }

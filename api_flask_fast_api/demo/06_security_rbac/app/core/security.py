"""
Fonctions de sécurité :
- hash du mot de passe
- vérification du mot de passe
- création du JWT
- lecture du JWT

Important :
Le mot de passe n'est pas chiffré de manière réversible.
Il est hashé, ce qui est le comportement attendu pour un mot de passe.
"""

import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
import jwt

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec PBKDF2-HMAC-SHA256.

    Format stocké :
        pbkdf2_sha256$iterations$salt$hash
    """
    iterations = 100000
    salt = os.urandom(16).hex()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    ).hex()

    return f"pbkdf2_sha256${iterations}${salt}${password_hash}"


def verify_password(password: str, stored_value: str) -> bool:
    """
    Vérifie qu'un mot de passe correspond bien au hash stocké.
    """
    try:
        algorithm_name, iterations_str, salt, stored_hash = stored_value.split("$")
        if algorithm_name != "pbkdf2_sha256":
            return False

        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations_str),
        ).hex()

        return hmac.compare_digest(computed_hash, stored_hash)
    except ValueError:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crée un vrai JWT signé.

    On copie le dictionnaire reçu puis on ajoute une date d'expiration.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Décode et vérifie un JWT.

    Si la signature est invalide ou si le token est expiré, PyJWT lèvera une
    exception que le code appelant pourra gérer.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

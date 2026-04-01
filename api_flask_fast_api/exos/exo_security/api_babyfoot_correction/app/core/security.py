"""
Fonctions de sécurité :
- hash / vérification de mot de passe
- création / validation de JWT
"""

from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec PBKDF2-HMAC-SHA256.
    On stocke :
    pbkdf2_sha256$iterations$salt$hash
    """
    iterations = 100_000
    salt = base64.b64encode(os.urandom(16)).decode("utf-8")
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    encoded_hash = base64.b64encode(password_hash).decode("utf-8")
    return f"pbkdf2_sha256${iterations}${salt}${encoded_hash}"


def verify_password(plain_password: str, stored_password_hash: str) -> bool:
    """
    Vérifie qu'un mot de passe saisi correspond au hash stocké.
    """
    try:
        algorithm_name, iterations_str, salt, encoded_hash = stored_password_hash.split("$")
        if algorithm_name != "pbkdf2_sha256":
            return False

        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations_str),
        )
        computed_encoded_hash = base64.b64encode(computed_hash).decode("utf-8")
        return hmac.compare_digest(computed_encoded_hash, encoded_hash)
    except ValueError:
        return False


def create_access_token(data: dict) -> str:
    """
    Crée un vrai JWT signé.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Décode et valide le JWT.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

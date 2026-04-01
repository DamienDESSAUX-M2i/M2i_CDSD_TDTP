"""
Configuration centrale de l'application.
Dans un vrai projet, ces valeurs seraient plutôt chargées depuis des variables d'environnement.
"""

SECRET_KEY = "change-me-for-a-long-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_URL = "sqlite:///./babyfoot.db"

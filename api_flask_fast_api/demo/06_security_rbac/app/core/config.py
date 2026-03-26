"""
Configuration centrale de l'application.

Dans une vraie application, les secrets et chemins sensibles devraient venir de
variables d'environnement. Ici, tout est volontairement laissé en dur pour que
la démo reste facile à lire.
"""

SECRET_KEY = "change-me-in-real-life-super-secret-key-v5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_PATH = "data/app.db"

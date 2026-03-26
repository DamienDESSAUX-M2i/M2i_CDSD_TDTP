"""
Configuration SQLAlchemy de l'application.

Cette version montre une organisation classique :
- un moteur de base de données
- une session SQLAlchemy
- une base déclarative partagée
- une dépendance FastAPI pour fournir une session aux endpoints
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_PATH

Path("data").mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


def get_db():
    """
    Fournit une session SQLAlchemy à un endpoint FastAPI.

    La session est créée au début de la requête puis fermée à la fin, même en
    cas d'erreur.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

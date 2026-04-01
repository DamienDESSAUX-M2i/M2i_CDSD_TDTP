"""
Initialisation SQLAlchemy :
- moteur SQLite
- session de base de données
- classe Base pour les modèles ORM
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import DATABASE_URL

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dépendance FastAPI qui fournit une session SQLAlchemy
    puis la ferme automatiquement à la fin de la requête.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

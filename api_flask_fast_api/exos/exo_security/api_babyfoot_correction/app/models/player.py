"""
Modèle ORM représentant un joueur de babyfoot.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(80), unique=True, nullable=False, index=True)

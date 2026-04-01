"""
Point d'entrée principal de l'application FastAPI.
On y assemble les routers et on crée les tables au démarrage.
"""

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.user import User
from app.routers import auth, matches, players, public, rankings, teams

app = FastAPI(
    title="Babyfoot API - Correction TP",
    description="Correction complète d'un TP FastAPI avec JWT, SQLite et SQLAlchemy",
    version="1.0.0",
)

app.include_router(public.router)
app.include_router(auth.router)
app.include_router(players.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(rankings.router)


def seed_default_user():
    """
    Crée un compte de démonstration si aucun utilisateur 'admin' n'existe encore.
    """
    db: Session = SessionLocal()
    try:
        existing = db.execute(select(User).where(User.username == "admin")).scalar_one_or_none()
        if existing is None:
            user = User(
                username="admin",
                full_name="Administrateur de démonstration",
                password_hash=hash_password("admin123"),
            )
            db.add(user)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_default_user()

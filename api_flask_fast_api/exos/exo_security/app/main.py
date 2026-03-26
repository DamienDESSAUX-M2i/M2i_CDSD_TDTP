from fastapi import FastAPI

from app.core.database import Base, SessionLocal, get_engine
from app.models.user import UserRole
from app.routers import auth, private, public
from app.schemas.public import RootResponse
from app.services.user import create_user, get_user_by_username

app = FastAPI(
    title="BAB.P.I",
    description="Ex0 security",
    version="1.0.0",
)

engine = get_engine()


def seed_demo_users() -> None:
    """Insère des utilisateurs de démonstration s'ils n'existent pas encore."""
    demo_users = [
        ("alice", "Alice Martin", "azerty123", UserRole.ADMIN.value),
        ("bob", "Bob Durand", "azerty123", UserRole.USER.value),
        ("guest", "Invité Lecture", "azerty123", UserRole.GUEST.value),
    ]

    db = SessionLocal()
    try:
        for username, full_name, raw_password, role in demo_users:
            if not get_user_by_username(db, username):
                create_user(db, username, full_name, raw_password, role)
    finally:
        db.close()


@app.on_event("startup")
async def on_startup():
    """Créer les tables et insérer les comptes de démonstration au démarrage"""
    Base.metadata.create_all(bind=engine)
    seed_demo_users()


@app.get("/", response_model=RootResponse)
def root() -> RootResponse:
    return {
        "message": "Bienvenue sur l'exo security.",
        "docs": "/docs",
        "features": ["jwt", "sqlite", "sqlalchemy", "rbac"],
    }


def include_routers(app: FastAPI):
    app.include_router(public.router)
    app.include_router(auth.router)
    app.include_router(private.router)


include_routers(app)

from typing import Generator

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from models import Base, User


DATABASE_URL = "sqlite:///demo.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


@app.get("/")
def home():
    return {"message": "Demo FastAPI + SQLAlchemy"}


@app.post("/users", status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise HTTPException(status_code=409, detail="email déjà utilisé")

    user = User(name=data.name, email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user.to_dict()


@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User).order_by(User.id)).all()
    return [user.to_dict() for user in users]


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="utilisateur introuvable")

    return user.to_dict()


@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="utilisateur introuvable")

    if data.name is not None:
        user.name = data.name

    if data.email is not None:
        existing_user = db.scalar(
            select(User).where(User.email == data.email, User.id != user_id)
        )
        if existing_user:
            raise HTTPException(status_code=409, detail="email déjà utilisé")
        user.email = data.email

    db.commit()
    db.refresh(user)

    return user.to_dict()


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="utilisateur introuvable")

    db.delete(user)
    db.commit()

    return {"message": "utilisateur supprimé"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",host='0.0.0.0',port=8000,reload=True)
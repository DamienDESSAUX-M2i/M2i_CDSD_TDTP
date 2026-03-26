from __future__ import annotations

from typing import Generator

from fastapi import Depends, FastAPI
from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


# ============================================================================
# Configuration SQLAlchemy
# ============================================================================
# Ici, on utilise SQLite dans un fichier local.
DATABASE_URL = "sqlite:///./modern_relations_demo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# ============================================================================
# Modèles ORM en écriture moderne SQLAlchemy 2.x
# ============================================================================

# une table (BookShelf) référence DEUX FOIS la même autre table (Author).



class Author(Base):
    __tablename__ = "authors"

    # Style moderne :
    # - Mapped[int] -> annotation de type SQLAlchemy ORM
    # - mapped_column(...) -> déclaration moderne de colonne
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class BookShelf(Base):
    __tablename__ = "bookshelves"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Ces deux colonnes sont des clés étrangères vers la même table : authors.
    favorite_author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    secondary_author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    # relationship(...) ne crée pas la clé étrangère en base.
    # Elle permet surtout d'accéder facilement aux objets liés en Python.
    # Comme on référence deux fois la même table, on doit préciser foreign_keys.
    favorite_author: Mapped[Author] = relationship(foreign_keys=[favorite_author_id])
    secondary_author: Mapped[Author] = relationship(foreign_keys=[secondary_author_id])


# ============================================================================
# Initialisation et données de démonstration
# ============================================================================
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # Si des auteurs existent déjà, on considère que la base est initialisée.
        existing_author = db.execute(select(Author)).scalars().first()
        if existing_author:
            return

        author_1 = Author(name="Agatha Christie")
        author_2 = Author(name="Jules Verne")
        author_3 = Author(name="Isaac Asimov")

        db.add_all([author_1, author_2, author_3])
        db.commit()

        # Après le commit, les IDs sont disponibles sur les objets.
        shelf_1 = BookShelf(
            name="Mystery Shelf",
            favorite_author_id=author_1.id,
            secondary_author_id=author_2.id,
        )
        shelf_2 = BookShelf(
            name="Science Fiction Shelf",
            favorite_author_id=author_3.id,
            secondary_author_id=author_2.id,
        )

        db.add_all([shelf_1, shelf_2])
        db.commit()


# ============================================================================
# Dépendance FastAPI pour obtenir une session SQLAlchemy
# ============================================================================
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Application FastAPI
# ============================================================================
app = FastAPI(
    title="SQLAlchemy Relations Demo - Modern Style",
    description="Mini démo en un seul fichier avec Mapped + mapped_column + relationship",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict:
    return {
        "message": "Demo SQLAlchemy moderne prête",
        "endpoints": ["/authors", "/bookshelves", "/authors-execute"],
    }


@app.get("/authors")
def get_authors(db: Session = Depends(get_db)) -> list[dict]:
    authors = db.execute(select(Author)).scalars().all()
    return [{"id": author.id, "name": author.name} for author in authors]


@app.get("/bookshelves")
def get_bookshelves(db: Session = Depends(get_db)) -> list[dict]:
    shelves = db.execute(select(BookShelf)).scalars().all()

    # Grâce à relationship(...), on peut accéder directement à :
    # - shelf.favorite_author
    # - shelf.secondary_author
    return [
        {
            "id": shelf.id,
            "name": shelf.name,
            "favorite_author": {
                "id": shelf.favorite_author.id,
                "name": shelf.favorite_author.name,
            },
            "secondary_author": {
                "id": shelf.secondary_author.id,
                "name": shelf.secondary_author.name,
            },
        }
        for shelf in shelves
    ]


@app.get("/authors-execute")
def get_authors_with_execute(db: Session = Depends(get_db)) -> list[dict]:
    # Exemple avec db.execute(...)
    result = db.execute(select(Author))
    authors = result.scalars().all()

    return [{"id": author.id, "name": author.name} for author in authors]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

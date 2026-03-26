from fastapi import Depends, FastAPI
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy import ForeignKey, String, create_engine, select
from typing import Generator
 

"""
démo SQLAlchemy - relations 
=========================================================

- Author : un auteur
- BookShelf : une étagère qui contient exactement 2 auteurs favoris

Documentation :
    http://127.0.0.1:8000/docs
"""

# -----------------------------------------------------------------------------
# Configuration SQLAlchemy
# -----------------------------------------------------------------------------

DATABASE_URL = "sqlite:///./relations_demo_v2.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# Modèle 1 : Author
# -----------------------------------------------------------------------------

class Author(Base):
    """
    Table simple : un auteur.

    Cette classe devient une table SQL grâce à SQLAlchemy.
    Chaque instance Python représente une ligne dans la table.
    """

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


# -----------------------------------------------------------------------------
# Modèle 2 : BookShelf
# -----------------------------------------------------------------------------

class BookShelf(Base):
    """
    Une étagère avec exactement deux auteurs favoris.

    - favorite_author_id -> authors.id
    - second_favorite_author_id -> authors.id

    Comme les deux colonnes pointent vers la même table, SQLAlchemy a besoin
    qu'on lui précise quelle colonne correspond à quelle relation Python.
    """

    __tablename__ = "bookshelves"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)

    # Ces deux colonnes sont des clés étrangères vers la même table : authors.
    favorite_author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    second_favorite_author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Ces relations permettent d'accéder directement aux objets Author.
    # Le paramètre foreign_keys=[...] est indispensable ici car il y a deux liens
    # possibles vers la table authors.
    favorite_author = relationship("Author", foreign_keys=[favorite_author_id])
    second_favorite_author = relationship("Author", foreign_keys=[second_favorite_author_id])


# -----------------------------------------------------------------------------
# Création des tables
# -----------------------------------------------------------------------------

Base.metadata.create_all(bind=engine)


# -----------------------------------------------------------------------------
# Données de démonstration
# -----------------------------------------------------------------------------

def seed_data() -> None:
    """
    Insère quelques données si la base est vide.

    On crée :
    - 3 auteurs
    - 2 étagères

    Cela permet de démarrer la démo immédiatement sans avoir à faire de POST.
    """
    db: Session = SessionLocal()
    try:
        existing_authors = db.query(Author).count()
        if existing_authors > 0:
            return

        author_1 = Author(name="Victor Hugo")
        author_2 = Author(name="Jane Austen")
        author_3 = Author(name="Jules Verne")

        db.add_all([author_1, author_2, author_3])
        db.commit()
        db.refresh(author_1)
        db.refresh(author_2)
        db.refresh(author_3)

        shelf_1 = BookShelf(
            label="Classiques A",
            favorite_author_id=author_1.id,
            second_favorite_author_id=author_2.id,
        )

        shelf_2 = BookShelf(
            label="Classiques B",
            favorite_author_id=author_3.id,
            second_favorite_author_id=author_1.id,
        )

        db.add_all([shelf_1, shelf_2])
        db.commit()
    finally:
        db.close()


seed_data()


# -----------------------------------------------------------------------------
# Application FastAPI
# -----------------------------------------------------------------------------

app = FastAPI(
    title="SQLAlchemy Relations Demo",
    description="Démo des relations SQLAlchemy",
    version="1.0.0",
)


@app.get("/")
def root():
    """
    Petit endpoint d'accueil.
    """
    return {
        "message": "démo SQLAlchemy sur les relations.",
        "idea": "Une étagère référence deux auteurs favoris.",
        "important": [
            "ForeignKey crée le lien côté base",
            "relationship facilite l'accès côté Python",
            "foreign_keys=[...] est nécessaire si on pointe deux fois vers la même table"
        ]
    }


@app.get("/authors")
def get_authors():
    """
    Retourne la liste des auteurs.

    Endpoint simple, juste pour voir le contenu de la table Author.
    """
    db: Session = SessionLocal()
    try:
        authors = db.query(Author).all()
        return [
            {
                "id": author.id,
                "name": author.name
            }
            for author in authors
        ]
    finally:
        db.close()


@app.get("/bookshelves")
def get_bookshelves():
    """
    Retourne les étagères avec les noms des deux auteurs liés.

    Ici, on voit l'intérêt de relationship(...).
    Grâce à cela, on peut écrire :
    - shelf.favorite_author.name
    - shelf.second_favorite_author.name

    Sans relationship, on aurait seulement les ids.
    """
    db: Session = SessionLocal()
    try:
        shelves = db.query(BookShelf).all()
        return [
            {
                "id": shelf.id,
                "label": shelf.label,
                "favorite_author_id": shelf.favorite_author_id,
                "favorite_author_name": shelf.favorite_author.name,
                "second_favorite_author_id": shelf.second_favorite_author_id,
                "second_favorite_author_name": shelf.second_favorite_author.name,
            }
            for shelf in shelves
        ]
    finally:
        db.close()

@app.get("/authors-execute")
def get_authors_with_execute(db: Session = Depends(get_db)):
    result = db.execute(select(Author))
    authors = result.scalars().all()

    return [
        {
            "id": author.id,
            "name": author.name
        }
        for author in authors
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

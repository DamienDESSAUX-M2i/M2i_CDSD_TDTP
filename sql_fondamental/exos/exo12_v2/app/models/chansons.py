import datetime

from pydantic import BaseModel, ValidationError


class Chansons(BaseModel):
    titre: str
    artiste: str
    album: str
    duree: datetime.time
    genre: str
    annee_sortie: datetime.date


if __name__ == "__main__":
    data = {
        "titre": "titre",
        "artiste": "artiste",
        "album": "album",
        "duree": "00:05:00",
        "genre": "genre",
        "annee_sortie": "2000-03-14",
    }
    try:
        chanson = Chansons(**data)
        print(chanson)
    except ValidationError as e:
        print(e.errors())

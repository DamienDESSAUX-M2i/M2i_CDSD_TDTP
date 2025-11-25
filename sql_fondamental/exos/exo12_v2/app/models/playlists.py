import datetime

from pydantic import BaseModel, PositiveInt, ValidationError


class Playlists(BaseModel):
    nom_playlist: str
    date_creation: datetime.date
    id_utilisateur: PositiveInt


if __name__ == "__main__":
    data = {
        "nom_playlist": "nom",
        "date_creation": "2000-03-14",
        "id_utilisateur": "1",
    }
    try:
        playlist = Playlists(**data)
        print(playlist)
    except ValidationError as e:
        print(e.errors())

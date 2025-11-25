from pydantic import BaseModel, PositiveInt, ValidationError


class PlaylistsChansons(BaseModel):
    id_playlist: PositiveInt
    id_chanson: PositiveInt


if __name__ == "__main__":
    data = {
        "id_playlist": "1",
        "id_chanson": "1",
    }
    try:
        playlist_chanson = PlaylistsChansons(**data)
        print(playlist_chanson)
    except ValidationError as e:
        print(e.errors())

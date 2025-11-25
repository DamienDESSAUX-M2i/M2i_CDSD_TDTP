import datetime

from pydantic import BaseModel, EmailStr, ValidationError


class Utilisateurs(BaseModel):
    nom_utilisateur: str
    email: EmailStr
    date_inscription: datetime.date


if __name__ == "__main__":
    data = {
        "nom_utilisateur": "nom",
        "email": "nom@m2i.com",
        "date_inscription": "2000-03-14",
    }
    try:
        utilisateur = Utilisateurs(**data)
        print(utilisateur)
    except ValidationError as e:
        print(e.errors())

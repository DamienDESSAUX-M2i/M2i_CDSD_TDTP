import datetime

from app.ihm.utils import get_email, get_positive_int, get_str
from app.repository.utilisateurs_repository import (
    delete_utilisateur,
    insert_into_utilisateurs,
    select_utilisateur,
    update_utilisateur,
)


def display_utilisateur() -> None:
    id_utilisateur: int = get_positive_int(message="ID utilisateur : ")
    if id_utilisateur:
        row = select_utilisateur(id_utilisateur=id_utilisateur)
        if row:
            print(row)
        else:
            print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")


def add_utilisateur() -> None:
    nom_utilisateur = get_str(message="Nom : ")
    email = get_email(message="Email : ")
    insert_into_utilisateurs(
        nom_utilisateur=nom_utilisateur,
        email=email,
        date_inscription=datetime.date.today(),
    )


def modify_utilisateur() -> None:
    id_utilisateur: int = get_positive_int(message="ID utilisateur : ")
    row = select_utilisateur(id_utilisateur=id_utilisateur)
    if row:
        nom_utilisateur: str = input(f"Nom ({row[0]}) : ")
        if nom_utilisateur.isspace() or nom_utilisateur == "":
            nom_utilisateur = row[0]
        email: str = input(f"Email ({row[1]}) : ")
        date_inscription: str = input(f"Date d'inscription AAAA-MM-JJ ({row[2]}) : ")
        try:
            year = int(date_inscription.split("-")[0])
            month = int(date_inscription.split("-")[1])
            day = int(date_inscription.split("-")[2])
            date_inscription: datetime.date = datetime.date(year, month, day)
        except Exception:
            date_inscription: datetime.date = row[3]
        update_utilisateur(
            id_utilisateur=id_utilisateur,
            nom_utilisateur=nom_utilisateur,
            email=email,
            date_inscription=date_inscription,
        )
    else:
        print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")


def remove_utilisateur() -> None:
    id_utilisateur: int = get_positive_int(message="ID utilisateur : ")
    if id_utilisateur:
        delete_utilisateur(id_utilisateur=id_utilisateur)


def show():
    menu_name: str = "=== Menu utilisateurs ==="
    menu_message: str = "\n".join(
        [
            "[1] Afficher",
            "[2] Ajouter",
            "[3] Modifier",
            "[4] Supprimer",
            "[0] Quitter",
            "=>",
        ]
    )
    while True:
        print(menu_name)
        input_user: str = input(menu_message)
        match input_user:
            case "1":
                display_utilisateur()
            case "2":
                add_utilisateur()
            case "3":
                modify_utilisateur()
            case "4":
                remove_utilisateur()
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")

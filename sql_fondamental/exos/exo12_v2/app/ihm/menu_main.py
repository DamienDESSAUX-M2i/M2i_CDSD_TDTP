from app.ihm import menu_chansons, menu_playlists, menu_utilisateurs


def show():
    menu_name: str = "=== Menu principal ==="
    menu_message: str = "\n".join(
        [
            "[1] Utilisateurs",
            "[2] Chansons",
            "[3] Playlists",
            "[0] Quitter",
            "=>",
        ]
    )
    while True:
        print(menu_name)
        input_user: str = input(menu_message)
        match input_user:
            case "1":
                menu_utilisateurs.show()
            case "2":
                menu_chansons.show()
            case "3":
                menu_playlists.show()
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")

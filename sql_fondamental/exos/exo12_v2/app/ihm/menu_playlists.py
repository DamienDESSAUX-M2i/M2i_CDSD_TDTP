def menu_playlists():
    msg_menu = "[1] Afficher\n[2] Ajouter\n[3] Modifier\n[4] Supprimer\n[5] Remplir\n[6] Vider\n[0] Quitter\n=> "
    while True:
        input_user: str = input(msg_menu)
        match input_user:
            case "1":
                id_playlist: str = input("ID playlist : ")
                try:
                    id_playlist: int = int(id_playlist)
                    row = select_playlist_chansons(id_playlist=id_playlist)
                    if row:
                        print(row)
                    else:
                        print(f"Aucune playlist n'a l'id {id_playlist}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "2":
                id_utilisateur: str = input("ID utilisateur : ")
                row = select_utilisateur(id_utilisateur=id_utilisateur)
                if row:
                    nom_playlist: str = input("Nom playlist : ")
                    date_creation: str = datetime.date.today()
                    insert_into_playlists(
                        id_utilisateur=id_utilisateur,
                        nom_playlist=nom_playlist,
                        date_creation=date_creation,
                    )
                else:
                    print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")
            case "3":
                id_playlist: str = input("ID playlist : ")
                try:
                    id_playlist: int = int(id_playlist)
                    row = select_playlist(id_playlist=id_playlist)
                    if row:
                        id_utilisateur: str = input(f"ID utilisateur ({row[0]}): ")
                        try:
                            id_utilisateur = int(id_utilisateur)
                            if not select_utilisateur(id_utilisateur=id_utilisateur):
                                raise ValueError(f"{id_utilisateur} n'est pas valide.")
                        except Exception:
                            id_utilisateur = row[0]
                        nom_playlist: str = input(f"Nom playlist ({row[1]}): ")
                        date_creation: str = input(
                            f"Date de création AAAA-MM-JJ ({row[2]}): "
                        )
                        try:
                            year = int(date_creation.split("-")[0])
                            month = int(date_creation.split("-")[1])
                            day = int(date_creation.split("-")[2])
                            date_creation: datetime.date = datetime.date(
                                year, month, day
                            )
                        except Exception:
                            date_creation: datetime.date = row[2]
                        update_playlist(
                            id_playlist=id_playlist,
                            id_utilisateur=id_utilisateur,
                            nom_playlist=nom_playlist,
                            date_creation=date_creation,
                        )
                    else:
                        print(f"Aucune playlist n'a l'id {id_playlist}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "4":
                id_playlist: str = input("ID playlist : ")
                try:
                    id_playlist: int = int(id_playlist)
                    delete_playlist(id_playlist=id_playlist)
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "5":
                id_playlist: str = input("ID playlist : ")
                try:
                    id_playlist: int = int(id_playlist)
                    row = select_playlist(id_playlist=id_playlist)
                    if row:
                        id_chanson: str = input("ID chanson : ")
                        try:
                            id_chanson: int = int(id_chanson)
                            row = select_chanson(id_chanson=id_chanson)
                            if row:
                                insert_into_playlists_chansons(
                                    id_playlist=id_playlist, id_chanson=id_chanson
                                )
                            else:
                                print(f"Aucune chanson n'a l'id {id_chanson}.")
                        except Exception:
                            print("Saisie invalide, veuilliez recommencer.")
                    else:
                        print(f"Aucune playlist n'a l'id {id_playlist}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "6":
                id_playlist: str = input("ID playlist : ")
                try:
                    id_playlist: int = int(id_playlist)
                    row = select_playlist(id_playlist=id_playlist)
                    if row:
                        id_chanson: str = input("ID chanson : ")
                        try:
                            id_chanson: int = int(id_chanson)
                            row = select_playlist_chanson(
                                id_playlist=id_playlist, id_chanson=id_chanson
                            )
                            if row:
                                delete_playlist_chanson(
                                    id_playlist=id_playlist, id_chanson=id_chanson
                                )
                            else:
                                print(
                                    f"Aucune chanson n'a l'id {id_chanson} dans cette playlist."
                                )
                        except Exception:
                            print("Saisie invalide, veuilliez recommencer.")
                    else:
                        print(f"Aucune playlist n'a l'id {id_playlist}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")

def menu_chansons():
    msg_menu = (
        "[1] Afficher\n[2] Ajouter\n[3] Modifier\n[4] Supprimer\n[0] Quitter\n=> "
    )
    while True:
        input_user: str = input(msg_menu)
        match input_user:
            case "1":
                id_chanson: str = input("ID chanson : ")
                try:
                    id_chanson: int = int(id_chanson)
                    row = select_chanson(id_chanson=id_chanson)
                    if row:
                        print(row)
                    else:
                        print(f"Aucune chanson n'a l'id {id_chanson}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "2":
                titre: str = input("Titre : ")
                artiste: str = input("Artiste : ")
                album: str = input("Album : ")
                duree: str = input("Durée HH:MM:SS: ")
                try:
                    h: int = int(duree.split(":")[0])
                    m: int = int(duree.split(":")[1])
                    s: int = int(duree.split(":")[2])
                    duree: datetime.time = datetime.time(h, m, s)
                except Exception:
                    duree: datetime.time = datetime.time(0, 0, 0)
                genre: str = input("Genre : ")
                annee_sortie: str = input("Année de sortie AAAA-MM-JJ: ")
                try:
                    year = int(annee_sortie.split("-")[0])
                    month = int(annee_sortie.split("-")[1])
                    day = int(annee_sortie.split("-")[2])
                    annee_sortie: datetime.date = datetime.date(year, month, day)
                except Exception:
                    annee_sortie: datetime.date = datetime.date.today()
                insert_into_chansons(
                    titre=titre,
                    artiste=artiste,
                    album=album,
                    duree=duree,
                    genre=genre,
                    annee_sortie=annee_sortie,
                )
            case "3":
                id_chanson: str = input("ID chanson : ")
                try:
                    id_chanson: int = int(id_chanson)
                    row = select_chanson(id_chanson=id_chanson)
                    if row:
                        titre: str = input(f"Titre ({row[0]}) : ")
                        artiste: str = input(f"Artiste ({row[1]}) : ")
                        album: str = input(f"Album ({row[2]}) : ")
                        duree: str = input(f"Durée HH:MM:SS ({row[3]}) : ")
                        try:
                            h: int = int(duree.split(":")[0])
                            m: int = int(duree.split(":")[1])
                            s: int = int(duree.split(":")[2])
                            duree: datetime.time = datetime.time(h, m, s)
                        except Exception:
                            duree: datetime.time = row[3]
                        genre: str = input(f"Genre ({row[4]}) : ")
                        annee_sortie: str = input(
                            f"Année de sortie AAAA-MM-JJ ({row[5]}) : "
                        )
                        try:
                            year = int(annee_sortie.split("-")[0])
                            month = int(annee_sortie.split("-")[1])
                            day = int(annee_sortie.split("-")[2])
                            annee_sortie: datetime.date = datetime.date(
                                year, month, day
                            )
                        except Exception:
                            annee_sortie: datetime.date = row[5]
                        update_chanson(
                            id_chanson=id_chanson,
                            titre=titre,
                            artiste=artiste,
                            album=album,
                            duree=duree,
                            genre=genre,
                            annee_sortie=annee_sortie,
                        )
                    else:
                        print(f"Aucun utilisateur n'a l'id {id_chanson}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "4":
                id_chanson: str = input("ID chanson : ")
                try:
                    id_chanson: int = int(id_chanson)
                    delete_chanson(id_chanson=id_chanson)
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")

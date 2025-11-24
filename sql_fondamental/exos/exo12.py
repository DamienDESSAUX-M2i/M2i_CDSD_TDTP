import datetime

import psycopg

DSN = "dbname=mydb user=root password=root host=localhost port=5432"


def init_db():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                # DROP TABLES
                cursor.execute("DROP TABLE IF EXISTS playlists_chansons;")
                cursor.execute("DROP TABLE IF EXISTS chansons;")
                cursor.execute("DROP TABLE IF EXISTS playlists;")
                cursor.execute("DROP TABLE IF EXISTS utilisateurs;")
                # CREATE TABLES
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS utilisateurs (
                        id_utilisateur SERIAL PRIMARY KEY,
                        nom_utilisateur VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        date_inscription DATE NOT NULL DEFAULT CURRENT_DATE
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS playlists (
                        id_playlist SERIAL PRIMARY KEY,
                        nom_playlist VARCHAR(255) NOT NULL,
                        date_creation DATE NOT NULL,
                        id_utilisateur INT NOT NULL,
                        CONSTRAINT fk_id_utilisateur
                            FOREIGN KEY (id_utilisateur)
                            REFERENCES utilisateurs(id_utilisateur)
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS chansons (
                        id_chanson SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        artiste VARCHAR(255) NOT NULL,
                        album VARCHAR(255) NOT NULL,
                        duree TIME NOT NULL,
                        genre VARCHAR(255) NOT NULL,
                        annee_sortie DATE NOT NULL
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS playlists_chansons (
                        id_playlist INT NOT NULL,
                        id_chanson INT NOT NULL,
                        CONSTRAINT pk_id_playlist_id_chanson
                            PRIMARY KEY (id_playlist, id_chanson),
                        CONSTRAINT fk_id_playlist
                            FOREIGN KEY (id_playlist)
                            REFERENCES playlists(id_playlist),
                        CONSTRAINT fk_id_chanson
                            FOREIGN KEY (id_chanson)
                            REFERENCES chansons(id_chanson)
                    );
                    """
                )
    except Exception as e:
        print(e)


def insert_into_utilisateurs(
    nom_utilisateur: str, email: str, date_inscription: datetime.date
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO utilisateurs (nom_utilisateur, email, date_inscription) VALUES (%s, %s, %s) RETURNING *;",
                    (nom_utilisateur, email, date_inscription),
                )
                print(
                    f"Insertion d'un utilisateur dans la table utilisateurs :\n{cursor.fetchone()}"
                )
    except Exception as e:
        print(e)


def select_utilisateur(id_utilisateur: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom_utilisateur, email, date_inscription FROM utilisateurs WHERE id_utilisateur=%s;",
                    (id_utilisateur,),
                )
                return cursor.fetchone()
    except Exception as e:
        print(e)


def update_utilisateur(
    id_utilisateur: int,
    nom_utilisateur: str,
    email: str,
    date_inscription: datetime.date,
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_utilisateur(id_utilisateur=id_utilisateur)
                if row:
                    cursor.execute(
                        """
                        UPDATE utilisateurs
                        SET nom_utilisateur=%s, email=%s, date_inscription=%s
                        WHERE id_utilisateur=%s
                        RETURNING *;
                        """,
                        (nom_utilisateur, email, date_inscription, id_utilisateur),
                    )
                    print(
                        f"Modification d'un utilisateur dans la table utilisateurs :\nAvant : {row}\nAprès : {cursor.fetchone()}"
                    )
                else:
                    print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")
    except Exception as e:
        print(e)


def delete_utilisateur(id_utilisateur: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_utilisateur(id_utilisateur=id_utilisateur)
                if row:
                    cursor.execute(
                        "DELETE FROM playlists WHERE id_utilisateur=%s",
                        (id_utilisateur,),
                    )
                    print(
                        "Suppression des playlists associées à l'utilisateur dans la table playlists."
                    )
                    cursor.execute(
                        "DELETE FROM utilisateurs WHERE id_utilisateur=%s",
                        (id_utilisateur,),
                    )
                    print(
                        f"Suppression d'un utilisateur dans la table utilisateurs :\n{row}"
                    )
                else:
                    print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")
    except Exception as e:
        print(e)


def insert_into_chansons(
    titre: str,
    artiste: str,
    album: str,
    duree: datetime.time,
    genre: str,
    annee_sortie: datetime.date,
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chansons (titre, artiste, album, duree, genre, annee_sortie) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;",
                    (titre, artiste, album, duree, genre, annee_sortie),
                )
                print(
                    f"Insertion d'une chanson dans la table chansons :\n{cursor.fetchone()}"
                )
    except Exception as e:
        print(e)


def select_chanson(id_chanson: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT titre, artiste, album, duree, genre, annee_sortie FROM chansons WHERE id_chanson=%s;",
                    (id_chanson,),
                )
                return cursor.fetchone()
    except Exception as e:
        print(e)


def update_chanson(
    id_chanson: int,
    titre: str,
    artiste: str,
    album: str,
    duree: datetime.time,
    genre: str,
    annee_sortie: datetime.date,
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_chanson(id_chanson=id_chanson)
                if row:
                    cursor.execute(
                        """
                        UPDATE chansons
                        SET titre=%s, artiste=%s, album=%s, duree=%s, genre=%s, annee_sortie=%s
                        WHERE id_chanson=%s
                        RETURNING *;
                        """,
                        (titre, artiste, album, duree, genre, annee_sortie, id_chanson),
                    )
                    print(
                        f"Modification d'une chanson dans la table chansons :\nAvant : {row}\nAprès : {cursor.fetchone()}"
                    )
                else:
                    print(f"Aucune chanson n'a l'id {id_chanson}.")
    except Exception as e:
        print(e)


def delete_chanson(id_chanson: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_chanson(id_chanson=id_chanson)
                if row:
                    cursor.execute(
                        "DELETE FROM playlists_chansons WHERE id_chanson=%s",
                        (id_chanson,),
                    )
                    print(
                        "Suppression des playlists_chansons associées à la chanson dans la table playlists_chansons."
                    )
                    cursor.execute(
                        "DELETE FROM chansons WHERE id_chanson=%s",
                        (id_chanson,),
                    )
                    print(f"Suppression d'une chanson dans la table chansons :\n{row}")
                else:
                    print(f"Aucune chanson n'a l'id {id_chanson}.")
    except Exception as e:
        print(e)


def insert_into_playlists(
    id_utilisateur: int, nom_playlist: str, date_creation: datetime.date
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO playlists (id_utilisateur, nom_playlist, date_creation) VALUES (%s, %s, %s) RETURNING *;",
                    (id_utilisateur, nom_playlist, date_creation),
                )
                print(
                    f"Insertion d'une chanson dans la table chansons :\n{cursor.fetchone()}"
                )
    except Exception as e:
        print(e)


def select_playlist(id_playlist):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.nom_utilisateur, p.nom_playlist, p.date_creation
                    FROM playlists AS p
                    INNER JOIN utilisateurs AS u
                    ON p.id_utilisateur = u.id_utilisateur
                    WHERE p.id_playlist=%s;
                    """,
                    (id_playlist,),
                )
                return cursor.fetchone()
    except Exception as e:
        print(e)


def select_playlist_chansons(id_playlist):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.nom_utilisateur, p.nom_playlist, p.date_creation, c.titre, c.artiste, c.album, c.duree, c.genre, c.annee_sortie
                    FROM playlists AS p
                    INNER JOIN utilisateurs AS u
                    ON p.id_utilisateur = u.id_utilisateur
                    INNER JOIN playlists_chansons AS pc
                    ON p.id_playlist = pc.id_playlist
                    INNER JOIN chansons AS c
                    ON pc.id_chanson = c.id_chanson
                    WHERE p.id_playlist=%s;
                    """,
                    (id_playlist,),
                )
                return cursor.fetchall()
    except Exception as e:
        print(e)


def insert_into_playlists_chansons(id_playlist: int, id_chanson: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO playlists_chansons (id_playlist, id_chanson) VALUES (%s, %s) RETURNING *;",
                    (id_playlist, id_chanson),
                )
                print(
                    f"Insertion d'une chanson dans la table playlists_chansons :\n{cursor.fetchone()}"
                )
    except Exception as e:
        print(e)


def update_playlist(
    id_playlist: int,
    id_utilisateur: int,
    nom_playlist: str,
    date_creation: datetime.date,
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_playlist(id_playlist=id_playlist)
                if row:
                    cursor.execute(
                        """
                        UPDATE playlist
                        SET id_utilisateur=%s, nom_playlist=%s, date_creation=%s
                        WHERE id_chanson=%s
                        RETURNING *;
                        """,
                        (id_utilisateur, nom_playlist, date_creation, id_playlist),
                    )
                    print(
                        f"Modification d'une chanson dans la table chansons :\nAvant : {row}\nAprès : {cursor.fetchone()}"
                    )
                else:
                    print(f"Aucune chanson n'a l'id {id_playlist}.")
    except Exception as e:
        print(e)


def delete_playlist(id_playlist: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                row = select_playlist(id_playlist=id_playlist)
                if row:
                    cursor.execute(
                        "DELETE FROM playlists_chansons WHERE id_playlist=%s",
                        (id_playlist,),
                    )
                    print(
                        "Suppression des playlists_chansons associées à la playlist dans la table playlists_chansons."
                    )
                    cursor.execute(
                        "DELETE FROM playlists WHERE id_playlist=%s",
                        (id_playlist,),
                    )
                    print(
                        f"Suppression d'une playlist dans la table playlists :\n{row}"
                    )
                else:
                    print(f"Aucune paylist n'a l'id {id_playlist}.")
    except Exception as e:
        print(e)


def menu_utilisateurs():
    msg_menu = (
        "[1] Afficher\n[2] Ajouter\n[3] Modifier\n[4] Supprimer\n[0] Quitter\n=> "
    )
    while True:
        input_user: str = input(msg_menu)
        match input_user:
            case "1":
                id_utilisateur: str = input("ID utilisateur : ")
                try:
                    id_utilisateur: int = int(id_utilisateur)
                    row = select_utilisateur(id_utilisateur=id_utilisateur)
                    if row:
                        print(row)
                    else:
                        print(f"Aucun utilisateur n'a l'id {id_utilisateur}.")
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "2":
                nom_utilisateur = input("Nom : ")
                email = input("Email : ")
                insert_into_utilisateurs(
                    nom_utilisateur=nom_utilisateur,
                    email=email,
                    date_inscription=datetime.date.today(),
                )
            case "3":
                id_utilisateur: str = input("ID utilisateur : ")
                try:
                    id_utilisateur: int = int(id_utilisateur)
                    row = select_utilisateur(id_utilisateur=id_utilisateur)
                    if row:
                        nom_utilisateur: str = input(f"Nom ({row[0]}) : ")
                        email: str = input(f"Email ({row[1]}) : ")
                        date_inscription: str = input(
                            f"Date d'inscription AAAA-MM-JJ ({row[2]}) : "
                        )
                        try:
                            year = int(date_inscription.split("-")[0])
                            month = int(date_inscription.split("-")[1])
                            day = int(date_inscription.split("-")[2])
                            date_inscription: datetime.date = datetime.date(
                                year, month, day
                            )
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
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "4":
                id_utilisateur: str = input("ID utilisateur : ")
                try:
                    id_utilisateur: int = int(id_utilisateur)
                    delete_utilisateur(id_utilisateur=id_utilisateur)
                except Exception:
                    print("Saisie invalide, veuilliez recommencer.")
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")


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
                duree: str = input("Durée HH-MM-SS: ")
                try:
                    h: int = int(duree.split("-")[0])
                    m: int = int(duree.split("-")[1])
                    s: int = int(duree.split("-")[2])
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
                        duree: str = input(f"Durée HH-MM-SS ({row[3]}) : ")
                        try:
                            h: int = int(duree.split("-")[0])
                            m: int = int(duree.split("-")[1])
                            s: int = int(duree.split("-")[2])
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
                id_playlist: str = input("ID : ")
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
                pass  # Vider
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")


def menu_main():
    msg_menu = "[1] Utilisateurs\n[2] Chansons\n[3] Playlists\n[0] Quitter\n=> "
    while True:
        input_user: str = input(msg_menu)
        match input_user:
            case "1":
                menu_utilisateurs()
            case "2":
                menu_chansons()
            case "3":
                menu_playlists()
            case "0":
                break
            case _:
                print("Saisie invalide, veuilliez recommencer.")


def main() -> None:
    init_db()
    menu_main()


if __name__ == "__main__":
    main()

import datetime

import psycopg
from app.repository.dsn import DSN


def select_utilisateur(id_utilisateur: int):
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nom_utilisateur, email, date_inscription FROM utilisateurs WHERE id_utilisateur=%s;",
                    (id_utilisateur,),
                )
                return cursor.fetchone()
    except Exception as e:
        print(e)


def insert_into_utilisateurs(
    nom_utilisateur: str, email: str, date_inscription: datetime.date
):
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
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


def update_utilisateur(
    id_utilisateur: int,
    nom_utilisateur: str,
    email: str,
    date_inscription: datetime.date,
):
    try:
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
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
        with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as connection:
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

import datetime
from enum import Enum

import psycopg

DSN = "dbname=mydb user=root password=root host=localhost port=5432"


def drop_type_regime_alimentaire():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TYPE IF EXISTS regime_alimentaire_enum;")
    except Exception as e:
        print(e)


def create_type_regime_alimentaire():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "CREATE TYPE regime_alimentaire_enum AS ENUM ('herbivore', 'carnivore', 'omnivore');"
                )
    except Exception as e:
        print(e)


def drop_table_animals():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS animals;")
    except Exception as e:
        print(e)


def create_table_animals():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE animals (
                        animal_id SERIAL PRIMARY KEY,
                        nom VARCHAR(255) NOT NULL,
                        age INT NOT NULL,
                        regime_alimentaire regime_alimentaire_enum NOT NULL,
                        date_arrivee DATE NOT NULL
                    );
                    """
                )
    except Exception as e:
        print(e)


class RegimeAlimentaire(Enum):
    HERBIVORE = "herbivore"
    CARNIVORE = "carnivore"
    OMNIVORE = "omnivore"


def insert_into_animals(
    nom: str, age: int, regime_alimentaire: RegimeAlimentaire, date: datetime.date
):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO animals (nom, age, regime_alimentaire, date_arrivee) VALUES (%s, %s, %s, %s) RETURNING *;",
                    (nom, age, regime_alimentaire.value, date),
                )
                print(f"Insertion titi :\n{cursor.fetchone()}")
    except Exception as e:
        print(e)


def select_animal_id(animal_id: int):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM animals WHERE animal_id=%s;", (animal_id,)
                )
                titi_row = cursor.fetchall()
                print(f"Recherche par id :\n{titi_row = }")
    except Exception as e:
        print(e)


def select_animal_nom(nom: str):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM animals WHERE nom=%s;", (nom,))
                titi_row = cursor.fetchone()
                print(f"Recherche par nom :\n{titi_row = }")
    except Exception as e:
        print(e)


def drop_table_regimes_alimentaires():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS regimes_alimentaires;")
    except Exception as e:
        print(e)


def create_table_regimes_alimentaires():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE regimes_alimentaires (
                        regime_alimentaire_id SERIAL PRIMARY KEY,
                        regime_alimentaire VARCHAR(255) NOT NULL
                    );
                    """
                )
    except Exception as e:
        print(e)


def insert_into_regimes_alimentaires(regime_alimentaire: RegimeAlimentaire):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO regimes_alimentaires (regime_alimentaire) VALUES (%s) RETURNING *;",
                    (regime_alimentaire.value,),
                )
                print(f"Insertion {regime_alimentaire.value} :\n{cursor.fetchone()}")
    except Exception as e:
        print(e)


def alter_table_animals():
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    ALTER TABLE animals
                    ADD COLUMN regime_alimentaire_id INT
                    """
                )
                cursor.execute(
                    """
                    ALTER TABLE animals
                    ADD CONSTRAINT fk_regime_alimentaire
                    FOREIGN KEY (regime_alimentaire_id)
                    REFERENCES regimes_alimentaires(regime_alimentaire_id);
                    """
                )
                for regime_alimentaire in RegimeAlimentaire:
                    cursor.execute(
                        """
                        UPDATE animals
                        SET regime_alimentaire_id=(
                            SELECT regime_alimentaire_id
                            FROM regimes_alimentaires
                            WHERE regime_alimentaire=%s
                            )
                        WHERE regime_alimentaire=%s;
                        """,
                        (regime_alimentaire.value, regime_alimentaire.value),
                    )
                cursor.execute("ALTER TABLE animals DROP COLUMN regime_alimentaire;")
                print("Success : Alteration table animals")
    except Exception as e:
        print(e)


def select_animal_regime_alimentaire(regime_alimentaire: RegimeAlimentaire):
    try:
        with psycopg.connect(DSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM animals AS a
                    INNER JOIN regimes_alimentaires AS r
                    ON a.regime_alimentaire_id = r.regime_alimentaire_id
                    WHERE r.regime_alimentaire=%s;
                    """,
                    (regime_alimentaire.value,),
                )
                rows = cursor.fetchall()
                for row in rows:
                    print(f"Recherche par régime alimentaire :\n{row}")
    except Exception as e:
        print(e)


def main() -> None:
    # Clean db
    drop_table_regimes_alimentaires()
    drop_table_animals()
    drop_type_regime_alimentaire()

    # Question 1
    create_type_regime_alimentaire()
    create_table_animals()

    # Question 2.1
    animal_nom = "titi"
    animal_age = 1
    animal_regime_alimentaire = RegimeAlimentaire("omnivore")
    animal_date_arrivee = datetime.date(2025, 11, 24)
    insert_into_animals(
        animal_nom, animal_age, animal_regime_alimentaire, animal_date_arrivee
    )

    # Question 2.2
    select_animal_id(1)

    # Question 2.3
    select_animal_nom(animal_nom)

    # Bonus
    create_table_regimes_alimentaires()
    for regime_alimentaire in RegimeAlimentaire:
        insert_into_regimes_alimentaires(regime_alimentaire)
    alter_table_animals()
    select_animal_regime_alimentaire(animal_regime_alimentaire)


if __name__ == "__main__":
    main()

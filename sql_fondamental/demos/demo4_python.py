import psycopg

connection = psycopg.connect(
    dbname="mydb", user="root", password="root", host="localhost", port="5432"
)

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute(
    """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        age INT
    );
    """
)

connection.commit()

cursor.close()

connection.close()


# CONTEXT MANAGER

DSN = "dbname=mydb user=root password=root host=localhost port=5432"

with psycopg.connect(DSN) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        print(cursor.fetchall())


# EXCEPTIONS

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELEC * FROM users;")
            rows = cursor.fetchall()
            print(rows)
except psycopg.errors.SyntaxError as e:
    print(e)


# INSERT

user_id = 0

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (first_name, last_name, age) VALUES (%s, %s, %s) RETURNING user_id;",
                ("John", "Doe", 30),
            )
            user_id = cursor.fetchone()[0]
            print(user_id)
except Exception as e:
    print(e)


# UPDATE

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET age=%s WHERE user_id=%s RETURNING *;",
                (40, user_id),
            )
            row = cursor.fetchone()
            print(row)
except Exception as e:
    print(e)


# SELECT

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
except Exception as e:
    print(e)

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id=%s;", (user_id,))
            row = cursor.fetchone()
            print(row)
except Exception as e:
    print(e)


# DELETE

try:
    with psycopg.connect(DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users;")
except Exception as e:
    print(e)

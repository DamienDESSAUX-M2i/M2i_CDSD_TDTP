from pydantic_settings import BaseSettings

DSN = "dbname=mydb user=admin password=admin host=pgdb port=5432"


class Settings(BaseSettings):
    dbname: str = "mydb"
    user: str = "admin"
    password: str = "admin"
    host: str = "pgdb"
    port: int = 5432


if __name__ == "__main__":
    print(Settings())

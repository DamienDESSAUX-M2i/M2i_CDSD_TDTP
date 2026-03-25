from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = Field(
        ...,
        alias="VAR_NAME",
        title="Name",
        description="Application's name",
        examples=["app"],
    )
    debug: bool = Field(
        default=False,
        alias="DEBUG",
        title="Debug Mode",
        description="Debug Mode (default=False)",
        examples=[True],
    )
    database_url: PostgresDsn = Field(
        ...,
        alias="DB_URL",
        title="Postgres DSN",
        description="Postgres DSN",
        examples=["postgresql://user:password@localhost:5432/mydb"],
    )
    secret_key: SecretStr = Field(
        ...,
        alias="SECRET_KEY",
        title="Secret Key",
        description="Secret Key",
        examples=["secret123"],
    )
    api_v1_prefix: str = Field(
        "/api/v1",
        alias="API_PREFIX",
        title="Prefix",
        description="API prefix",
        examples=["/api/v1"],
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


api_config = AppSettings()

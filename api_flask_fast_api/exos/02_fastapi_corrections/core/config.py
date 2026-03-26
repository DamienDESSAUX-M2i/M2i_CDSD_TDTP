from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field("TP2 FastAPI API", alias="APP_NAME")
    debug: bool = Field(False, alias="DEBUG")
    database_url: Optional[str] = Field(None, alias="DATABASE_URL")
    secret_key: str = Field("dev-secret-key-change-in-production", alias="SECRET_KEY")
    api_v1_prefix: str = Field("/api/v1", alias="API_V1_PREFIX")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
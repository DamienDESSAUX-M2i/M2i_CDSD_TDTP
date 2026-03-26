from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BAB.P.I"
    debug: bool = False
    api_prefix: str = "/api"

    secret_key: str
    algorithm: Literal["HS256"] = "HS256"
    iterations: int = 100_000
    access_token_expire_minutes: int = 60

    database_path: str = "data/db.sqlite"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("access_token_expire_minutes")
    @classmethod
    def validate_expire_minutes(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be > 0")
        return v

    @field_validator("iterations")
    @classmethod
    def validate_iterations(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ITERATIONS must be > 0")
        return v

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()

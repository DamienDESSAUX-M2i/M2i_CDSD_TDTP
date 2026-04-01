"""Configuration de l'application."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ML Iris API"
    debug: bool = False
    log_level: str = "INFO"
    model_path: str = "models/iris_model.pkl"
    report_path: str = "models/training_report.json"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

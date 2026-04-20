import logging
import random
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)


@dataclass
class PipelineConfig:
    data_path: Path = Path("data/wine_data.csv")
    model_path: Path = Path("models/model.pkl")
    target: str = "quality"
    test_size: float = 0.2


@dataclass
class LoggerConfig:
    name: str = "app"
    logger_path: Path = Path("logs/app.log")


def set_up_logger(name: str = "app", file_path: Path | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if file_path:
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            file_path, maxBytes=5_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def load_csv(data_path: Path) -> pd.DataFrame:
    if not data_path.exists():
        raise FileNotFoundError(f"{data_path} not found")

    if data_path.suffix != ".csv":
        raise ValueError("data_path must be a CSV file")

    return pd.read_csv(data_path)


def split_train_test(
    df: pd.DataFrame, target: str, test_size: float
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if target not in df.columns:
        raise ValueError(
            f"target must be a column of the dataframe: target={target}, columns={df.columns}"
        )

    x = df.drop(columns=target)
    y = df[target]

    return train_test_split(x, y, test_size=test_size, random_state=SEED)


def get_random_forest_model() -> RandomForestClassifier:
    return RandomForestClassifier(random_state=SEED)


def train_model(
    model: RandomForestClassifier,
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    logger: logging.Logger | None = None,
) -> RandomForestClassifier:
    logger = logger or logging.getLogger(__name__)

    logger.info("training_started")

    model.fit(x_train, y_train)
    logger.info("training_completed")

    y_pred = model.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)

    logger.info(f"model_evaluation: accuracy={round(accuracy, 4)}")

    logger.info(
        f"training_context: n_samples_train={x_train.shape[0]}, n_samples_test={x_test.shape[0]}, n_features={x_train.shape[1]}",
    )

    logger.info(f"model_params={model.get_params()}")

    return model


def save_model(model: RandomForestClassifier, model_path: Path) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)


def ml_pipeline(config: PipelineConfig, logger: logging.Logger) -> None:
    logger.info("pipeline_started")

    logger.info(f"loading_data | path={config.data_path}")

    try:
        df = load_csv(config.data_path)
    except Exception:
        logger.exception("data_loading_failed")
        raise

    logger.info(f"data_loaded | shape={df.shape}")

    logger.info(f"splitting_data | target={config.target}")

    try:
        x_train, x_test, y_train, y_test = split_train_test(
            df, config.target, config.test_size
        )
    except Exception:
        logger.exception("data_split_failed")
        raise

    logger.info(
        f"data_split_completed | train={x_train.shape[0]} | test={x_test.shape[0]}"
    )

    logger.info("initializing_model")
    model = get_random_forest_model()

    model = train_model(
        model,
        x_train,
        x_test,
        y_train,
        y_test,
        logger=logger,
    )

    logger.info(f"saving_model | path={config.model_path}")

    try:
        save_model(model, config.model_path)
    except Exception:
        logger.exception("model_saving_failed")
        raise

    logger.info("pipeline_completed")


if __name__ == "__main__":
    logger_config = LoggerConfig()
    logger = set_up_logger(name=logger_config.name, file_path=logger_config.logger_path)

    pipeline_config = PipelineConfig()
    ml_pipeline(config=pipeline_config, logger=logger)

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer

NUMERIC_FEATURES = [
    "air_temperature",
    "process_temperature",
    "rotational_speed",
    "torque",
    "tool_wear",
]

CATEGORICAL_FEATURES = ["type"]

TARGET = "machine_failure"

COLS_TO_DROP = ["UDI", "Product ID", "TWF", "HDF", "PWF", "OSF", "RNF"]

def load_raw_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    rename_map = {
        "Air temperature [K]": "air_temperature",
        "Process temperature [K]": "process_temperature",
        "Rotational speed [rpm]": "rotational_speed",
        "Torque [Nm]": "torque",
        "Tool wear [min]": "tool_wear",
        "Machine failure": "machine_failure",
        "Type": "type",
    }
    df = df.rename(columns=rename_map)

    # On filtre uniquement les colonnes presentes pour etre robuste
    # a des variantes du fichier CSV.
    cols_to_drop = [c for c in COLS_TO_DROP if c in df.columns]
    df = df.drop(columns=cols_to_drop)

    return df

def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["temp_delta"] = df["process_temperature"] - df["air_temperature"]
    df["power_proxy"] = df["rotational_speed"] * df["torque"]
    df["wear_per_rpm"] = df["tool_wear"] / (df["rotational_speed"] + 1e-6)
    return df


def get_feature_pipeline() -> ColumnTransformer:
    numeric_pipeline = Pipeline(steps=[
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("encoder", OrdinalEncoder(categories=[["L", "M", "H"]])),
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_pipeline, NUMERIC_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
    ])

    return preprocessor


def split_features_target(df: pd.DataFrame):
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    return X, y

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler


def load_raw_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df = df.drop(columns=["UDI", "Product ID", "TWF", "HDF", "PWF", "OSF", "RNF"])

    df = df.rename(
        columns={
            "Type": "type",
            "Air temperature [K]": "air_temperature",
            "Process temperature [K]": "process_temperature",
            "Rotational speed [rpm]": "rotational_speed",
            "Torque [Nm]": "torque",
            "Tool wear [min]": "tool_wear",
            "Machine failure": "machine_failure",
        }
    )

    return df


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df_eng_feat = df.copy()
    df_eng_feat["temp_delta"] = (
        df_eng_feat["process_temperature"] - df_eng_feat["air_temperature"]
    )
    df_eng_feat["power_proxy"] = df_eng_feat["rotational_speed"] * df_eng_feat["torque"]
    df_eng_feat["wear_per_rpm"] = df_eng_feat["tool_wear"] / (
        df_eng_feat["rotational_speed"] + 1e-6
    )
    return df_eng_feat


def get_feature_pipeline() -> ColumnTransformer:
    numeric_features = [
        "air_temperature",
        "process_temperature",
        "rotational_speed",
        "torque",
        "tool_wear",
    ]

    categorical_features = ["type"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OrdinalEncoder(categories=[["L", "M", "H"]]), categorical_features),
        ],
    )

    return preprocessor

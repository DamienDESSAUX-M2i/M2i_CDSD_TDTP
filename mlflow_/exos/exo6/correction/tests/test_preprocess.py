import pytest
import pandas as pd
import numpy as np

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.preprocess import (
    get_feature_pipeline,
    add_engineered_features,
    split_features_target,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "type": ["L", "M", "H", "M", "L"],
        "air_temperature": [298.1, 299.0, 300.5, 297.8, 301.2],
        "process_temperature": [308.6, 309.2, 310.1, 308.0, 311.5],
        "rotational_speed": [1551, 1408, 1862, 2000, 1200],
        "torque": [42.8, 55.1, 30.2, 25.0, 60.5],
        "tool_wear": [0, 100, 200, 50, 150],
        "machine_failure": [0, 0, 1, 0, 1],
    })

def test_pipeline_fit_transform_shape(sample_df):
    X = sample_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    preprocessor = get_feature_pipeline()
    X_transformed = preprocessor.fit_transform(X)

    assert X_transformed.shape[0] == len(sample_df)
    assert X_transformed.shape[1] == len(NUMERIC_FEATURES) + len(CATEGORICAL_FEATURES)


def test_numeric_features_are_scaled(sample_df):
    X = sample_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    preprocessor = get_feature_pipeline()
    X_transformed = preprocessor.fit_transform(X)

    numeric_cols = X_transformed[:, :len(NUMERIC_FEATURES)]
    assert abs(numeric_cols.mean()) < 1.0


def test_categorical_encoding(sample_df):
    X = sample_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    preprocessor = get_feature_pipeline()
    X_transformed = preprocessor.fit_transform(X)

    cat_col = X_transformed[:, -1]
    expected_map = {"L": 0.0, "M": 1.0, "H": 2.0}
    for i, t in enumerate(sample_df["type"].values):
        assert cat_col[i] == expected_map[t]


def test_temp_delta_computed(sample_df):
    df = add_engineered_features(sample_df)
    assert "temp_delta" in df.columns
    expected = sample_df["process_temperature"] - sample_df["air_temperature"]
    pd.testing.assert_series_equal(
        df["temp_delta"].reset_index(drop=True),
        expected.reset_index(drop=True),
        check_names=False,
    )

def test_wear_per_rpm_no_division_by_zero(sample_df):
    df_zero = sample_df.copy()
    df_zero["rotational_speed"] = 0
    df = add_engineered_features(df_zero)

    assert not df["wear_per_rpm"].isnull().any()
    assert not np.isinf(df["wear_per_rpm"]).any()


def test_original_df_not_mutated(sample_df):
    original_columns = set(sample_df.columns)
    _ = add_engineered_features(sample_df)
    assert set(sample_df.columns) == original_columns

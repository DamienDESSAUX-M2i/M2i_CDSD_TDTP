import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.preprocess import (
    add_engineered_features,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)

ENGINEERED = ["temp_delta", "power_proxy", "wear_per_rpm"]
ALL_FEATURES = NUMERIC_FEATURES + ENGINEERED + CATEGORICAL_FEATURES


def _build_synthetic_dataset(n: int = 500, seed: int = 42) -> tuple:
    # Cree un dataset synthetique dans les plages du dataset AI4I.
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "type": rng.choice(["L", "M", "H"], n),
        "air_temperature": rng.uniform(295, 305, n),
        "process_temperature": rng.uniform(305, 315, n),
        "rotational_speed": rng.uniform(1168, 2886, n),
        "torque": rng.uniform(3.8, 76.6, n),
        "tool_wear": rng.uniform(0, 253, n),
    })
    df = add_engineered_features(df)
    y = rng.choice([0, 1], n, p=[0.97, 0.03])
    return df[ALL_FEATURES], y


def _build_preprocessor():
    numeric_feats = NUMERIC_FEATURES + ENGINEERED
    return ColumnTransformer(transformers=[
        ("num", StandardScaler(), numeric_feats),
        ("cat", OrdinalEncoder(categories=[["L", "M", "H"]]), CATEGORICAL_FEATURES),
    ])


@pytest.fixture(scope="module")
def trained_pipeline():
    X, y = _build_synthetic_dataset()
    pipeline = Pipeline(steps=[
        ("preprocessor", _build_preprocessor()),
        ("classifier", RandomForestClassifier(
            n_estimators=50,
            class_weight="balanced",
            random_state=42,
        )),
    ])
    pipeline.fit(X, y)
    return pipeline, X, y


def test_probabilities_in_valid_range(trained_pipeline):
    pipeline, X, _ = trained_pipeline
    probas = pipeline.predict_proba(X)[:, 1]
    assert (probas >= 0.0).all()
    assert (probas <= 1.0).all()


def test_predictions_are_binary(trained_pipeline):
    pipeline, X, _ = trained_pipeline
    preds = pipeline.predict(X)
    assert set(preds).issubset({0, 1})

def test_model_is_not_trivial(trained_pipeline):
    pipeline, X, _ = trained_pipeline
    preds = pipeline.predict(X)
    assert preds.mean() > 0.0, (
        "Le modele predit uniquement la classe 0. "
        "Verifier class_weight='balanced' ou SMOTE."
    )

def test_deterministic_predictions(trained_pipeline):
    pipeline, X, _ = trained_pipeline
    preds_1 = pipeline.predict(X[:20])
    preds_2 = pipeline.predict(X[:20])
    np.testing.assert_array_equal(preds_1, preds_2)

def test_recall_above_threshold(trained_pipeline):
    from sklearn.metrics import recall_score
    pipeline, X, y = trained_pipeline
    preds = pipeline.predict(X)

    if y.sum() == 0:
        pytest.skip("Pas de positifs dans le jeu synthetique - skip SLA recall.")

    recall = recall_score(y, preds, zero_division=0)
    assert recall >= 0.3, (
        f"Recall trop faible : {recall:.3f} < 0.3. "
        "Verifier le reequilibrage des classes."
    )


def test_roc_auc_above_threshold(trained_pipeline):
    from sklearn.metrics import roc_auc_score
    pipeline, X, y = trained_pipeline

    if y.sum() == 0 or (y == 0).all():
        pytest.skip("Classes non representees - skip SLA AUC.")

    probas = pipeline.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, probas)
    assert auc >= 0.55, f"AUC-ROC trop faible : {auc:.3f} < 0.55."

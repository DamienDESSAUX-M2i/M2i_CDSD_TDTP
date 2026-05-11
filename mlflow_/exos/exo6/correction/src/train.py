import argparse
import os
import logging
import json

import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

from preprocess import (
    load_raw_data,
    add_engineered_features,
    get_feature_pipeline,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME = "predictive-maintenance"
MODEL_REGISTRY_NAME = "predictive-maintenance-model"
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ai4i2020.csv")

ENGINEERED_FEATURES = ["temp_delta", "power_proxy", "wear_per_rpm"]
ALL_FEATURES = NUMERIC_FEATURES + ENGINEERED_FEATURES + CATEGORICAL_FEATURES


def _build_preprocessor() -> ColumnTransformer:
    numeric_feats = NUMERIC_FEATURES + ENGINEERED_FEATURES
    categorical_feats = CATEGORICAL_FEATURES

    numeric_pipeline = Pipeline(steps=[("scaler", StandardScaler())])
    categorical_pipeline = Pipeline(steps=[
        ("encoder", OrdinalEncoder(categories=[["L", "M", "H"]]))
    ])

    return ColumnTransformer(transformers=[
        ("num", numeric_pipeline, numeric_feats),
        ("cat", categorical_pipeline, categorical_feats),
    ])


def _get_classifier(model_name: str, n_estimators: int, max_depth):
    if model_name == "rf":
        return RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        )
    if model_name == "gb":
        return GradientBoostingClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth if max_depth else 4,
            random_state=42,
        )
    raise ValueError(f"Modele inconnu : {model_name}. Valeurs acceptees : rf, gb.")


def _compute_metrics(y_true, y_pred, y_proba) -> dict:
    return {
        "f1_score": round(f1_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_proba), 4),
    }


def train(
    model_name: str = "rf",
    test_size: float = 0.2,
    use_smote: bool = True,
    n_estimators: int = 150,
    max_depth: int = None,
    register_model: bool = True,
) -> tuple:

    logger.info("Chargement des donnees : %s", DATA_PATH)
    df = load_raw_data(DATA_PATH)
    df = add_engineered_features(df)

    X = df[ALL_FEATURES]
    y = df["machine_failure"]

    logger.info(f"Dataset :{len(df)} lignes | Taux de pannes : {y.mean() * 100}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42,
        stratify=y,
    )
    logger.info(f"Train : {len(X_train)} | Test : {len(X_test)}")

    preprocessor = _build_preprocessor()
    classifier = _get_classifier(model_name, n_estimators, max_depth)

    if use_smote:
        pipeline = ImbPipeline(steps=[
            ("preprocessor", preprocessor),
            ("smote", SMOTE(random_state=42)),
            ("classifier", classifier),
        ])
    else:
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ])

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        logger.info(f"MLflow Run ID : {run_id}")

        mlflow.log_params({
            "model_name": model_name,
            "n_estimators": n_estimators,
            "use_smote": use_smote,
            "test_size": test_size,
            "max_depth": str(max_depth),
            "n_features": len(ALL_FEATURES),
        })

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_results = cross_validate(
            pipeline, X_train, y_train,
            cv=cv,
            scoring=["f1", "roc_auc", "recall"],
            return_train_score=False,
        )
        cv_f1_mean = round(cv_results["test_f1"].mean(), 4)
        cv_f1_std = round(cv_results["test_f1"].std(), 4)
        mlflow.log_metric("cv_f1_mean", cv_f1_mean)
        mlflow.log_metric("cv_f1_std", cv_f1_std)
        mlflow.log_metric("cv_roc_auc_mean",
                          round(cv_results["test_roc_auc"].mean(), 4))

        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        y_proba = pipeline.predict_proba(X_test)[:, 1]
        metrics = _compute_metrics(y_test, y_pred, y_proba)
        mlflow.log_metrics(metrics)

        logger.info(f"Metriques test : {json.dumps(metrics)}")
        logger.info(f"\n{classification_report(
            y_test, y_pred, target_names=["OK", "Panne"]
        )}")

        # Artefact : matrice de confusion
        cm = confusion_matrix(y_test, y_pred)
        cm_text = (
            f"Confusion Matrix\n{cm}\n"
            f"TN={cm[0,0]}  FP={cm[0,1]}  FN={cm[1,0]}  TP={cm[1,1]}"
        )
        mlflow.log_text(cm_text, "confusion_matrix.txt")

        # Artefact : importances de features (RandomForest uniquement)
        if hasattr(pipeline.named_steps["classifier"], "feature_importances_"):
            fi = pipeline.named_steps["classifier"].feature_importances_
            fi_dict = dict(zip(ALL_FEATURES, fi.tolist()))
            mlflow.log_dict(fi_dict, "feature_importances.json")

        mlflow.set_tags({
            "domain": "predictive-maintenance",
            "dataset": "AI4I-2020",
        })

        input_example = X_train.iloc[:3]

        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            input_example=input_example,
            registered_model_name=MODEL_REGISTRY_NAME if register_model else None,
        )

        logger.info(
            f"Run termine. F1={metrics["f1_score"]} | Recall={metrics["recall"]} | ROC-AUC={metrics["roc_auc"]}"
        )

        return run_id, metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Entrainement MLOps - Maintenance Predictive"
    )
    parser.add_argument("--model", default="rf", choices=["rf", "gb"])
    parser.add_argument("--n-estimators", type=int, default=150)
    parser.add_argument("--max-depth", type=int, default=None)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--no-smote", action="store_true")
    parser.add_argument("--no-register", action="store_true")
    args = parser.parse_args()

    train(
        model_name=args.model,
        test_size=args.test_size,
        use_smote=not args.no_smote,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        register_model=not args.no_register,
    )

import os
from pathlib import Path

import mlflow
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as Pipeline
from mlflow.tracking import MlflowClient
from preprocess import add_engineered_features, get_feature_pipeline, load_raw_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

PROJECT_DIR = Path(__file__).parent.parent.resolve()
DATA_PATH = PROJECT_DIR / "data" / "ai4i2020.csv"

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "predictive-maintenance")
RUN_NAME = os.getenv("RUN_NAME", "random-forest")
REGISTERED_MODEL_NAME = os.getenv("REGISTRY_MODEL_NAME", "predictive-maintenance-model")

SEED = 42
TEST_SIZE = 0.2


def train():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    client = MlflowClient()

    with mlflow.start_run(run_name=RUN_NAME):
        df = load_raw_data(DATA_PATH)
        df_eng_feat = add_engineered_features(df)

        target_name = "machine_failure"
        features = df_eng_feat.drop(columns=target_name)
        target = df_eng_feat[target_name]

        features_train, features_test, target_train, target_test = train_test_split(
            features, target, stratify=target, test_size=TEST_SIZE, random_state=SEED
        )

        mlflow.log_param("test_size", TEST_SIZE)
        mlflow.log_param("random_state", SEED)

        preprocess = get_feature_pipeline()

        n_estimators = 100

        pipeline = Pipeline(
            steps=[
                ("preprocess", preprocess),
                ("smote", SMOTE(random_state=SEED)),
                (
                    "clf",
                    RandomForestClassifier(
                        n_estimators=n_estimators,
                        class_weight="balanced",
                        random_state=SEED,
                    ),
                ),
            ]
        )

        mlflow.log_param("model_name", "RandomForest")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("use_smote", True)

        stratified_k_fold = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        cv_results = cross_validate(
            estimator=pipeline,
            X=features_train,
            y=target_train,
            cv=stratified_k_fold,
            scoring="f1",
            return_train_score=True,
            n_jobs=-1,
        )
        mlflow.log_metric("cv_f1_mean", cv_results["test_score"].mean())
        mlflow.log_metric("cv_f1_std", cv_results["test_score"].std())

        pipeline.fit(features_train, target_train)

        target_predict = pipeline.predict(features_test)
        target_probability = pipeline.predict_proba(features_test)[:, 1]

        f1 = f1_score(target_test, target_predict)
        recall = recall_score(target_test, target_predict)
        precision = precision_score(target_test, target_predict)
        roc_auc = roc_auc_score(target_test, target_probability)

        mlflow.log_metric("recall", recall)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("roc_auc", roc_auc)
        mlflow.log_metric("f1_score", f1)

        mlflow.set_tags(
            {"stage": "training", "model_type": "RandomForest", "smote": "true"}
        )

        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            registered_model_name=REGISTERED_MODEL_NAME,
        )

        latest_version = client.get_latest_versions(
            REGISTERED_MODEL_NAME, stages=["None"]
        )[0]

        client.transition_model_version_stage(
            name=REGISTERED_MODEL_NAME,
            version=latest_version.version,
            stage="Production",
            archive_existing_versions=True,
        )


if __name__ == "__main__":
    train()

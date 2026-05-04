from datetime import datetime

import mlflow
import pandas as pd
from mlflow.entities import Experiment, Run
from mlflow.store.entities import PagedList
from mlflow.tracking import MlflowClient
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

import numpy as np

RANDOM_STATE = 42
EXPERIMENT_NAME = "spam_detection"


def make_dataset() -> None:
    return make_classification(
        n_samples=1500,
        n_features=18,
        n_informative=10,
        random_state=RANDOM_STATE,
    )


def split_dataset(
    x: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return train_test_split(
        x,
        y,
        stratify=y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )


def get_or_create_experiment(client: MlflowClient, name: str, tags: dict) -> str:
    experiment = client.get_experiment_by_name(name=name)

    if experiment:
        experiment_id = experiment.experiment_id

        if experiment.lifecycle_stage == "deleted":
            client.restore_experiment(experiment_id)
            print("Experiment restored")
            return experiment_id

        else:
            print("Experiment already exists")
            return experiment_id

    else:
        experiment_id = client.create_experiment(
            name=name,
            tags={"team": "data-science", "project": "spam-v1", "owner": "ddx1"},
        )
        print("Experiment created")
        return experiment_id


def setup_mlflow() -> tuple[MlflowClient, Experiment]:
    mlflow.set_tracking_uri("http://localhost:5000")
    client = MlflowClient()

    print(f"Tracking uri : {mlflow.get_tracking_uri()}")

    experiment_id = get_or_create_experiment(
        client=client,
        name=EXPERIMENT_NAME,
        tags={
            "team": "data-science",
            "project": "spam-v1",
            "owner": "ddx1",
        },
    )
    experiment = client.get_experiment(experiment_id=experiment_id)

    print(f"Experiment ID: {experiment_id}")
    print(f"Experiment lifecycle_stage: {experiment.lifecycle_stage}")

    mlflow.set_experiment(experiment_id=experiment_id)

    return client, experiment


def start_runs(client: MlflowClient, experiment: Experiment) -> list[str]:
    x, y = make_dataset()
    x_train, x_test, y_train, y_test = split_dataset(x, y)

    param_grid = [
        {
            "run_name": "rf_trial_1",
            "model_type": "random_forest",
            "n_estimators": 50,
            "max_depth": 3,
        },
        {
            "run_name": "rf_trial_2",
            "model_type": "random_forest",
            "n_estimators": 100,
            "max_depth": 5,
        },
        {
            "run_name": "logreg_trial_1",
            "model_type": "logistic_regression",
            "C": 0.1,
            "max_iter": 200,
        },
        {
            "run_name": "logreg_trial_2",
            "model_type": "logistic_regression",
            "C": 1,
            "max_iter": 200,
        },
    ]

    run_ids = []

    for params in param_grid:
        model_type = params["model_type"]
        run_name = params["run_name"]

        run = client.create_run(
            experiment_id=experiment.experiment_id,
            run_name=run_name,
            tags={"model_type": model_type},
        )

        run_id = run.info.run_id
        run_ids.append(run_id)

        try:
            for k, v in params.items():
                if k not in ["run_name"]:
                    client.log_param(run_id, k, v)
            client.log_param(run_id, "model_type", model_type)

            if model_type == "random_forest":
                model = RandomForestClassifier(
                    n_estimators=params["n_estimators"],
                    max_depth=params["max_depth"],
                    random_state=RANDOM_STATE,
                )

            elif model_type == "logistic_regression":
                model = LogisticRegression(
                    C=params["C"],
                    max_iter=params["max_iter"],
                    random_state=RANDOM_STATE,
                )

            else:
                raise ValueError(f"model_type not supported: model_type={model_type}")

            model.fit(x_train, y_train)
            cv_score = cross_val_score(
                model,
                x_train,
                y_train,
                cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
                scoring="accuracy",
            )
            client.log_metric(run_id, "cv_score", cv_score.mean())

            y_pred = model.predict(x_test)
            y_proba = model.predict_proba(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_proba)
            f1 = f1_score(y_test, y_pred)

            client.log_metric(run_id, "test_accuracy", accuracy)
            client.log_metric(run_id, "test_roc_auc", roc_auc)
            client.log_metric(run_id, "test_f1_score", f1)

            mlflow.sklearn.log_model(model, run_id=run_id)

            client.set_terminated(run_id, status="FINISHED")

        except Exception as e:
            print(e)
            client.set_terminated(run_id, status="FAILED")


def get_runs(client: MlflowClient, experiment: Experiment) -> PagedList[Run]:
    return client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.test_roc_auc DESC"],
    )


if __name__ == "__main__":
    client, experiment = setup_mlflow()
    run_ids = start_runs(client=client, experiment=experiment)

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.test_roc_auc DESC"],
    )
    for run in runs:
        print(f"Run name: {run.info.run_name}")
        print(f"  test_accuracy : {run.data.metrics.get('test_accuracy', 0)}")
        print(f"  test_roc_auc : {run.data.metrics.get('test_roc_auc', 0)}")
        print()

    filtered_test_roc_auc = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="metrics.test_roc_auc > 0.85",
        order_by=["metrics.test_roc_auc DESC"],
    )
    print(f"Number of runs such that test_roc_auc > 0.85: {len(filtered_test_roc_auc)}")

    filtered_rf = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="tags.model_type = 'random_forest'",
        order_by=["metrics.accuracy DESC"],
    )
    print(f"Number of runs such that model_type = 'random_forest': {len(filtered_rf)}")

    filtered_rf_test_accuracy = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="metrics.test_accuracy > 0.88 AND tags.model_type = 'random_forest'",
        order_by=["metrics.test_roc_auc DESC"],
    )
    print(
        f"Number of runs such that test_accuracy > 0.88 AND model_type = 'random_forest': {len(filtered_rf_test_accuracy)}"
    )

    runs_data = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="attributes.status = 'FINISHED'",
    )

    df = pd.DataFrame(
        [
            {
                "run_name": r.info.run_name,
                "model_type": r.data.tags.get("model_type", ""),
                "cv_score": r.data.metrics.get("cv_score", None),
                "test_accuracy": r.data.metrics.get("test_accuracy", None),
                "test_f1": r.data.metrics.get("test_f1", None),
                "test_roc_auc": r.data.metrics.get("test_roc_auc", None),
                "run_id": r.info.run_id,
            }
            for r in runs_data
        ]
    )

    df.sort_values("test_roc_auc", ascending=False)
    print(df)

    best_row = df.iloc[0]
    best_run_id = best_row["run_id"]

    print(f"Best run : {best_row['run_name']}")
    print(f"Best run id : {best_run_id}")
    print(f"Best accuracy : {best_row['test_accuracy']}")
    print(f"Best roc auc : {best_row['test_roc_auc']}")

    client.set_tag(best_run_id, "status", "champion")
    client.set_tag(best_run_id, "promoted_at", datetime.now().strftime("%Y-%m-%d"))

    updated_run = client.get_run(best_run_id)
    print(updated_run.data.tags)

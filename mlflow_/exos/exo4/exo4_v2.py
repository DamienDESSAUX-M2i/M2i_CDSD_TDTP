from dataclasses import dataclass
from datetime import datetime

import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

import numpy as np


@dataclass(frozen=True)
class Config:
    tracking_uri: str = "http://localhost:5000"
    experiment_name: str = "spam_detection"
    random_state: int = 42
    test_size: float = 0.2


class DataModule:
    def __init__(self, config: Config):
        self.config = config

    def load(self) -> tuple[np.ndarray, np.ndarray]:
        return make_classification(
            n_samples=1500,
            n_features=18,
            n_informative=10,
            random_state=self.config.random_state,
        )

    def split(
        self, x: np.ndarray, y: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return train_test_split(
            x,
            y,
            stratify=y,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
        )


class ModelFactory:
    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def build(params: dict):
        model_type = params["model_type"]

        if model_type == "random_forest":
            return RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                random_state=config.random_state,
            )

        if model_type == "logistic_regression":
            return LogisticRegression(
                C=params["C"],
                max_iter=params["max_iter"],
                random_state=config.random_state,
            )

        raise ValueError(f"Unsupported model_type={model_type}")


class MLflowService:
    def __init__(self, config: Config):
        mlflow.set_tracking_uri(config.tracking_uri)
        self.client = MlflowClient()
        self.config = config

    def setup_experiment(self) -> str:
        exp = self.client.get_experiment_by_name(self.config.experiment_name)

        if exp:
            if exp.lifecycle_stage == "deleted":
                self.client.restore_experiment(exp.experiment_id)
            experiment_id = exp.experiment_id
        else:
            experiment_id = self.client.create_experiment(
                name=self.config.experiment_name,
                tags={"team": "data-science", "project": "spam-v1"},
            )

        mlflow.set_experiment(experiment_id=experiment_id)
        return experiment_id

    def start_run(self, experiment_id: str, run_name: str, tags: dict):
        return self.client.create_run(
            experiment_id=experiment_id,
            run_name=run_name,
            tags=tags,
        )

    def finalize_run(self, run_id: str, status: str):
        self.client.set_terminated(run_id, status=status)


class Trainer:
    def __init__(self, config: Config):
        self.config = config

    def train_and_evaluate(
        self,
        model: RandomForestClassifier | LogisticRegression,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_test: np.ndarray,
        y_test: np.ndarray,
    ) -> dict:
        model.fit(x_train, y_train)

        cv_accuracy = cross_val_score(
            model,
            x_train,
            y_train,
            cv=StratifiedKFold(
                n_splits=5, shuffle=True, random_state=self.config.random_state
            ),
            scoring="accuracy",
        )

        y_pred = model.predict(x_test)
        y_proba = model.predict_proba(x_test)

        return {
            "cv_accuracy_mean": cv_accuracy.mean(),
            "cv_accuracy_std": cv_accuracy.std(),
            "test_accuracy": accuracy_score(y_test, y_pred),
            "test_f1": f1_score(y_test, y_pred),
            "test_roc_auc": roc_auc_score(y_test, y_proba),
        }


class ExperimentRunner:
    def __init__(self, config: Config):
        self.config = config
        self.data = DataModule(config)
        self.trainer = Trainer(config)
        self.tracking = MLflowService(config)

    def run(self, param_grid: list[dict]) -> list[str]:
        experiment_id = self.tracking.setup_experiment()

        x, y = self.data.load()
        x_train, x_test, y_train, y_test = self.data.split(x, y)

        run_ids = []

        for params in param_grid:
            run = self.tracking.start_run(
                experiment_id,
                run_name=params["run_name"],
                tags={"model_type": params["model_type"]},
            )

            run_id = run.info.run_id
            run_ids.append(run_id)

            try:
                for k, v in params.items():
                    if k != "run_name":
                        self.tracking.client.log_param(run_id, k, v)

                model = ModelFactory(config).build(params)

                metrics = self.trainer.train_and_evaluate(
                    model, x_train, y_train, x_test, y_test
                )

                for k, v in metrics.items():
                    self.tracking.client.log_metric(run_id, k, v)

                mlflow.sklearn.log_model(model, run_id=run_id)

                self.tracking.finalize_run(run_id, "FINISHED")

            except Exception as e:
                print(f"[ERROR] run_id={run_id} -> {e}")
                self.tracking.finalize_run(run_id, "FAILED")

        return run_ids


class RunAnalyzer:
    def __init__(self, client: MlflowClient, experiment_id: str):
        self.client = client
        self.experiment_id = experiment_id

    def to_dataframe(self) -> pd.DataFrame:
        runs = self.client.search_runs(
            [self.experiment_id],
            filter_string="attributes.status = 'FINISHED'",
        )

        return pd.DataFrame(
            [
                {
                    "run_name": r.info.run_name,
                    "model_type": r.data.tags.get("model_type"),
                    "cv_accuracy_mean": r.data.metrics.get("cv_accuracy_mean"),
                    "cv_accuracy_std": r.data.metrics.get("cv_accuracy_std"),
                    "test_accuracy": r.data.metrics.get("test_accuracy"),
                    "test_f1": r.data.metrics.get("test_f1"),
                    "test_roc_auc": r.data.metrics.get("test_roc_auc"),
                    "run_id": r.info.run_id,
                }
                for r in runs
            ]
        )

    def promote_best(self, df: pd.DataFrame):
        df = df.sort_values("test_roc_auc", ascending=False)
        best = df.iloc[0]

        self.client.set_tag(best["run_id"], "status", "champion")
        self.client.set_tag(
            best["run_id"],
            "promoted_at",
            datetime.now().strftime("%Y-%m-%d"),
        )

        return best


if __name__ == "__main__":
    config = Config()

    param_grid = [
        {
            "run_name": "rf_1",
            "model_type": "random_forest",
            "n_estimators": 50,
            "max_depth": 3,
        },
        {
            "run_name": "rf_2",
            "model_type": "random_forest",
            "n_estimators": 100,
            "max_depth": 5,
        },
        {
            "run_name": "lr_1",
            "model_type": "logistic_regression",
            "C": 0.1,
            "max_iter": 200,
        },
        {
            "run_name": "lr_2",
            "model_type": "logistic_regression",
            "C": 1,
            "max_iter": 200,
        },
    ]

    runner = ExperimentRunner(config)
    run_ids = runner.run(param_grid)

    client = runner.tracking.client
    experiment = client.get_experiment_by_name(config.experiment_name)

    analyzer = RunAnalyzer(client, experiment.experiment_id)
    df = analyzer.to_dataframe()

    print(df.sort_values("test_roc_auc", ascending=False))

    best = analyzer.promote_best(df)

    print("\nBest run:")
    print(best)

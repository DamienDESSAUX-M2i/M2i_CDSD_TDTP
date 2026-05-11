import logging
import os

import mlflow
from imblearn.pipeline import Pipeline
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME = os.getenv("EXPERIMENT_NAME", "predictive-maintenance")
REGISTERED_MODEL_NAME = os.getenv("REGISTRY_MODEL_NAME", "predictive-maintenance-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")


logging.basicConfig(level=logging.INFO)


class ModelLoader:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        self.client = MlflowClient()

        self.model: Pipeline | None = None
        self.is_loaded: bool = False
        self.version: str | None = None
        self.source: str | None = None

        self._load_model()

    def _load_model(self):
        try:
            model_uri = f"models:/{REGISTERED_MODEL_NAME}/{MODEL_STAGE}"
            self.model = mlflow.pyfunc.load_model(model_uri)

            latest_versions = self.client.get_latest_versions(
                REGISTERED_MODEL_NAME, stages=[MODEL_STAGE]
            )

            if latest_versions:
                self.version = latest_versions[0].version

            self.is_loaded = True
            self.source = "registry"

            self.logger.info(
                f"Model loaded from registry: {REGISTERED_MODEL_NAME} "
                f"(stage={MODEL_STAGE}, version={self.version})"
            )
            return

        except Exception as e:
            self.logger.warning(f"Registry load failed: {e}")

        try:
            experiment = self.client.get_experiment_by_name(EXPERIMENT_NAME)

            if experiment is None:
                raise ValueError("Experiment not found")

            runs = self.client.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["attributes.start_time DESC"],
                max_results=1,
            )

            if not runs:
                raise ValueError("No runs found")

            run = runs[0]
            run_id = run.info.run_id

            model_uri = f"runs:/{run_id}/model"
            self.model = mlflow.pyfunc.load_model(model_uri)

            self.version = run_id
            self.is_loaded = True
            self.source = "experiment"

            self.logger.info(f"Model loaded from experiment: run_id={run_id}")

        except Exception as e:
            self.logger.error(f"Fallback load failed: {e}")
            self.model = None
            self.is_loaded = False

    def predict(self, X):
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        try:
            return self.model.predict(X)
        except Exception as e:
            self.logger.error(f"Prediction error: {e}")
            raise

    def predict_proba(self, X):
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        if not hasattr(self.model, "predict_proba"):
            self.logger.warning("predict_proba not available on this model")
            raise NotImplementedError("predict_proba not supported")

        try:
            return self.model.predict_proba(X)
        except Exception as e:
            self.logger.error(f"Predict_proba error: {e}")
            raise

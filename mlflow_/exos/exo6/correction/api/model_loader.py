import os
import logging
import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "predictive-maintenance-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "latest")


class ModelLoader:

    _instance = None
    _model = None
    _model_version = "unknown"


    def load(self) -> None:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

        # Tentative 1 : Model Registry
        try:
            model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
            logger.info(f"Chargement du modele depuis : {model_uri}")
            self._model = mlflow.sklearn.load_model(model_uri)

            client = mlflow.MlflowClient()
            versions = client.get_latest_versions(MODEL_NAME)
            if versions:
                self._model_version = versions[-1].version

            logger.info(f"Modele charge - version {self._model_version}")
            return

        except Exception as exc:
            logger.warning(
                f"Model Registry indisponible ({exc}). Tentative depuis les runs..."
            )

        # Tentative 2 : dernier run de l'experience
        try:
            client = mlflow.MlflowClient()
            experiment = client.get_experiment_by_name("predictive-maintenance")
            if experiment is None:
                raise RuntimeError("Experience 'predictive-maintenance' introuvable.")

            runs = client.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["start_time DESC"],
                max_results=1,
            )
            if not runs:
                raise RuntimeError("Aucun run disponible dans l'experience.")

            run_id = runs[0].info.run_id
            model_uri = f"runs:/{run_id}/model"
            self._model = mlflow.sklearn.load_model(model_uri)
            self._model_version = f"run-{run_id[:8]}"
            logger.info(f"Modele charge depuis le run {run_id}")

        except Exception as exc:
            logger.error(f"Impossible de charger le modele : {exc}")
            self._model = None

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def version(self) -> str:
        return self._model_version

    def predict(self, X):
        if not self.is_loaded:
            raise RuntimeError("Modele non charge.")
        return self._model.predict(X)

    def predict_proba(self, X):
        if not self.is_loaded:
            raise RuntimeError("Modele non charge.")
        return self._model.predict_proba(X)[:, 1]


model_loader = ModelLoader()

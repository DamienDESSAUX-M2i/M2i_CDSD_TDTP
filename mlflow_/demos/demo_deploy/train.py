import os

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42, test_size=0.2
)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

mlflow.set_experiment("deploy-demo")

with mlflow.start_run(run_name="random-forest"):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    mlflow.log_params({"n_estimators": 100, "random_state": 42})
    mlflow.log_metric("test_accuracy", accuracy)

    mlflow.sklearn.log_model(model, "model", registered_model_name="iris-api-model")

client = MlflowClient()

client.transition_model_version_stage(
    name="iris-api-model", version=1, stage="Production", archive_existing_versions=True
)

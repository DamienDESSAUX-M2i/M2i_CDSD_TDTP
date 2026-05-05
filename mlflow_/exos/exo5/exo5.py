import mlflow
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

SEED = 42
EXPERIMENT_NAME = "iris-classification"
MODEL_NAME = "iris_classifier"

x, y = load_iris(return_X_y=True)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=SEED
)

mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name="random-forest"):
    mlflow.set_tag("model_type", "RandomForest")
    mlflow.set_tag("dataset", "iris")

    model = RandomForestClassifier(random_state=SEED)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.log_metric("accuracy", accuracy)

    # registered_model_name=MODEL_NAME ajouter au registry
    mlflow.sklearn.log_model(model, "model", registered_model_name=MODEL_NAME)

with mlflow.start_run(run_name="logistic-regression"):
    mlflow.set_tag("model_type", "LogisticRegression")
    mlflow.set_tag("dataset", "iris")

    model = LogisticRegression(random_state=SEED)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(model, "model", registered_model_name=MODEL_NAME)

client = MlflowClient()

versions = client.search_model_versions(f"name='{MODEL_NAME}'")

# Trouver la meilleure version
best_version = None
best_accuracy = 0

for v in versions:
    run = client.get_run(v.run_id)
    accuracy = run.data.metrics.get("accuracy", 0)

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_version = v

# Promouvoir en Production
if best_version:
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=best_version.version,
        stage="Production",
        archive_existing_versions=True,
    )

    print(
        f"\nVersion {best_version.version} promue en Production (accuracy: {best_accuracy:.4f})"
    )

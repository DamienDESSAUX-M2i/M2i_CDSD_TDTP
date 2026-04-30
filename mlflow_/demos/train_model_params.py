import mlflow
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

x, y = load_wine(return_X_y=True)

test_size = 0.2
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size, random_state=42
)

mlflow.set_experiment("wine-classification")

configs = [
    {"n_estimators": 50, "max_depth": 3},
    {"n_estimators": 100, "max_depth": 5},
    {"n_estimators": 200, "max_depth": 10},
    {"n_estimators": 150, "max_depth": 7},
]

for i, config in enumerate(configs, 1):
    with mlflow.start_run(run_name=f"config-{i}"):
        mlflow.log_params(config)

        model = RandomForestClassifier(**config, random_state=42)
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")
        f1 = f1_score(y_test, y_pred, average="weighted")

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)

        mlflow.sklearn.log_model(model, "model-random-forest")

        print("Model saved")

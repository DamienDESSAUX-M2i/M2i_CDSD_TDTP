import time
from itertools import product

import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

x, y = load_wine(return_X_y=True)

test_size = 0.2
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size, random_state=42
)

mlflow.set_experiment("wine-classification")

n_estimators = [50, 100, 150, 200]
max_depths = [3, 5, 7, 10]
random_state = 42

metrics = []

for k, (n_estimator, max_depth) in enumerate(product(n_estimators, max_depths), 1):
    with mlflow.start_run(run_name=f"random-forest-config-{k}"):
        mlflow.set_tag("model_type", "RandomForest")
        mlflow.set_tag("dataset", "wine")
        mlflow.set_tag("version", "1.0.0")
        mlflow.set_tag("developer", "ddx1")

        mlflow.log_param("n_estimator", n_estimator)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("test_size", test_size)

        model = RandomForestClassifier(
            n_estimators=n_estimator, max_depth=max_depth, random_state=random_state
        )

        start_training = time.time()
        model.fit(x_train, y_train)
        training_time = time.time() - start_training

        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")
        f1 = f1_score(y_test, y_pred, average="weighted")

        metrics.append(
            {
                "model": "RandomForest",
                "n_estimator": n_estimator,
                "max_depth": max_depth,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "training_time": training_time,
            }
        )

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("training_time", training_time)

        mlflow.sklearn.log_model(model, f"model-random-forest-config-{k}")

        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(cm)
        disp.plot()
        plt.title("Confusion matrix")
        mlflow.log_figure(plt.gcf(), f"confusion_matrix-config-{k}.png")
        plt.close()

        feature_importance = model.feature_importances_
        plt.figure(figsize=(7, 5))
        plt.bar(range(len(feature_importance)), feature_importance)
        plt.xlabel("Feature Index")
        plt.ylabel("Importance")
        plt.title("Feature importance")
        mlflow.log_figure(plt.gcf(), f"feature_importance-config-{k}.png")
        plt.close()

metrics_df = pd.DataFrame(metrics)
best_model = metrics_df.sort_values("accuracy", ascending=False).loc[0]
print("Best model:")
print("  n_estimator: ", best_model["n_estimator"])
print("  max_depth: ", best_model["max_depth"])

with mlflow.start_run(run_name="random-forest-metrics"):
    mlflow.log_text(metrics_df.to_string(index=False), "metrics.txt")

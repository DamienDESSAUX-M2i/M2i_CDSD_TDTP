import time

import mlflow
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

x, y = load_wine(return_X_y=True)

test_size = 0.2
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size, random_state=42
)

metrics = []

mlflow.set_experiment("wine-classification")

with mlflow.start_run(run_name="random-forest"):
    mlflow.set_tag("model_type", "RandomForest")
    mlflow.set_tag("algorithm_family", "ensemble")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    random_state = 42

    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)

    model = RandomForestClassifier(random_state=random_state)

    start_training = time.time()
    model.fit(x_train, y_train)
    training_time = time.time() - start_training

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("training_time", training_time)

    mlflow.sklearn.log_model(model, "model-random-forest")

    metrics.append(
        {
            "model": "RandomForest",
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "training_time": training_time,
        }
    )

with mlflow.start_run(run_name="gradient-boosting"):
    mlflow.set_tag("model_type", "GradientBoosting")
    mlflow.set_tag("algorithm_family", "ensemble")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    random_state = 42

    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)

    model = GradientBoostingClassifier(random_state=random_state)

    start_training = time.time()
    model.fit(x_train, y_train)
    training_time = time.time() - start_training

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("training_time", training_time)

    mlflow.sklearn.log_model(model, "model-gradient-boosting")

    metrics.append(
        {
            "model": "GradientBoosting",
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "training_time": training_time,
        }
    )

with mlflow.start_run(run_name="logistic-regression"):
    mlflow.set_tag("model_type", "LogisticRegression")
    mlflow.set_tag("algorithm_family", "linear")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    random_state = 42

    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)

    model = LogisticRegression(random_state=random_state)

    start_training = time.time()
    model.fit(x_train, y_train)
    training_time = time.time() - start_training

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("training_time", training_time)

    mlflow.sklearn.log_model(model, "model-logistic-regression")

    metrics.append(
        {
            "model": "LogisticRegression",
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "training_time": training_time,
        }
    )

with mlflow.start_run(run_name="svm"):
    mlflow.set_tag("model_type", "SVM")
    mlflow.set_tag("algorithm_family", "svm")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    random_state = 42

    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)

    model = SVC(random_state=random_state)

    start_training = time.time()
    model.fit(x_train, y_train)
    training_time = time.time() - start_training

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("training_time", training_time)

    mlflow.sklearn.log_model(model, "model-svm")

    metrics.append(
        {
            "model": "SVM",
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "training_time": training_time,
        }
    )

metrics_df = pd.DataFrame(metrics)
print(metrics_df.head(4))

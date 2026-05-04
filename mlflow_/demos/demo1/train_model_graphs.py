import matplotlib.pyplot as plt
import mlflow
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

with mlflow.start_run(run_name="random-forest-baseline"):
    mlflow.set_tag("model_type", "RandomForest")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    n_estimator = 100
    max_depth = 5
    random_state = 42

    mlflow.log_param("n_estimator", n_estimator)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("test_size", test_size)

    model = RandomForestClassifier(
        n_estimators=n_estimator, max_depth=max_depth, random_state=random_state
    )
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

    # Méthode 1 : Sauvegarde locale

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.title("Confusion matrix")
    plt.savefig("confusion_matrix.png")
    mlflow.log_artifact("confusion_matrix.png")
    plt.close()

    # Méthode 2 : Sans sauvegarde locale

    feature_importance = model.feature_importances_
    plt.figure(figsize=(7, 5))
    plt.bar(range(len(feature_importance)), feature_importance)
    plt.xlabel("Feature Index")
    plt.ylabel("Importance")
    plt.title("Feature importance")
    mlflow.log_figure(plt.gcf(), "feature_importance.png")
    plt.close()

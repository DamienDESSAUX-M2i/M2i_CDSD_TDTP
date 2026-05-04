from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import mlflow

X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "RandomForest": {
        "model": RandomForestClassifier(n_estimators=100, random_state=42),
        "family": "ensemble"
    },
    "GradientBoosting": {
        "model": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "family": "ensemble"
    },
    "LogisticRegression": {
        "model": LogisticRegression(random_state=42, max_iter=1000),
        "family": "linear"
    },
    "SVC": {
        "model": SVC(random_state=42),
        "family": "SVM"
    }
}

mlflow.set_experiment("model-comparaison")

results = []

for model_name, model_info in models.items():
    print(f"Entraînement de {model_name}")

    with mlflow.start_run(run_name=model_name):
        mlflow.set_tag("model_type", model_name)
        mlflow.set_tag("algo_family", model_info["family"])

        model = model_info["model"]
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        precision = precision_score(y_test, y_pred, average="weighted")
        recall = recall_score(y_test, y_pred, average="weighted")

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)

        mlflow.sklearn.log_model(model, "model")

        results.append({
            "model": model_name,
            "accuracy": accuracy,
            "f1": f1,
            "precision": precision,
            "recall": recall
        })

best = max(results, key=lambda x: x["accuracy"])

print(f"Meilleur modèle : {best['model']}")

for r in results:
    print(r)
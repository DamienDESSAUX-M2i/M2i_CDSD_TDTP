from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix
import mlflow
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mlflow.tracking import MlflowClient
from itertools import product

mlflow.set_experiment("exercice2")

X,y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

n_estimators_list = [50, 100, 150, 200]
max_depth_list = [3, 5, 7, 10]
random_state = 42
test_size = 0.2

result = []

for n_estimators, max_depth in product(n_estimators_list, max_depth_list):

    run_name = f"RF_{n_estimators}_{max_depth}"

    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("test_size", test_size)

        mlflow.set_tag("model_type", "RandomForest")
        mlflow.set_tag("developer", "Formation")
        mlflow.set_tag("dataset", "wine quality")

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )

        start_time = time.time()
        model.fit(X_train, y_train)
        training_time = time.time() - start_time

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("training_time", training_time)

        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8,6))
        sns.heatmap(cm, cmap="Blues", annot=True)
        plt.title("Matrice de confusion")
        plt.ylabel("valeur réelle")
        plt.ylabel("valeur prédite")
        plt.tight_layout()
        plt.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")
        plt.close()

        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]

        plt.figure(figsize=(10,6))
        plt.title("feature importance")
        plt.bar(range(X.shape[1]), importances[indices])
        plt.ylabel("features")
        plt.ylabel("importance")
        plt.tight_layout()
        plt.savefig("features.png")
        mlflow.log_artifact("features.png")
        plt.close()

        mlflow.sklearn.log_model(model, "random_forest_model")

        run_id = mlflow.active_run().info.run_id

        result.append({
            "run_id": run_id,
            "run_name": run_name,
            "n_estimators": n_estimators,
            'max_depth': max_depth,
            'accuracy': accuracy,
            'f1_score': f1,
            'precision': precision,
            'recall': recall,
            'training_time': training_time
        })


client = MlflowClient()
experiment = client.get_experiment_by_name("exercice2")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1
)

print(f"meilleure run : {runs[0]}")
# /!\
# execute command mlflow ui
# before run the script
# /!\

import time

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42

x, y = make_classification(n_samples=2000, n_features=20, random_state=42)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
)

mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

print(f"Tracking uri : {mlflow.get_tracking_uri()}")

EXPERIMENT_NAME = "demo_client"

# GET EXPERIMENT
existing = client.get_experiment_by_name(name=EXPERIMENT_NAME)

if existing:
    # DELETE EXPERIMENT
    # client.delete_experiment() ne supprime pas physiquement l’expérience.
    # Elle passe simplement son lifecycle_stage à "deleted"

    # client.delete_experiment(experiment_id=existing.experiment_id)
    # print("Experiment deleted (lifecycle_stage == 'deleted')")
    pass

if existing:
    # Restaurer l’expérience au lieu de la recréer
    if existing.lifecycle_stage == "deleted":
        client.restore_experiment(existing.experiment_id)
        print("Experiment restored")

if not existing:
    # CREATE EXPERIMENT
    client.create_experiment(
        name=EXPERIMENT_NAME,
        tags={
            "team": "data-science",
            "project": "fraud-v1",
        },
    )
    print("Experiment created")

exp = client.get_experiment_by_name(name=EXPERIMENT_NAME)

print(f"tags: {exp.tags}")

# 2. Créer et logger des runs
param_grid = [
    {"model": "random_forest", "n_estimators": 50, "max_depth": 3},
    {"model": "random_forest", "n_estimators": 100, "max_depth": 5},
    {"model": "random_forest", "n_estimators": 200, "max_depth": 10},
    {"model": "logistic_reg", "C": 0.01, "max_iter": 200},
    {"model": "logistic_reg", "C": 0.1, "max_iter": 150},
    {"model": "logistic_reg", "C": 1.0, "max_iter": 100},
]

run_ids = []

for i, params in enumerate(param_grid):
    model_type = params["model"]
    run_name = f"{model_type}_{i + 1}"

    run = client.create_run(
        experiment_id=exp.experiment_id,
        run_name=run_name,
        tags={"model_type": model_type},
    )

    run_id = run.info.run_id

    try:
        for k, v in params.items():
            if k != "model":
                client.log_param(run_id, k, v)
        client.log_param(run_id, "model_type", model_type)

        if model_type == "random_forest":
            model = RandomForestClassifier(
                n_estimators=params["n_estimators"],
                max_depth=params["max_depth"],
                random_state=42,
            )
        else:
            model = LogisticRegression(
                C=params["C"], max_iter=params["max_iter"], random_state=42
            )

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        acc = accuracy_score(y_test, y_pred)

        client.log_metric(run_id, "accuracy", acc)

        mlflow.sklearn.log_model(model, run_id=run_id)

        client.set_terminated(run_id, status="FINISHED")

    except Exception as e:
        print(e)
        client.set_terminated(run_id, status="FAILED")


# 3. Recherche et filtrage de runs

# Tous les runs triés par accuracy décroissant
all_runs = client.search_runs(
    experiment_ids=[exp.experiment_id], order_by=["metrics.accuracy DESC"]
)

print("tous les runs :")
for r in all_runs:
    print(f"{r.info.run_name} - accuracy : {r.data.metrics.get('accuracy', 0)}")

# Filtrer uniquement les runs avec une accuracy > 0.8
filtered = client.search_runs(
    experiment_ids=[exp.experiment_id],
    filter_string="metrics.accuracy > 0.8",
    order_by=["metrics.accuracy DESC"],
)

print("tous les runs > 0.8 accuracy :")
for r in filtered:
    print(f"{r.info.run_name} - accuracy : {r.data.metrics.get('accuracy', 0)}")

# filtrer uniquement les runs par type de modèle
filtered_rf = client.search_runs(
    experiment_ids=[exp.experiment_id],
    filter_string="tags.model_type = 'random_forest'",
    order_by=["metrics.accuracy DESC"],
)

print("tous les runs random_forest :")
for r in filtered_rf:
    print(f"{r.info.run_name} - accuracy : {r.data.metrics.get('accuracy', 0)}")

# 4. Comparer les runs

runs_data = client.search_runs(
    experiment_ids=[exp.experiment_id], filter_string="attributes.status = 'FINISHED'"
)

df = pd.DataFrame(
    [
        {
            "run_name": r.info.run_name,
            "model_type": r.data.tags.get("model_type", ""),
            "accuracy": r.data.metrics.get("accuracy", None),
            "run_id": r.info.run_id,
        }
        for r in runs_data
    ]
)

df_sorted = df.sort_values("accuracy", ascending=False)
print(df_sorted)

# Selectionner et taguer le meilleur run

best_row = df_sorted.iloc[0]
best_run_id = best_row["run_id"]

print(f"Meilleur run : {best_row['run_name']}")
print(f"Meilleur run id : {best_run_id}")
print(f"Meilleur accuracy : {best_row['accuracy']}")

client.set_tag(best_run_id, "status", "best_run")
client.set_tag(best_run_id, "timestamp", time.strftime("%Y-%m-%d"))

updated_run = client.get_run(best_run_id)
print(updated_run.data.tags)

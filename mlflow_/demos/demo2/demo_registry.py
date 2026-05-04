import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

# Pour un serveur distant MlflowClient("https://my-mlflow.com")
mlflow.set_tracking_uri("http://localhost:5000")
client = MlflowClient()

X, y = load_wine(return_X_y=True)
_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

EXPERIMENT_NAME = "wine-classification"
MODEL_NAME = "wine_classifier"  # nom dans le registry

exp = client.get_experiment_by_name(EXPERIMENT_NAME)

all_runs = client.search_runs(
    experiment_ids=[exp.experiment_id],
    filter_string="attributes.status = 'FINISHED'",
    order_by=["metrics.accuracy DESC"],
)

print(all_runs)

rows = []

for r in all_runs:
    # Vérifie que le run a bien des artefact "model"
    artifacts = [
        a.path for a in client.list_artifacts(r.info.run_id, path="model-random-forest")
    ]
    has_model = "model-random-forest/model.pkl" in artifacts

    # Méthode 2 :
    # try:
    #     mlflow.sklearn.load_model(f"runs:/{r.info.run_id}/model-random-forest")
    #     has_model = True
    # except:
    #     has_model = False

    rows.append(
        {
            "run_name": r.info.run_name,
            "model_type": r.data.tags.get("model_type", "_"),
            "accuracy": r.data.metrics.get("accuracy"),
            "f1": r.data.metrics.get("f1_score"),
            "precision": r.data.metrics.get("precision"),
            "recall": r.data.metrics.get("recall"),
            "has_model": has_model,
            "run_id": r.info.run_id,
        }
    )

df = pd.DataFrame(rows)

df_with_model = df[df["has_model"] == True].copy()

top2 = df_with_model.head(2)
print("top 2 :")
print(top2)

registered_versions = []

for _, row in top2.iterrows():
    run_id = row["run_id"]
    model_uri = f"runs:/{run_id}/model-random-forest"

    # register_model() copie l'artefact du run dans le registry et lui attribue automatiquement une version ("1", "2"....)
    result = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)

    client.update_model_version(
        name=MODEL_NAME,
        version=result.version,
        description=(
            f"modèle : {row['model_type']} |"
            f"accuracy : {row['accuracy']} |"
            f"run_id : {run_id} |"
        ),
    )

    registered_versions.append(result.version)

print(f"version enregistré : {registered_versions}")

v1, v2 = registered_versions[0], registered_versions[1]

# Promouvoir V1 en staging
client.transition_model_version_stage(name=MODEL_NAME, version=v1, stage="Staging")

print(f"V{v1} =>  staging")

client.transition_model_version_stage(name=MODEL_NAME, version=v2, stage="Staging")

print(f"V{v2} =>  staging")

# archive_existing_versions=True => archive automatiquement les autres versions en production
client.transition_model_version_stage(
    name=MODEL_NAME, version=v1, stage="Production", archive_existing_versions=True
)

print(f"V{v1} =>  Production")

print("=" * 30)
print("Etat du registry : ")
versions = client.search_model_versions(f"name='{MODEL_NAME}'")
print(versions)

# Charger un modèle en production
model_prod = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/Production")

preds = model_prod.predict(X_test[:5])

print(preds)

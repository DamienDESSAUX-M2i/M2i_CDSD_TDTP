import mlflow
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

x, y = load_wine(return_X_y=True)

test_size = 0.2
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size, random_state=42
)


mlflow.sklearn.autolog()

mlflow.set_experiment("wine-classification")

with mlflow.start_run(run_name="random-forest-baseline"):
    mlflow.set_tag("model_type", "RandomForest")
    mlflow.set_tag("dataset", "wine")
    mlflow.set_tag("version", "1.0.0")

    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    model.score(y_test, y_pred)

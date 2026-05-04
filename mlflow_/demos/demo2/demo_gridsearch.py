import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split

x, y = load_iris(return_X_y=True)
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, None],
    "min_samples_split": [2, 5],
}

mlflow.set_experiment("demo-gridsearch")

with mlflow.start_run(run_name="GridSearch"):
    gs = GridSearchCV(
        estimator=RandomForestClassifier(random_state=42),
        param_grid=param_grid,
        cv=5,
        scoring="accuracy",
        n_jobs=-1,
    )

    gs.fit(x_train, y_train)

    mlflow.log_metric("best_accuracy", gs.best_score_)

    y_pred = gs.predict(x_test)
    mlflow.log_metric("test_accuracy", accuracy_score(y_test, y_pred))

    mlflow.sklearn.log_model(gs.best_estimator_, "best_model")

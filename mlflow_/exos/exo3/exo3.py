import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import numpy as np

RANDOM_STATE = 42

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
columns = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target",
]
df = pd.read_csv(url, names=columns, na_values="?")

# Binary target : 0 = healthy, 1 = sick
df["target"] = (df["target"] > 0).astype(int)

print(f"DataFrame shape: {df.shape}")
print(f"\nNumber of NaN per column:\n{df.isnull().sum()}")
print(f"\nTarget repartition:\n{df['target'].value_counts()}")

df_clean = df.dropna()

print(f"\nDataFrame cleaned shape: {df_clean.shape}")
print(f"\nNumber of rows removed: {len(df) - len(df_clean)}")

x = df_clean.drop(columns="target")
print(f"\nNumber of features: {len(x.columns)}")
y = df_clean["target"].copy()

mlflow.set_experiment("heart_disease_eda")

with mlflow.start_run(run_name="EDA"):
    # --- Figure 1 : Target distribution ---
    target_distribution = y.value_counts()
    plt.figure(figsize=(7, 5))
    plt.bar(["healthy", "sick"], target_distribution.values)
    plt.ylabel("Number of patient")
    plt.title("Target Distribution")
    mlflow.log_figure(plt.gcf(), "target_distribution.png")
    plt.close()

    # --- Figure 2 : Age distribution ---
    plt.figure(figsize=(7, 5))
    plt.hist(x["age"], bins=12, range=(0, 120))
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.title("Age histogram")
    mlflow.log_figure(plt.gcf(), "age_histogram.png")
    plt.close()

    # --- Figure 3 : Correlations heatmap ---
    correlation_matrix = df_clean.corr(method="pearson")
    plt.figure(figsize=(10, 10))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="Blues",
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        fmt=".2f",
    )
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.title("Correlation Matrix")
    mlflow.log_figure(plt.gcf(), "correlation_matrix.png")
    plt.close()


x_train, x_test, y_train, y_test = train_test_split(
    x, y, stratify=y, test_size=0.2, random_state=RANDOM_STATE
)

print(f"\nTrain set shape: {x_train.shape}")
print(f"Train set shape: {x_test.shape}")

print(f"\nTarget repartition: {y.sum() / len(y) * 100:.2f}%")
print(f"Train target repartition: {y_train.sum() / len(y_train) * 100:.2f}%")
print(f"Test target repartition: {y_test.sum() / len(y_test) * 100:.2f}%")

mlflow.set_experiment("heart_disease_svc")

pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        ("svm", SVC(probability=True, random_state=RANDOM_STATE)),
    ]
)

param_grid = {
    "svm__C": [0.01, 0.1, 1, 10, 100],
    "svm__kernel": ["linear", "rbf", "poly"],
    "svm__gamma": ["scale", "auto", 0.1, 0.01, 0.001],
}

gs = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=5,
    scoring="recall",
    n_jobs=-1,
)

gs.fit(x_train, y_train)

with mlflow.start_run(run_name="SVC_GridSearch"):
    # Log best hyperparameters ---
    best_params_clean = {k.replace("svm__", ""): v for k, v in gs.best_params_.items()}
    mlflow.log_params(best_params_clean)
    mlflow.log_metric("best_cv_score", gs.best_score_)

    # Evaluation on test set
    y_pred = gs.predict(x_test)
    y_proba = gs.predict_proba(x_test)[:, 1]
    mlflow.log_metric("test_accuracy", accuracy_score(y_test, y_pred))

    # AUC-ROC
    mlflow.log_metric("auc_roc", roc_auc_score(y_test, y_pred))

    # --- Figure 1 : Confusion matrix ---
    cm = confusion_matrix(y_test, y_pred)
    class_names = [
        "age",
        "sex",
        "cp",
        "trestbps",
        "chol",
        "fbs",
        "restecg",
        "thalach",
        "exang",
        "oldpeak",
        "slope",
        "ca",
        "thal",
    ]
    plt.figure(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        cmap="Blues",
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8},
        fmt="d",
    )
    plt.xlabel("Predict label")
    plt.xticks(np.arange(0.5, 2.5, 1), ["healthy", "sick"], rotation=45)
    plt.ylabel("True label")
    plt.yticks(np.arange(0.5, 2.5, 1), ["healthy", "sick"], rotation=45)
    plt.title("Confusion Matrix")
    mlflow.log_figure(plt.gcf(), "confusion_matrix.png")
    plt.close()

    # --- Figure 2 : ROC curve ---
    fpr, tpr, threshold = roc_curve(y_test, y_proba)
    youden_j = tpr - fpr
    optimal_idx = np.argmax(youden_j)
    optimal_threshold = threshold[optimal_idx]
    y_pred_optimal = (y_proba >= optimal_threshold).astype(int)
    auc_score = roc_auc_score(y_test, y_proba)

    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"AUC = {auc_score:.2f}")
    plt.plot(
        fpr[optimal_idx],
        tpr[optimal_idx],
        "ro",
        markersize=8,
        label=f"Optimal threshold = {optimal_threshold:.3f}",
    )

    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("ROC curve")
    plt.legend()
    mlflow.log_figure(plt.gcf(), "roc_curve.png")
    plt.close()

    # Log model
    mlflow.sklearn.log_model(
        gs.best_estimator_, "best_model", input_example=x_train.iloc[:5]
    )

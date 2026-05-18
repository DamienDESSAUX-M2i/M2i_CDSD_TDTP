import json
import os
import time
from datetime import datetime

import numpy as np
from sklearn.datasets import make_classification, make_regression, make_blobs
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score,
    silhouette_score,
    davies_bouldin_score,
)
from sklearn.model_selection import train_test_split

METRICS_FILE = os.getenv("METRICS_FILE", "/metrics/model_metrics.json")

history = []


def evaluate_balanced_classification():
    X, y = make_classification(
        n_samples=1200,
        n_features=12,
        n_informative=8,
        n_redundant=2,
        weights=[0.5, 0.5],
        flip_y=np.random.uniform(0.01, 0.08),
        random_state=None,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, stratify=y
    )

    model = RandomForestClassifier(n_estimators=80, max_depth=6)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "problem_type": "Classification équilibrée",
        "recommended_kpis": ["Accuracy"],
        "when_to_choose": "Classes équilibrées et erreurs symétriques",
        "metrics": {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1_score": round(f1_score(y_test, y_pred), 4),
            "auc_roc": round(roc_auc_score(y_test, y_proba), 4),
        },
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "interpretation": "L'accuracy est pertinente car les deux classes sont représentées de manière équilibrée."
    }


def evaluate_imbalanced_classification():
    X, y = make_classification(
        n_samples=1600,
        n_features=14,
        n_informative=8,
        n_redundant=3,
        weights=[0.93, 0.07],
        flip_y=np.random.uniform(0.01, 0.05),
        random_state=None,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, max_depth=7, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "problem_type": "Classification déséquilibrée",
        "recommended_kpis": ["F1-score", "Precision", "Recall", "AUC-ROC"],
        "when_to_choose": "Classes déséquilibrées : fraude, churn, défaut de paiement, panne rare",
        "metrics": {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, y_pred, zero_division=0), 4),
            "auc_roc": round(roc_auc_score(y_test, y_proba), 4),
        },
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "interpretation": "L'accuracy peut être trompeuse. Il faut regarder precision, recall, F1-score et AUC-ROC."
    }


def evaluate_regression():
    X, y = make_regression(
        n_samples=1200,
        n_features=10,
        n_informative=7,
        noise=np.random.uniform(8, 25),
        random_state=None,
    )

    y = y + 300

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30
    )

    model = RandomForestRegressor(n_estimators=100, max_depth=8)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = mean_squared_error(y_test, y_pred, squared=False)

    return {
        "problem_type": "Régression",
        "recommended_kpis": ["RMSE", "MAE", "MAPE", "R²"],
        "when_to_choose": "Prédiction de valeurs continues : prix, ventes, consommation, salaire",
        "metrics": {
            "rmse": round(rmse, 2),
            "mae": round(mean_absolute_error(y_test, y_pred), 2),
            "mape": round(mean_absolute_percentage_error(y_test, y_pred) * 100, 2),
            "r2": round(r2_score(y_test, y_pred), 4),
        },
        "sample_predictions": [
            {
                "real": round(float(real), 2),
                "predicted": round(float(pred), 2),
                "error": round(float(abs(real - pred)), 2)
            }
            for real, pred in list(zip(y_test[:20], y_pred[:20]))
        ],
        "interpretation": "RMSE pénalise fortement les grosses erreurs, MAE donne une erreur moyenne lisible, R² mesure la variance expliquée."
    }


def evaluate_clustering():
    X, _ = make_blobs(
        n_samples=900,
        centers=4,
        cluster_std=np.random.uniform(0.7, 1.8),
        n_features=2,
        random_state=None,
    )

    model = KMeans(n_clusters=4, n_init=10)
    labels = model.fit_predict(X)

    return {
        "problem_type": "Clustering",
        "recommended_kpis": ["Silhouette", "Davies-Bouldin"],
        "when_to_choose": "Évaluation non supervisée : segmentation client, groupes de comportements, typologies",
        "metrics": {
            "silhouette": round(silhouette_score(X, labels), 4),
            "davies_bouldin": round(davies_bouldin_score(X, labels), 4),
        },
        "cluster_points": [
            {
                "x": round(float(point[0]), 3),
                "y": round(float(point[1]), 3),
                "cluster": int(label)
            }
            for point, label in list(zip(X[:350], labels[:350]))
        ],
        "interpretation": "Silhouette proche de 1 indique des clusters bien séparés. Davies-Bouldin plus faible indique de meilleurs clusters."
    }


def build_payload():
    payload = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "balanced_classification": evaluate_balanced_classification(),
        "imbalanced_classification": evaluate_imbalanced_classification(),
        "regression": evaluate_regression(),
        "clustering": evaluate_clustering(),
    }

    history.append({
        "timestamp": payload["timestamp"],
        "balanced_accuracy": payload["balanced_classification"]["metrics"]["accuracy"],
        "imbalanced_f1": payload["imbalanced_classification"]["metrics"]["f1_score"],
        "regression_r2": payload["regression"]["metrics"]["r2"],
        "clustering_silhouette": payload["clustering"]["metrics"]["silhouette"],
    })

    if len(history) > 40:
        history.pop(0)

    payload["history"] = history

    return payload


def save_payload(payload):
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "w") as f:
        json.dump(payload, f, indent=4)


while True:
    metrics = build_payload()
    save_payload(metrics)
    print(json.dumps(metrics, indent=2))
    time.sleep(8)

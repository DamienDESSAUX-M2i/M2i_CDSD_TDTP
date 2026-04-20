import json
import os
import pickle
from datetime import datetime
from pathlib import Path

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


class Config:
    """Classe de configuration centralisée"""

    def __init__(self):
        # Environnement
        self.environment = os.getenv("ENVIRONMENT", "development")

        # Chemins
        self.data_path = os.getenv("DATA_PATH", "/app/data/dataset.csv")
        self.model_output = os.getenv("MODEL_OUTPUT", "/app/models/")

        # Modèle
        self.model_type = os.getenv("MODEL_TYPE", "logistic")
        self.n_estimators = int(os.getenv("N_ESTIMATORS", "100"))
        self.test_size = float(os.getenv("TEST_SIZE", "0.2"))
        self.random_state = int(os.getenv("RANDOM_STATE", "42"))

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.enable_monitoring = (
            os.getenv("ENABLE_MONITORING", "false").lower() == "true"
        )

        # Données
        self.n_samples = int(os.getenv("N_SAMPLES", "1000"))
        self.n_features = int(os.getenv("N_FEATURES", "20"))

    def validate(self):
        """Valider la configuration"""
        errors = []

        if self.model_type not in ["logistic", "random_forest"]:
            errors.append(f"Invalid MODEL_TYPE: {self.model_type}")

        if self.test_size <= 0 or self.test_size >= 1:
            errors.append(f"Invalid TEST_SIZE: {self.test_size}")

        if self.n_estimators <= 0:
            errors.append(f"Invalid N_ESTIMATORS: {self.n_estimators}")

        if errors:
            raise ValueError(
                "Configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
            )

    def display(self):
        """Afficher la configuration"""
        print(f"CONFIGURATION - {self.environment.upper()}")
        print(f"Environment:       {self.environment}")
        print(f"Model Type:        {self.model_type}")
        print(f"N Estimators:      {self.n_estimators}")
        print(f"Test Size:         {self.test_size}")
        print(f"Random State:      {self.random_state}")
        print(f"Data Path:         {self.data_path}")
        print(f"Model Output:      {self.model_output}")
        print(f"Log Level:         {self.log_level}")
        print(f"Monitoring:        {self.enable_monitoring}")


class Logger:
    def __init__(self, level="INFO"):
        self.level = level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def log(self, message, level="INFO"):
        if self.levels.get(level, 1) >= self.levels.get(self.level, 1):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")


def main():
    # Charger et valider la configuration
    config = Config()

    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error:\n{e}")
        return

    config.display()

    # Logger
    logger = Logger(config.log_level)

    # Charger ou générer les données
    logger.log("Chargement des données...", "INFO")

    if Path(config.data_path).exists():
        logger.log(f"Lecture depuis {config.data_path}", "DEBUG")
        df = pd.read_csv(config.data_path)
        X = df.drop("target", axis=1).values
        y = df["target"].values
    else:
        logger.log("Génération de données synthétiques", "DEBUG")
        X, y = make_classification(
            n_samples=config.n_samples,
            n_features=config.n_features,
            random_state=config.random_state,
        )

    logger.log(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features", "INFO")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, random_state=config.random_state
    )

    logger.log(f"Train: {len(X_train)}, Test: {len(X_test)}", "DEBUG")

    # Entraîner le modèle
    logger.log("Entraînement du modèle...", "INFO")

    if config.model_type == "logistic":
        model = LogisticRegression(random_state=config.random_state, max_iter=1000)
    else:  # random_forest
        model = RandomForestClassifier(
            n_estimators=config.n_estimators, random_state=config.random_state
        )

    model.fit(X_train, y_train)
    logger.log("Entraînement terminé", "DEBUG")

    # Évaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    logger.log(f"Accuracy: {accuracy:.2%}", "INFO")

    if config.log_level == "DEBUG":
        logger.log("\n" + classification_report(y_test, y_pred), "DEBUG")

    # Sauvegarder le modèle
    os.makedirs(config.model_output, exist_ok=True)
    model_filename = (
        f"model_{config.environment}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    )
    model_path = os.path.join(config.model_output, model_filename)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    logger.log(f"Modèle sauvegardé: {model_path}", "INFO")

    # Monitoring
    if config.enable_monitoring:
        logger.log("Génération des métriques de monitoring", "INFO")

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "environment": config.environment,
            "model_type": config.model_type,
            "accuracy": accuracy,
            "n_samples": X.shape[0],
            "n_features": X.shape[1],
            "model_path": model_path,
        }

        metrics_path = os.path.join(config.model_output, "metrics.json")
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)

        logger.log(f"Métriques sauvegardées: {metrics_path}", "DEBUG")

    print("\nProcessus terminé avec succès!\n")


if __name__ == "__main__":
    main()

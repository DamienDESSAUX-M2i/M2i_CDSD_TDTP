import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model(data_path, model_path, n_estimators=100):
    """
    Entraîner un modèle de prédiction de qualité du vin
    Appelé par l'endpoint POST /train depuis l'onglet Entraînement de Streamlit
    """

    # TODO: Charger les données CSV
    df = pd.read_csv(data_path)

    # TODO: Séparer features (X) et target (y)
    x = df.drop(columns="quality")
    y = df["quality"]

    # TODO: Split train/test (80/20, random_state=42)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    # TODO: Créer et entraîner le RandomForestClassifier
    model = RandomForestClassifier(
        n_estimators=n_estimators, random_state=42, n_jobs=-1
    )
    model.fit(x_train, y_train)

    # TODO: Calculer l'accuracy sur le test set
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    # TODO: Sauvegarder le modèle avec joblib.dump()
    joblib.dump(model, model_path)

    # Retourner les métriques pour Streamlit (onglet Entraînement)
    return {
        "accuracy": accuracy,  # TODO: accuracy calculée
        "n_samples": len(df),  # TODO: len(df)
        "n_features": len(x),  # TODO: nombre de features
        "model_path": model_path,
    }

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime

def train_model(data_path, model_output_dir, n_estimators=100):
    """Entraîner un modèle de classification"""

    print("Démarrage de l'entraînement...")

    # Charger les données
    df = pd.read_csv(data_path)
    print(f"Dataset chargé: {len(df)} échantillons")

    # Préparer les données
    X = df.drop('quality', axis=1)
    y = df['quality']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Entraîner
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=42,
        n_jobs=-1
    )

    print("Entraînement en cours...")
    model.fit(X_train, y_train)

    # Évaluer
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Accuracy: {accuracy:.2%}")

    # Sauvegarder
    os.makedirs(model_output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = os.path.join(model_output_dir, f"model_{timestamp}.pkl")

    joblib.dump(model, model_path)
    print(f"Modèle sauvegardé: {model_path}")

    return {
        'model_path': model_path,
        'accuracy': float(accuracy),
        'n_samples': len(df),
        'n_features': len(X.columns),
        'timestamp': timestamp
    }
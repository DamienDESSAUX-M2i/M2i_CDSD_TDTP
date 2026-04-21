import os
from contextlib import contextmanager

import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


@contextmanager
def get_db_connection():
    connexion = None
    try:
        connexion = psycopg2.connect(DATABASE_URL)
        yield connexion
        connexion.commit()
    except Exception:
        if connexion is not None:
            connexion.rollback()
        raise
    finally:
        if connexion is not None:
            connexion.close()


def init_database():
    """Créer les tables nécessaires pour Streamlit"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    fixed_acidity FLOAT NOT NULL,
                    volatile_acidity FLOAT NOT NULL,
                    citric_acid FLOAT NOT NULL,
                    residual_sugar FLOAT NOT NULL,
                    chlorides FLOAT NOT NULL,
                    free_sulfur_dioxide FLOAT NOT NULL,
                    total_sulfur_dioxide FLOAT NOT NULL,
                    density FLOAT NOT NULL,
                    ph FLOAT NOT NULL,
                    sulphates FLOAT NOT NULL,
                    alcohol FLOAT NOT NULL,
                    predicted_quality INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS training_runs (
                    id SERIAL PRIMARY KEY,
                    model_type VARCHAR(255) NOT NULL,
                    accuracy FLOAT NOT NULL,
                    n_samples INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            print("Database initialized")


def save_prediction(features, prediction):
    """Sauvegarder une prédiction - appelé par l'API lors d'une prédiction"""
    print(type(prediction))
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO predictions (
                    fixed_acidity,
                    volatile_acidity,
                    citric_acid,
                    residual_sugar,
                    chlorides,
                    free_sulfur_dioxide,
                    total_sulfur_dioxide,
                    density,
                    pH,
                    sulphates,
                    alcohol,
                    predicted_quality
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    features["fixed_acidity"],
                    features["volatile_acidity"],
                    features["citric_acid"],
                    features["residual_sugar"],
                    features["chlorides"],
                    features["free_sulfur_dioxide"],
                    features["total_sulfur_dioxide"],
                    features["density"],
                    features["pH"],
                    features["sulphates"],
                    features["alcohol"],
                    prediction,
                ),
            )
            return cursor.fetchone()


def save_training_run(model_type, accuracy, n_samples):
    """Sauvegarder un entraînement - appelé par l'API après training"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO training_runs (
                    model_type,
                    accuracy,
                    n_samples
                )
                VALUES (%s, %s, %s)
                RETURNING *;
                """,
                (
                    model_type,
                    accuracy,
                    n_samples,
                ),
            )
            return cursor.fetchone()


def get_recent_predictions(limit=10):
    """Récupérer les dernières prédictions - utilisé par l'onglet Historique de Streamlit"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT %s;",
                (limit,),
            )
            return cursor.fetchall()


def get_training_history():
    """Récupérer l'historique des entraînements - utilisé par l'onglet Métriques de Streamlit"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM training_runs ORDER BY timestamp DESC LIMIT 20;"
            )
            return cursor.fetchall()

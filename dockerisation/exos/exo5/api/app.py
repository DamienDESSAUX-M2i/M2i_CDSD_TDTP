import os
import random
from dataclasses import dataclass

import psycopg2
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor


@dataclass(frozen=True)
class PostgreSQLConfig:
    dbname: str = os.getenv("POSTGRES_DBNAME", "mydb")
    user: str = os.getenv("POSTGRES_USER", "username")
    password: str = os.getenv("POSTGRES_PASSWORD", "userpassword")
    host: str = os.getenv("POSTGRES_HOST", "postgres")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


postgresql_config = PostgreSQLConfig()

app = Flask(__name__)


def insert(feature: str, prediction: int, probability: float) -> dict:
    try:
        with psycopg2.connect(postgresql_config.connection_string) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "INSERT INTO predictions (feature, prediction, probability) VALUES (%s, %s, %s) RETURNING *;",
                    (feature, prediction, probability),
                )
                return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Insert error: {e}")


def select_all() -> list[dict]:
    try:
        with psycopg2.connect(postgresql_config.connection_string) as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM predictions;")
                return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Select error: {e}")


def get_prediction_probability(feature: str, threshold: float = 0.5):
    probability = random.uniform(0, 1)
    prediction = 1 if probability > threshold else 0
    return prediction, probability


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return jsonify({"success": False, "error": "JSON required"}), 400

        data = request.get_json()

        if not data.get("feature"):
            return jsonify({"success": False, "error": "Missing feature"}), 400

        feature = data["feature"]
        prediction, probability = get_prediction_probability(feature)

        row = insert(feature, prediction, probability)

        return jsonify({"success": True, "data": row}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/history", methods=["GET"])
def history():
    try:
        rows = select_all()
        return jsonify({"success": True, "data": rows}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

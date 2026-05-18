import json
import os
import re
import time
from datetime import datetime
from kafka import KafkaConsumer

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "raw-data")
METRICS_FILE = os.getenv("METRICS_FILE", "/metrics/metrics.json")

records = []
history = []

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def detect_errors(record):
    errors = []

    age = record.get("age")
    salary = record.get("salary")
    email = record.get("email")

    if not isinstance(age, int) or age < 18 or age > 100:
        errors.append("age invalide")

    if not isinstance(salary, int) or salary < 0 or salary > 200000:
        errors.append("salaire aberrant")

    if not isinstance(email, str) or not re.match(EMAIL_REGEX, email):
        errors.append("email invalide")

    for key, value in record.items():
        if value is None:
            errors.append(f"valeur nulle : {key}")

    return errors


def compute_metrics():
    total_rows = len(records)

    if total_rows == 0:
        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "total_rows": 0,
            "total_cells": 0,
            "non_null_cells": 0,
            "duplicate_rows": 0,
            "error_rows": 0,
            "completeness_rate": 0,
            "duplicate_rate": 0,
            "error_rate": 0,
            "valid_rows": 0,
            "error_types": {},
            "history": []
        }

    total_cells = 0
    non_null_cells = 0
    duplicate_rows = 0
    error_rows = 0
    error_types = {}
    local_seen = set()

    for record in records:
        total_cells += len(record)
        non_null_cells += sum(1 for value in record.values() if value is not None)

        record_hash = json.dumps(record, sort_keys=True)

        if record_hash in local_seen:
            duplicate_rows += 1
            error_types["doublon"] = error_types.get("doublon", 0) + 1
        else:
            local_seen.add(record_hash)

        errors = detect_errors(record)

        if errors:
            error_rows += 1

        for error in errors:
            error_types[error] = error_types.get(error, 0) + 1

    completeness_rate = (non_null_cells / total_cells) * 100
    duplicate_rate = (duplicate_rows / total_rows) * 100
    error_rate = (error_rows / total_rows) * 100
    valid_rows = total_rows - error_rows - duplicate_rows

    point = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "completeness_rate": round(completeness_rate, 2),
        "duplicate_rate": round(duplicate_rate, 2),
        "error_rate": round(error_rate, 2),
        "total_rows": total_rows
    }

    history.append(point)

    if len(history) > 50:
        history.pop(0)

    return {
        "timestamp": point["timestamp"],
        "total_rows": total_rows,
        "total_cells": total_cells,
        "non_null_cells": non_null_cells,
        "duplicate_rows": duplicate_rows,
        "error_rows": error_rows,
        "valid_rows": max(valid_rows, 0),
        "completeness_rate": round(completeness_rate, 2),
        "duplicate_rate": round(duplicate_rate, 2),
        "error_rate": round(error_rate, 2),
        "targets": {
            "completeness": 95,
            "duplicates": 1,
            "errors": 2
        },
        "status": {
            "completeness": "OK" if completeness_rate > 95 else "KO",
            "duplicates": "OK" if duplicate_rate < 1 else "KO",
            "errors": "OK" if error_rate < 2 else "KO"
        },
        "error_types": error_types,
        "history": history
    }


def save_metrics(metrics):
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=4)


def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC_NAME,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="data-quality-analyzer",
                value_deserializer=lambda v: json.loads(v.decode("utf-8"))
            )
            print("Analyzer connecté à Kafka/Redpanda")
            return consumer
        except Exception as e:
            print(f"Broker non prêt, nouvelle tentative... {e}")
            time.sleep(5)


consumer = create_consumer()

for message in consumer:
    record = message.value
    records.append(record)

    metrics = compute_metrics()
    save_metrics(metrics)

    print(json.dumps(metrics, indent=2))

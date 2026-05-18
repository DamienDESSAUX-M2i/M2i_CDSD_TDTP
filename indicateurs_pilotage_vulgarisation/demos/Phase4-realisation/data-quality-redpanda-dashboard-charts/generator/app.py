import json
import os
import random
import time
from faker import Faker
from kafka import KafkaProducer

fake = Faker("fr_FR")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "raw-data")


def create_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("Producer connecté à Kafka/Redpanda")
            return producer
        except Exception as e:
            print(f"Broker non prêt, nouvelle tentative... {e}")
            time.sleep(5)


def generate_record():
    record = {
        "customer_id": random.randint(1, 500),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "age": random.randint(18, 90),
        "salary": random.randint(18000, 120000),
        "country": random.choice(["France", "Belgique", "Suisse", "Maroc"]),
        "signup_date": fake.date_this_decade().isoformat()
    }

    if random.random() < 0.05:
        record[random.choice(list(record.keys()))] = None

    if random.random() < 0.03:
        record["age"] = random.choice([-5, 150, "unknown"])

    if random.random() < 0.02:
        record["email"] = "email_invalide"

    if random.random() < 0.01:
        record["salary"] = random.choice([-1000, 999999])

    return record


producer = create_producer()

while True:
    data = generate_record()
    producer.send(TOPIC_NAME, data)
    producer.flush()
    print(f"Donnée envoyée : {data}")
    time.sleep(1)

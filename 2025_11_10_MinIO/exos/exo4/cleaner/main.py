import os
import time
from minio import Minio

import clean_customers
import clean_orders
import clean_clicks


ENDPOINT = os.getenv("S3_ENDPOINT", "minio:9000")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "rootuser")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "rootpass123")
BUCKET_BRONZE = os.getenv("BRONZE_BUCKET", "bronze")
BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")


def main() -> None:
    client: Minio = Minio(
        endpoint=ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )

    # Create buckets
    if not client.bucket_exists(BUCKET_BRONZE):
        client.make_bucket(bucket_name=BUCKET_BRONZE)
    if not client.bucket_exists(BUCKET_SILVER):
        client.make_bucket(bucket_name=BUCKET_SILVER)

    while True:
        time.sleep(10)
        clean_customers.processing(client=client)
        clean_orders.processing(client=client)
        clean_clicks.processing(client=client)


if __name__ == "__main__":
    main()
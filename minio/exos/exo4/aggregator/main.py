import os
import time
from minio import Minio

import processing


ENDPOINT = os.getenv("S3_ENDPOINT", "minio:9000")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "rootuser")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "rootpass123")
BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")
BUCKET_GOLD = os.getenv("GOLD_BUCKET", "gold")


def main() -> None:
    client: Minio = Minio(
        endpoint=ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )

    # Create buckets
    if not client.bucket_exists(BUCKET_SILVER):
        client.make_bucket(bucket_name=BUCKET_SILVER)
    if not client.bucket_exists(BUCKET_GOLD):
        client.make_bucket(bucket_name=BUCKET_GOLD)

    while True:
        time.sleep(15)
        processing.processing(client=client)


if __name__ == "__main__":
    main()
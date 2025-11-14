import os
import time
from minio import Minio


def main() -> None:
    endpoint = os.getenv("S3_ENDPOINT", "minio:9000")
    access_key = os.getenv("MINIO_ROOT_USER", "rootuser")
    secret_key = os.getenv("MINIO_ROOT_PASSWORD", "rootpass123")
    secure = False

    client: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )

    # Create buckets
    if not client.bucket_exists('bronze'):
        client.make_bucket(bucket_name='bronze')
    if not client.bucket_exists('silver'):
        client.make_bucket(bucket_name='silver')

    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
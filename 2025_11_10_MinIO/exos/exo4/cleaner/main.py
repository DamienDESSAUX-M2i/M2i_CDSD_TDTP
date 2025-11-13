import time
from minio import Minio

import clean_customers

def main() -> None:
    while True:
        time.sleep(5)
        try:
            clean_customers.main()
        except Exception:
            pass


if __name__ == "__main__":
    endpoint = "minio:9000"
    access_key = "rootuser"
    secret_key = "rootpass123"
    secure = False
    client: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )
    if not client.bucket_exists('bronze'):
        client.make_bucket(bucket_name='bronze')
    if not client.bucket_exists('silver'):
        client.make_bucket(bucket_name='silver')
    main()
import json
from minio import Minio


def list_all_objects(client: Minio):
    print(f"Client {client.__repr__()}")
    for bucket in client.list_buckets():
        print(f"Bucket : {bucket.name}")
        for object in client.list_objects(bucket_name=bucket.name):
            print(f"Objet : {object.object_name}")


def main() -> None:
    endpoint = "localhost:9000"
    secure = False

    # access_key = "minioadmin"
    # secret_key = "minioadmin"
    # client: Minio = Minio(
    #     endpoint=endpoint,
    #     access_key=access_key,
    #     secret_key=secret_key,
    #     secure=secure
    # )

    access_key_admin = "minio-admin"
    secret_key_admin = "minioadmin"
    client_admin: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key_admin,
        secret_key=secret_key_admin,
        secure=secure
    )

    access_key_manager = "minio-manager"
    secret_key_manager = "miniomanager"
    client_manager: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key_manager,
        secret_key=secret_key_manager,
        secure=secure
    )

    access_key_client = "minio-client"
    secret_key_client = "minioclient"
    client_client: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key_client,
        secret_key=secret_key_client,
        secure=secure
    )

    bucket_admin = "admin-bucket"
    bucket_manager = "manager-bucket"
    bucket_client = "client-bucket"
    list_all_objects(client=client_admin)
    list_all_objects(client=client_manager)
    list_all_objects(client=client_client)

    object_name = "customers.csv"
    file_path = "./2025_11_10_MinIO/exos/exo3/file.csv"
    client_admin.fput_object(bucket_name=bucket_admin, object_name=object_name, file_path=file_path)
    client_admin.fput_object(bucket_name=bucket_manager, object_name=object_name, file_path=file_path)
    client_admin.fput_object(bucket_name=bucket_client, object_name=object_name, file_path=file_path)


if __name__ == "__main__":
    main()
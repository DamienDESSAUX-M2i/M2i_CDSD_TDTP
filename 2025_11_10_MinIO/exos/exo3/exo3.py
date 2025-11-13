from typing import Callable
from minio import Minio
from minio.error import S3Error


def list_all_objects(client: Minio):
    # print(f"Client {client.__repr__()}")
    for bucket in client.list_buckets():
        # print(f"Bucket : {bucket.name}")
        for object in client.list_objects(bucket_name=bucket.name):
            pass
            # print(f"Objet : {object.object_name}")


def test(description: str, callable: Callable, *args, **kwargs):
    print(description)
    try:
        callable(*args, **kwargs)
        print("Succes")
    except S3Error:
        print("Echec")


def main() -> None:
    endpoint = "localhost:9000"
    secure = False

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
    test(description="ListBucket Admin", callable=list_all_objects, client=client_admin)
    test(description="ListBucket Manager", callable=list_all_objects, client=client_manager)
    test(description="ListBucket client", callable=list_all_objects, client=client_client)

    object_name = "customers.csv"
    file_path = "./2025_11_10_MinIO/exos/exo3/file.csv"
    test(description="PutObject admin/admin", callable=client_admin.fput_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path)
    test(description="PutObject admin/manager", callable=client_admin.fput_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path)
    test(description="PutObject admin/client", callable=client_admin.fput_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path)

    test(description="PutObject manager/admin", callable=client_manager.fput_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path)
    test(description="PutObject manager/manager", callable=client_manager.fput_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path)
    test(description="PutObject manager/client", callable=client_manager.fput_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path)

    test(description="PutObject client/admin", callable=client_client.fput_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path)
    test(description="PutObject client/manager", callable=client_client.fput_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path)
    test(description="PutObject client/client", callable=client_client.fput_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path)

    file_path_get = "./2025_11_10_MinIO/exos/exo3/file_get.csv"
    test(description="GetObject admin/admin", callable=client_admin.fget_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path_get)
    test(description="GetObject admin/manager", callable=client_admin.fget_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path_get)
    test(description="GetObject admin/client", callable=client_admin.fget_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path_get)

    test(description="GetObject manager/admin", callable=client_manager.fget_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path_get)
    test(description="GetObject manager/manager", callable=client_manager.fget_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path_get)
    test(description="GetObject manager/client", callable=client_manager.fget_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path_get)

    test(description="GetObject client/admin", callable=client_client.fget_object, bucket_name=bucket_admin, object_name=object_name, file_path=file_path_get)
    test(description="GetObject client/manager", callable=client_client.fget_object, bucket_name=bucket_manager, object_name=object_name, file_path=file_path_get)
    test(description="GetObject client/client", callable=client_client.fget_object, bucket_name=bucket_client, object_name=object_name, file_path=file_path_get)

    test(description="DeleteObject admin/admin", callable=client_admin.remove_object, bucket_name=bucket_admin, object_name=object_name)
    test(description="DeleteObject admin/manager", callable=client_admin.remove_object, bucket_name=bucket_manager, object_name=object_name)
    test(description="DeleteObject admin/client", callable=client_admin.remove_object, bucket_name=bucket_client, object_name=object_name)

    test(description="DeleteObject manager/admin", callable=client_manager.remove_object, bucket_name=bucket_admin, object_name=object_name)
    test(description="DeleteObject manager/manager", callable=client_manager.remove_object, bucket_name=bucket_manager, object_name=object_name)
    test(description="DeleteObject manager/client", callable=client_manager.remove_object, bucket_name=bucket_client, object_name=object_name)

    test(description="DeleteObject client/admin", callable=client_client.remove_object, bucket_name=bucket_admin, object_name=object_name)
    test(description="DeleteObject client/manager", callable=client_client.remove_object, bucket_name=bucket_manager, object_name=object_name)
    test(description="DeleteObject client/client", callable=client_client.remove_object, bucket_name=bucket_client, object_name=object_name)


if __name__ == "__main__":
    main()
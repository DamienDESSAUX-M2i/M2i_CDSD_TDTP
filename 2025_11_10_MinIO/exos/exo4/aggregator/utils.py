from minio import Minio


def object_name_to_datetime():
    raise NotImplementedError


def get_object_names(client: Minio, bucket_name: str , prefix: str) -> list[str]:
    object_names: list[str] = []
    # file_path = Path(FOLDER_DATA + PREFIX + "last_csv_processed.txt")
    # with open(file_path, "rt", encoding="utf-8", newline="") as f:
    #     last_csv_processed = f.read()
    #     datetime_last_csv_processed = object_name_to_datetime(last_csv_processed)
    minio_objects = client.list_objects(bucket_name=bucket_name, prefix=prefix)
    for minio_object in minio_objects:
        # if object_name_to_datetime(minio_object.object_name) > datetime_last_csv_processed:
        object_names.append(minio_object.object_name)
    return object_names

import json
import datetime
from minio import Minio


def load_json(file_path) -> list[dict]:
    with open(file_path, 'r', encoding="utf-8") as jsonfile:
        return json.loads(jsonfile.read())


def write_json(file_path, orders: list[dict]) -> None:
    with open(file_path, 'w', encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(orders))


def clean_json(orders: list[dict]) -> list[dict]:
    orders_cleaned: list[dict] = []
    for order in orders:
        try:
            if int(order["quantity"]) < 0:
                raise ValueError
        except Exception:
            continue
        try:
            datetime.datetime.strptime(order["order_ts"], "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            continue
        orders_cleaned.append(order)
    return orders_cleaned


def main() -> None:
    # endpoint = "minio:9000"
    # access_key = "rootuser"
    # secret_key = "rootpass123"
    # secure = False
    # client: Minio = Minio(
    #     endpoint=endpoint,
    #     access_key=access_key,
    #     secret_key=secret_key,
    #     secure=secure
    # )

    # bucket_bonze = "bronze"

    # bucket_silver = "silver"

    file_path_get = "./2025_11_10_MinIO/exos/exo4/data_test/orders_20251113T133710.json"
    orders = load_json(file_path=file_path_get)
    orders_cleaned = clean_json(orders=orders)
    file_path_put = "./2025_11_10_MinIO/exos/exo4/data_test/orders_cleaned_20251113T133710.json"
    write_json(file_path=file_path_put, orders=orders_cleaned)


if __name__ == "__main__":
    main()
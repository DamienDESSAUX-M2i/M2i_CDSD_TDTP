from datetime import datetime
from minio import Minio


TS_LAST_CUSTOMER_CLEANED = datetime.strptime("20250101T000000", "%Y%m%dT%H%M%S")
TS_LAST_ORDER_CLEANED = datetime.strptime("20250101T000000", "%Y%m%dT%H%M%S")
TS_LAST_CLICK_CLEANED = datetime.strptime("20250101T000000", "%Y%m%dT%H%M%S")


def sort_object_names_non_processed(object_names: list[str]) -> list[str]:
    global TS_LAST_CUSTOMER_CLEANED
    global TS_LAST_ORDER_CLEANED
    global TS_LAST_CLICK_CLEANED

    object_names_non_processed: list[str] = []
    list_ts_customer: list[datetime] = []
    list_ts_order: list[datetime] = []
    list_ts_click: list[datetime] = []

    for object_name in object_names:
        if "customer" in object_name:
            ts = datetime.strptime(object_name[object_name.rfind("_")+1:].replace(".csv", ""), "%Y%m%dT%H%M%S")
            if ts > TS_LAST_CUSTOMER_CLEANED:
                object_names_non_processed.append(object_name)
                list_ts_customer.append(ts)

        if "order" in object_name:
            ts = datetime.strptime(object_name[object_name.rfind("_")+1:].replace(".csv", ""), "%Y%m%dT%H%M%S")
            if ts > TS_LAST_ORDER_CLEANED:
                object_names_non_processed.append(object_name)
                list_ts_order.append(ts)

        if "click" in object_name:
            ts = datetime.strptime(object_name[object_name.rfind("_")+1:].replace(".csv", ""), "%Y%m%dT%H%M%S")
            if ts > TS_LAST_CLICK_CLEANED:
                object_names_non_processed.append(object_name)
                list_ts_click.append(ts)

    TS_LAST_CUSTOMER_CLEANED = max(list_ts_customer) if list_ts_customer else TS_LAST_CUSTOMER_CLEANED
    TS_LAST_ORDER_CLEANED = max(list_ts_order) if list_ts_order else TS_LAST_ORDER_CLEANED
    TS_LAST_CLICK_CLEANED = max(list_ts_click) if list_ts_click else TS_LAST_CLICK_CLEANED

    return object_names_non_processed


def get_object_names(client: Minio, bucket_name: str , prefix: str) -> list[str]:
    minio_objects = client.list_objects(bucket_name=bucket_name, prefix=prefix)
    object_names = [minio_object.object_name for minio_object in minio_objects]
    object_names_non_processed = sort_object_names_non_processed(object_names=object_names)
    return object_names_non_processed

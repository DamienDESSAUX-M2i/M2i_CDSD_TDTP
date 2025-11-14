import os
from pathlib import Path
import json
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict
from minio import Minio

import utils


BUCKET_BRONZE = os.getenv("BRONZE_BUCKET", "bronze")
BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")
PREFIX = "orders/"
FOLDER_DATA = "/app/data/"


class DictOrder(TypedDict):
    order_id: str
    customer_id: str
    product_id: str
    quantity: str
    unit_price: str
    total_amount: str
    order_ts: str
    channel: str


@dataclass
class Order:
    order_id: str
    customer_id: str
    product_id: str
    quantity: str
    unit_price: str
    total_amount: str
    order_ts: str
    channel: str
    concatenation: str # It is used to detect doubloons


def load_json(file_path) -> list[Order]:
    orders: list[Order] = []
    with open(file_path, 'rt', encoding="utf-8") as jsonfile:
        dict_orders: list[DictOrder] = json.loads(jsonfile.read())
        for dict_order in dict_orders:
            orders.append(Order(
                order_id=str(dict_order["order_id"]),
                customer_id=str(dict_order["customer_id"]),
                product_id=str(dict_order["product_id"]),
                quantity=str(dict_order["quantity"]),
                unit_price=str(dict_order["unit_price"]),
                total_amount=str(dict_order["total_amount"]),
                order_ts=str(dict_order["order_ts"]),
                channel=str(dict_order["channel"]),
                concatenation="".join([str(value) for value in dict_order.values()])
            ))
    return orders


def write_csv(file_path, orders: list[Order]) -> None:
    with open(file_path, 'wt', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["order_id", "customer_id", "product_id", "quantity", "unit_price", "total_amount", "order_ts", "channel"]
        writer: csv.DictWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for order in orders:
            writer.writerow(
                {
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "product_id": order.product_id,
                "quantity": order.quantity,
                "unit_price": order.unit_price,
                "total_amount": order.total_amount,
                "order_ts": order.order_ts,
                "channel": order.channel
                }
            )


def clean_json(orders: list[Order]) -> list[Order]:
    orders_cleaned: list[Order] = []
    concatenations: list[str] = [] # It is used to detect doubloons
    for order in orders:
        # Replace negative quantity
        try:
            if int(order.quantity) < 0:
                order.quantity = "0"
                order.total_amount = "0"
        except Exception:
            continue
        # Replace negative unit price
        try:
            if float(order.unit_price) < 0:
                order.unit_price = "0"
                order.total_amount = "0"
        except Exception:
            continue
        # Compute total amount if it is empty or negative
        try:
            if (order.total_amount.isspace()) or (order.total_amount == "") or (float(order.total_amount) < 0):
                order.total_amount = str(int(order.quantity) * int(order.total_amount))
        except Exception:
            continue
        # Remove empty date
        if (order.order_ts.isspace()) or (order.order_ts == ""):
            continue
        # Remove empty oder id
        if (order.order_id.isspace()) or (order.order_id == ""):
            continue
        # Remove empty customer id
        if (order.customer_id.isspace()) or (order.customer_id == ""):
            continue
        # Remove empty product id
        if (order.product_id.isspace()) or (order.product_id == ""):
            continue
        # Remove wrong date
        try:
            datetime.strptime(order.order_ts, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            continue
        # Remove doubloons
        if order.concatenation in concatenations:
            continue
        orders_cleaned.append(order)
        concatenations.append(order.concatenation)
    return orders_cleaned


def processing(client: Minio) -> None:
    for json_file_name in utils.get_object_names(client=client, bucket_name=BUCKET_BRONZE, prefix=PREFIX):
        # Local path
        file_path = Path(FOLDER_DATA + json_file_name)
        # Get json_file
        client.fget_object(bucket_name=BUCKET_BRONZE, object_name=json_file_name, file_path=file_path)
        # Processing
        orders = load_json(file_path=file_path)
        orders_cleaned = clean_json(orders=orders)
        write_csv(file_path=file_path, orders=orders_cleaned)
        # Put json_file
        index_underscore = json_file_name.index("_")
        json_file_cleaned_name = json_file_name[:index_underscore] + "_cleaned" + json_file_name[index_underscore:]
        csv_file_cleaned_name = json_file_cleaned_name.replace(".json", ".csv")
        client.fput_object(bucket_name=BUCKET_SILVER, object_name=csv_file_cleaned_name, file_path=file_path)
        # Clean local directory
        os.remove(file_path)
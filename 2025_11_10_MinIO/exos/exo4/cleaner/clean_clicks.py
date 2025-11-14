import os
from pathlib import Path
import json
from dataclasses import dataclass
from datetime import datetime
import re
from typing import TypedDict
from minio import Minio

import utils


BUCKET_BRONZE = os.getenv("BRONZE_BUCKET", "bronze")
BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")
PREFIX = "clicks/"
FOLDER_DATA = "/app/data/"


class DictClick(TypedDict):
    customer_id: str
    path: str
    ip: str
    ts: str


@dataclass
class Click:
    customer_id: str
    path: str
    ip: str
    ts: str


def load_txt(file_path) -> list[Click]:
    clicks: list[Click] = []
    with open(file_path, 'rt', encoding="utf-8") as txtfile:
        for line in txtfile.readlines():
            dict_click: DictClick = json.loads(line)
            clicks.append(Click(
                customer_id=str(dict_click["customer_id"]),
                path=str(dict_click["path"]),
                ip=str(dict_click["ip"]),
                ts=str(dict_click["ts"])
            ))
    return clicks


def write_txt(file_path, clicks: list[Click]) -> None:
    with open(file_path, 'wt', encoding="utf-8") as txtfile:
        for click in clicks:
            dict_click: DictClick = {
                "customer_id": click.customer_id,
                "path": click.path,
                "ts": click.ts
            }
            txtfile.writelines(json.dumps(dict_click))


def clean_txt(clicks: list[Click]) -> list[Click]:
    clicks_cleaned: list[Click] = []
    for click in clicks:
        regex_ipv4 = "^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        # Remove invalid ipv4
        if not re.search(regex_ipv4, click.ip):
            continue
        # Remove wrong date
        try:
            datetime.strptime(click.ts, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            continue
        clicks_cleaned.append(click)
    return clicks_cleaned


def processing(client: Minio) -> None:
    for txt_file_name in utils.get_object_names(client=client, bucket_name=BUCKET_BRONZE, prefix=PREFIX):
        # Local path
        file_path = Path(FOLDER_DATA + txt_file_name)
        # Get txt_file
        client.fget_object(bucket_name=BUCKET_BRONZE, object_name=txt_file_name, file_path=file_path)
        # Processing
        clicks = load_txt(file_path=file_path)
        clicks_cleaned = clean_txt(clicks=clicks)
        write_txt(file_path=file_path, clicks=clicks_cleaned)
        # Put txt_file
        index_underscore = txt_file_name.index("_")
        txt_file_cleaned_name = txt_file_name[:index_underscore] + "_cleaned" + txt_file_name[index_underscore:]
        client.fput_object(bucket_name=BUCKET_SILVER, object_name=txt_file_cleaned_name, file_path=file_path)
        # Clean local directory
        os.remove(file_path)
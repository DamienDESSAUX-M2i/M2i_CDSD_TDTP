import os
from pathlib import Path
import csv
from dataclasses import dataclass
import datetime
import hashlib
from typing import TypedDict
from minio import Minio

import utils


BUCKET_BRONZE = os.getenv("BRONZE_BUCKET", "bronze")
BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")
PREFIX = "customers/"
FOLDER_DATA = "/app/data/"


class DictCustomer(TypedDict):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    country: str
    signup_date: str


@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    initials: str
    email: str
    country: str
    signup_date: str


def load_csv(file_path) -> list[Customer]:
    customers: list[Customer] = []
    with open(file_path, 'rt', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["customer_id", "first_name", "last_name", "email", "country", "signup_date"]
        reader: csv.DictReader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row["customer_id"] == "customer_id":
                continue
            customer: Customer = Customer(
                customer_id=row["customer_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                initials="".join([row["first_name"][0] if row["first_name"] else "", row["last_name"][0] if row["last_name"] else ""]),
                email=row["email"],
                country=row["country"],
                signup_date=row["signup_date"],
                )
            customers.append(customer)
    return customers


def write_csv(file_path, customers: list[Customer]) -> None:
    with open(file_path, 'wt', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["customer_id", "initials", "country", "signup_date"]
        writer: csv.DictWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for customer in customers:
            writer.writerow(
                {
                "customer_id": str(customer.customer_id),
                "initials": customer.initials,
                "country": customer.country,
                "signup_date": customer.signup_date
                }
            )


def clean_csv(customers: list[Customer]) -> list[Customer]:
    customers_cleaned: list[Customer] = []
    for customer in customers:
        # Remove wrong date
        try:
            datetime.date.strptime(customer.signup_date, "%Y-%m-%d")
        except ValueError:
            continue
        # Replace empty country with 'NA'
        if (customer.country.isspace()) or (customer.country == ""):
            customer.country = "NA"
        # Remove blank email
        if (customer.customer_id.isspace()) or (customer.customer_id == ""):
            continue
        # Replace email address with its truncated SHA-256 hash.
        customer.email = hashlib.sha256(customer.email.encode("utf-8")).hexdigest() if customer.email else ""
        customers_cleaned.append(customer)
    return customers_cleaned


def processing(client: Minio) -> None:
    for csv_file_name in utils.get_object_names(client=client, bucket_name=BUCKET_BRONZE, prefix=PREFIX):
        # Local path
        file_path = Path(FOLDER_DATA + csv_file_name)
        # Get csv_file
        client.fget_object(bucket_name=BUCKET_BRONZE, object_name=csv_file_name, file_path=file_path)
        # Processing
        customers = load_csv(file_path=file_path)
        customers_cleaned = clean_csv(customers=customers)
        write_csv(file_path=file_path, customers=customers_cleaned)
        # Put csv_file
        index_underscore = csv_file_name.index("_")
        csv_file_cleaned_name = csv_file_name[:index_underscore] + "_cleaned" + csv_file_name[index_underscore:]
        client.fput_object(bucket_name=BUCKET_SILVER, object_name=csv_file_cleaned_name, file_path=file_path)
        # Clean local directory
        os.remove(file_path)
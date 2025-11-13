import os
import csv
from dataclasses import dataclass
import datetime
from minio import Minio


@dataclass
class Customer:
    customer_id: str
    first_name: str
    last_name: str
    email: str
    country: str
    signup_date: str


def load_csv(file_path) -> list[Customer]:
    customers: list[Customer] = []
    with open(file_path, 'rt', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["customer_id", "first_name", "last_name", "email", "country", "signup_date"]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row["customer_id"] == "customer_id":
                continue
            customer: Customer = Customer(
                customer_id=int(row["customer_id"]),
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                country=row["country"],
                signup_date=row["signup_date"],
                )
            customers.append(customer)
    return customers


def write_csv(file_path, customers: list[Customer]) -> None:
    with open(file_path, 'wt', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["customer_id", "first_name", "last_name", "email", "country", "signup_date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for customer in customers:
            writer.writerow(
                {
                "customer_id": str(customer.customer_id),
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "country": customer.country,
                "signup_date": customer.signup_date
                }
            )


def clean_csv(customers: list[Customer]) -> list[Customer]:
    customers_cleaned: list[Customer] = []
    for customer in customers:
        # Remove blank email
        if (customer.email.isspace()) or (customer.email == ""):
            continue
        # Remove wrong date
        try:
            datetime.date.strptime(customer.signup_date, "%Y-%m-%d")
        except ValueError:
            continue
        customers_cleaned.append(customer)
    return customers_cleaned


def processing(client: Minio) -> None:
    bucket_bonze = os.getenv("BRONZE_BUCKET", "bronze")
    bucket_silver = os.getenv("SILVER_BUCKET", "silver")
    prefix = "customers/"
    for csv_file in client.list_objects(bucket_name=bucket_bonze, prefix=prefix):
        # Local path
        file_path = f"/app/data/{csv_file.object_name}"
        # Get csv_file
        client.fget_object(bucket_name=bucket_bonze, object_name=csv_file.object_name, file_path=file_path)
        # Processing
        customers = load_csv(file_path=file_path)
        customers_cleaned = clean_csv(customers=customers)
        write_csv(file_path=file_path, customers=customers_cleaned)
        # Put csv_file
        client.fput_object(bucket_name=bucket_silver, object_name=csv_file.object_name, file_path=file_path)
        # Clean local directory
        os.remove(file_path)
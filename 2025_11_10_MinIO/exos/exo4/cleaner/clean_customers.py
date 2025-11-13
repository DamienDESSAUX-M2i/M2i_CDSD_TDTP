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
        if customer.email.isspace():
            continue
        try:
            datetime.date.strptime(customer.signup_date, "%Y-%m-%d")
        except ValueError:
            continue
        if (customer.email.isspace()) or (customer.email == ""):
            continue
        customers_cleaned.append(customer)
    return customers_cleaned


def main() -> None:
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

    bucket_bonze = "bronze"
    prefix = "customers/"
    csv_files_raw = client.list_objects(bucket_name=bucket_bonze, prefix=prefix)
    with open("log.txt", "wt", encoding="utf-8") as f:
        for csv_file_raw in csv_files_raw:
            f.write(csv_file_raw.object_name)

    # for csv_file_raw in csv_files_raw:
    #     file_path_get = f"/app/raw/{csv_file_raw.object_name}"
    #     client.fget_object(bucket_name=bucket_bonze, object_name=csv_file_raw.object_name, file_path=file_path_get)
    #     customers = load_csv(file_path=file_path_get)
    #     customers_cleaned = clean_csv(customers=customers)
    #     file_path_put = f"/app/cleaned/{csv_file_raw.object_name}"
    #     # write_csv(file_path=file_path_put, customers=customers_cleaned)

    # bucket_silver = "silver"
    # csv_files_cleaned = os.listdir("/app/cleaned/")
    # for csv_file_cleaned in csv_files_cleaned:
    #     client.fput_object(bucket_name=bucket_silver, object_name=f"customers/{csv_file_cleaned}", file_path=f"./app/cleaned/{csv_file_cleaned}")


if __name__ == "__main__":
    main()
import csv
from dataclasses import dataclass
import datetime
from minio import Minio


@dataclass
class Customer:
    index: int
    customer_id: str
    first_name: str
    last_name: str
    company: str
    city: str
    country: str
    phone1: str
    phone2: str
    email: str
    subscription_data: datetime.date
    website: str

    def values(self) -> list[str]:
        return [
            str(self.index),
            self.customer_id,
            self.first_name,
            self.last_name,
            self.company,
            self.city,
            self.country,
            self.phone1,
            self.phone2,
            self.email,
            self.subscription_data.strftime('%Y-%m-%d'),
            self.website
            ]


def load_csv(file_path) -> dict[int, Customer]:
    customers: dict[int, Customer] = {}
    with open(file_path, 'r', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Index", "Customer Id", "First Name", "Last Name", "Company", "City", "Country", "Phone 1", "Phone 2", "Email", "Subscription Date", "Website"]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            if row["Index"] == "Index":
                continue
            customer: Customer = Customer(
                index=int(row["Index"]),
                customer_id=row["Customer Id"],
                first_name=row["First Name"],
                last_name=row["Last Name"],
                company=row["Company"],
                city=row["City"],
                country=row["Country"],
                phone1=row["Phone 1"],
                phone2=row["Phone 2"],
                email=row["Email"],
                subscription_data=datetime.date.strptime(row["Subscription Date"], "%Y-%m-%d"),
                website=row["Website"]
                )
            customers.update({customer.index: customer})
    return customers


def write_csv(file_path, customers: dict[int, Customer]) -> None:
    with open(file_path, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["Index", "Customer Id", "First Name", "Last Name", "Company", "City", "Country", "Phone 1", "Phone 2", "Email", "Subscription Date", "Website"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for customer in customers.values():
            writer.writerow({
                "Index": customer.index,
                "Customer Id": customer.customer_id,
                "First Name": customer.first_name,
                "Last Name": customer.last_name,
                "Company": customer.company,
                "City": customer.city,
                "Country": customer.country,
                "Phone 1": customer.phone1,
                "Phone 2": customer.phone2,
                "Email": customer.email,
                "Subscription Date": customer.subscription_data,
                "Website": customer.website
            })


def write_txt(file_path, customers: dict[int, Customer]) -> None:
    with open(file_path, 'w', encoding="utf-8") as txtfile:
        fieldnames = ["Index", "Customer Id", "First Name", "Last Name", "Company", "City", "Country", "Phone 1", "Phone 2", "Email", "Subscription Date", "Website"]
        txtfile.write(",".join(fieldnames) + "\n")
        for customer in customers.values():
            txtfile.write(",".join(customer.values())  + "\n")


def filter_csv(customers: dict[int, Customer]) -> tuple[dict[int, Customer]]:
    customers_am: dict[int, Customer] = {}
    customers_nz: dict[int, Customer] = {}
    for index, customer in customers.items():
        if customer.country[0].lower() in "abcdefghijklm":
            customers_am.update({index: customer})
        if customer.country[0].lower() in "nopqrstuvwxyz":
            customers_nz.update({index: customer})
    return customers_am, customers_nz


def make_bucket(client: Minio, bucket_name: str) -> None:
    if client.bucket_exists(bucket_name=bucket_name):
        print(f"{bucket_name} already exists.")
    else:
        client.make_bucket(bucket_name=bucket_name)
        print(f"{bucket_name} is created.")


def main() -> None:
    endpoint = "localhost:9000"
    access_key = "minioadmin"
    secret_key = "minioadmin"
    secure = False
    client: Minio = Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )

    bucket_name_am="customers-am-bucket"
    bucket_name_nz="customers-nz-bucket"
    make_bucket(client=client, bucket_name=bucket_name_am)
    make_bucket(client=client, bucket_name=bucket_name_nz)

    file_path = "./2025_11_10_MinIO/exos/customers.csv"
    customers = load_csv(file_path=file_path)
    customers_am, customers_nz = filter_csv(customers=customers)
    file_path_am = "./2025_11_10_MinIO/exos/customers_am.txt"
    file_path_nz = "./2025_11_10_MinIO/exos/customers_nz.csv"
    write_txt(file_path=file_path_am, customers=customers_am)
    write_csv(file_path=file_path_nz, customers=customers_nz)

    object_name_am = "customers_am.txt"
    object_name_nz = "customers_nz.csv"
    client.fput_object(bucket_name=bucket_name_am, object_name=object_name_am, file_path=file_path_am)
    client.fput_object(bucket_name=bucket_name_nz, object_name=object_name_nz, file_path=file_path_nz)


if __name__ == "__main__":
    main()
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from minio import Minio

import utils


BUCKET_SILVER = os.getenv("SILVER_BUCKET", "silver")
BUCKET_GOLD = os.getenv("GOLD_BUCKET", "gold")
PREFIX = "orders/"
FOLDER_DATA = "/app/data/"


def sales_by_day(dataframe: pd.DataFrame, file_path: Path) -> None:
    dataframe["order_date"] = [datetime.strptime(order_ts, "%Y-%m-%d %H:%M:%S.%f").date() for order_ts in dataframe["order_ts"]]
    dataframe_agg = dataframe.groupby('order_date').agg({'total_amount':'mean'}).rename(columns={'total_amount':'mean_total_amount'}).reset_index()
    dataframe_agg.to_csv(file_path, sep=',', encoding='utf-8', index=False, header=True)


def top_products(dataframe: pd.DataFrame, file_path: Path) -> None:
    dataframe_agg = dataframe.groupby('product_id').agg({'total_amount':'sum'}).rename(columns={'total_amount':'sum_total_amount'}).reset_index()
    dataframe_filter = dataframe_agg.sort_values('sum_total_amount', ascending=False).head(10)
    dataframe_filter.to_csv(file_path, sep=',', encoding='utf-8', index=False, header=True)


def aov(dataframe: pd.DataFrame, file_path: Path) -> None:
    dataframe_agg = dataframe.groupby('customer_id').agg({'total_amount':'mean'}).rename(columns={'total_amount':'mean_total_amount'}).reset_index()
    dataframe_agg.to_csv(file_path, sep=',', encoding='utf-8', index=False, header=True)


def revenue_by_country(dataframe_order: pd.DataFrame, dataframe_customer: pd.DataFrame, file_path: Path) -> None:
    dataframe_merge = pd.merge(dataframe_order ,dataframe_customer, left_on='customer_id', right_on='customer_id', how='left')
    dataframe_agg = dataframe_merge.groupby('country').agg({'total_amount':'sum'}).rename(columns={'total_amount':'sum_total_amount'}).reset_index()
    dataframe_agg.to_csv(file_path, sep=',', encoding='utf-8', index=False, header=True)


def processing(client: Minio) -> None:
    for csv_file_name in utils.get_object_names(client=client, bucket_name=BUCKET_SILVER, prefix=PREFIX):
        # Local path
        file_path = Path(FOLDER_DATA + csv_file_name)

        # Get csv_file
        client.fget_object(bucket_name=BUCKET_SILVER, object_name=csv_file_name, file_path=file_path)

        # Processing
        dataframe = pd.read_csv(file_path)
        ## sales by day
        if not Path.exists(FOLDER_DATA + "sales_by_day"):
            os.mkdir(FOLDER_DATA + "sales_by_day")
        index_underscore = csv_file_name.rfind("_")
        csv_file_sales_by_day_name = "sales_by_day/sales_by_day" + csv_file_name[index_underscore:]
        file_path_sales_by_day = Path(FOLDER_DATA + csv_file_sales_by_day_name)
        sales_by_day(dataframe=dataframe, file_path=file_path_sales_by_day)
        ## top products
        if not Path.exists(FOLDER_DATA + "top_products"):
            os.mkdir(FOLDER_DATA + "top_products")
        csv_file_top_product_name = "top_products/top_products" + csv_file_name[index_underscore:]
        file_path_top_product = Path(FOLDER_DATA + csv_file_top_product_name)
        top_products(dataframe=dataframe, file_path=file_path_top_product)
        ## average order value
        if not Path.exists(FOLDER_DATA + "aov"):
            os.mkdir(FOLDER_DATA + "aov")
        csv_file_aov_name = "aov/aov" + csv_file_name[index_underscore:]
        file_path_aov = Path(FOLDER_DATA + csv_file_aov_name)
        aov(dataframe=dataframe, file_path=file_path_aov)
        ## revenue by channel
        if not Path.exists(FOLDER_DATA + "revenue_by_channel"):
            os.mkdir(FOLDER_DATA + "revenue_by_channel")
        csv_file_revenue_by_channel_name = "revenue_by_channel/revenue_by_channel" + csv_file_name[index_underscore:]
        file_path_revenue_by_channel = Path(FOLDER_DATA + csv_file_revenue_by_channel_name)
        aov(dataframe=dataframe, file_path=file_path_revenue_by_channel)
        # ## revenue by country
        # csv_file_customer_name = "customers/customers_cleaned" + csv_file_name[index_underscore:]
        # file_path_customer = Path(FOLDER_DATA + csv_file_customer_name)
        # ### GET customer
        # client.fget_object(bucket_name=BUCKET_SILVER, object_name=csv_file_customer_name, file_path=file_path_customer)
        # dataframe_customer = pd.read_csv(file_path_customer)
        # ### Processing
        # if not Path.exists(FOLDER_DATA + "revenue_by_country"):
        #     os.mkdir(FOLDER_DATA + "revenue_by_country")
        # csv_file_revenue_by_country_name = "revenue_by_country/revenue_by_country" + csv_file_name[index_underscore:]
        # file_path_revenue_by_country = Path(FOLDER_DATA + csv_file_revenue_by_country_name)
        # revenue_by_country(dataframe_order=dataframe, dataframe_customer=dataframe_customer, file_path=file_path_revenue_by_country)

        # Put csv_files
        client.fput_object(bucket_name=BUCKET_GOLD, object_name=csv_file_sales_by_day_name, file_path=file_path_sales_by_day)
        client.fput_object(bucket_name=BUCKET_GOLD, object_name=csv_file_top_product_name, file_path=file_path_top_product)
        client.fput_object(bucket_name=BUCKET_GOLD, object_name=csv_file_aov_name, file_path=file_path_aov)
        client.fput_object(bucket_name=BUCKET_GOLD, object_name=csv_file_revenue_by_channel_name, file_path=file_path_revenue_by_channel)
        # client.fput_object(bucket_name=BUCKET_GOLD, object_name=csv_file_revenue_by_country_name, file_path=file_path_revenue_by_country)

        # Clean local directory
        os.remove(file_path)
        os.remove(file_path_sales_by_day)
        os.remove(file_path_top_product)
        os.remove(file_path_aov)
        os.remove(file_path_revenue_by_channel)
        # os.remove(file_path_customer)
        # os.remove(file_path_revenue_by_country)
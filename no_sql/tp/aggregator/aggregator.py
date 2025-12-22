import datetime
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import psycopg
import pymongo

DIR_PATH = Path(__file__).parent.resolve()
URI_MONGO = "mongodb://admin:admin123@localhost:27017"
URI_POSTGRESQL = "postgresql://analyst:analyst123@localhost:5432/gold_db"


# ===
# Logger
# ===


def setup_logger(
    name, log_file: Path = None, level: Literal[10, 20, 30, 40, 50] = logging.INFO
):
    """Set up logger."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# ===
# MODELS
# ===


@dataclass
class CustomerMetric:
    customer_id: str
    full_name: str
    country: str
    city: str
    total_transactions: int
    total_spent: float
    avg_transaction_amount: float
    first_purchase_date: datetime.date
    last_purchase_date: datetime.date


@dataclass
class ProductPerformance:
    product: str
    total_sales: int
    total_revenue: float
    avg_price: float
    unique_customers: int


@dataclass
class CampaignPerformance:
    campaign_id: str
    campaign_name: str
    campaign_type: str
    total_impressions: int
    total_clicks: int
    total_conversions: int
    avg_ctr: float
    avg_conversion_rate: float
    avg_cpc: float
    avg_cpa: float
    roi: float
    status: str


@dataclass
class MonthlyRevenue:
    month: datetime.date
    total_revenue: float
    total_transactions: float
    unique_customers: int
    avg_transaction_value: float


@dataclass
class CountryStatistics:
    country: str
    total_customers: int
    total_revenue: float
    avg_customer_value: float
    marketing_consent_rate: float


# ===
# Initialization DB
# ===


def init_db():
    try:
        with psycopg.connect(URI_POSTGRESQL) as connection:
            with connection.cursor() as cursor:
                # DROP TABLES
                cursor.execute("DROP TABLE IF EXISTS customer_metrics;")
                cursor.execute("DROP TABLE IF EXISTS product_performance;")
                cursor.execute("DROP TABLE IF EXISTS campaign_performance;")
                cursor.execute("DROP TABLE IF EXISTS monthly_revenue;")
                cursor.execute("DROP TABLE IF EXISTS country_statistics;")
                # CREATE TABLES
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS customer_metrics (
                        customer_id VARCHAR(255) PRIMARY KEY,
                        full_name VARCHAR(255),
                        country VARCHAR(255),
                        city VARCHAR(255),
                        total_transactions INTEGER,
                        total_spent NUMERIC(10,2),
                        avg_transaction_amount FLOAT,
                        first_purchase_date DATE,
                        last_purchase_date DATE
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS product_performance (
                        product VARCHAR(255) PRIMARY KEY,
                        total_sales INTEGER,
                        total_revenue NUMERIC(10,2),
                        avg_price FLOAT,
                        unique_customers INTEGER
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS campaign_performance (
                        campaign_id VARCHAR(255) PRIMARY KEY,
                        campaign_name VARCHAR(255),
                        campaign_type VARCHAR(255),
                        total_impressions INTEGER,
                        total_clicks INTEGER,
                        total_conversions INTEGER,
                        avg_ctr FLOAT,
                        avg_conversion_rate FLOAT,
                        avg_cpc FLOAT,
                        avg_cpa FLOAT,
                        roi FLOAT,
                        status VARCHAR(255)
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS monthly_revenue (
                        month DATE PRIMARY KEY,
                        total_revenue NUMERIC(10,2),
                        total_transactions NUMERIC(10,2),
                        unique_customers INTEGER,
                        avg_transaction_value FLOAT
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS country_statistics (
                        country VARCHAR(255) PRIMARY KEY,
                        total_customers INTEGER,
                        total_revenue NUMERIC(10,2),
                        avg_customer_value FLOAT,
                        marketing_consent_rate NUMERIC(10,2)
                    );
                    """
                )
    except Exception as e:
        print(e)


# ===
# Extractor
# ===


class MongoDBExtractor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extract(self, db_name: str, collection_name: str) -> list[dict[str, Any]]:
        try:
            self.logger.info(f"Connexion: {URI_MONGO}")
            with pymongo.MongoClient(URI_MONGO) as client:
                self.logger.info("\tSuccess")
                self.logger.info(f"Extraction : {db_name}/{collection_name}")
                db = client.get_database(db_name)
                collection = db.get_collection(collection_name)
                cursor = collection.find()
                self.logger.info("\tSuccess")
                return [doc for doc in cursor]
        except Exception as e:
            self.logger.error(f"MongoDB extraction error : {e}")
            raise


# ===
# Loader
# ===


class PostgreSQLDBLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def insert_customer_metrics(
        self, list_customer_metrics: list[CustomerMetric]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI_POSTGRESQL}")
            with psycopg.connect(URI_POSTGRESQL) as connection:
                self.logger.info("\tSuccess")
                with connection.cursor() as cursor:
                    for customer_metric in list_customer_metrics:
                        self.logger.info(f"Loading : {customer_metric.customer_id}")
                        cursor.execute(
                            """INSERT INTO customer_metrics (
                                customer_id,
                                full_name,
                                country,
                                city,
                                total_transactions,
                                total_spent,
                                avg_transaction_amount,
                                first_purchase_date,
                                last_purchase_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
                            (
                                customer_metric.customer_id,
                                customer_metric.full_name,
                                customer_metric.country,
                                customer_metric.city,
                                customer_metric.total_transactions,
                                customer_metric.total_spent,
                                customer_metric.avg_transaction_amount,
                                customer_metric.first_purchase_date,
                                customer_metric.last_purchase_date,
                            ),
                        )
                        self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"PostgreSQL loader error : {e}")
            raise

    def insert_product_performance(
        self, list_product_performance: list[ProductPerformance]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI_POSTGRESQL}")
            with psycopg.connect(URI_POSTGRESQL) as connection:
                self.logger.info("\tSuccess")
                with connection.cursor() as cursor:
                    for product_performance in list_product_performance:
                        self.logger.info(f"Loading : {product_performance.product}")
                        cursor.execute(
                            """INSERT INTO product_performance (
                                product,
                                avg_price,
                                total_revenue,
                                total_sales,
                                unique_customers)
                            VALUES (%s, %s, %s, %s, %s) RETURNING *;""",
                            (
                                product_performance.product,
                                product_performance.avg_price,
                                product_performance.total_revenue,
                                product_performance.total_sales,
                                product_performance.unique_customers,
                            ),
                        )
                        self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"PostgreSQL loader error : {e}")
            raise

    def insert_campaign_performance(
        self, list_campaign_performance: list[CampaignPerformance]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI_POSTGRESQL}")
            with psycopg.connect(URI_POSTGRESQL) as connection:
                self.logger.info("\tSuccess")
                with connection.cursor() as cursor:
                    for campaign_performance in list_campaign_performance:
                        self.logger.info(
                            f"Loading : {campaign_performance.campaign_id}"
                        )
                        cursor.execute(
                            """INSERT INTO customer_metrics (
                                campaign_id,
                                campaign_name,
                                campaign_type,
                                total_impressions,
                                total_clicks,
                                total_conversions,
                                avg_ctr,
                                avg_conversion_rate,
                                avg_cpc,
                                avg_cpa,
                                roi,
                                status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
                            (
                                campaign_performance.campaign_id,
                                campaign_performance.campaign_name,
                                campaign_performance.campaign_type,
                                campaign_performance.total_impressions,
                                campaign_performance.total_clicks,
                                campaign_performance.total_conversions,
                                campaign_performance.avg_ctr,
                                campaign_performance.avg_conversion_rate,
                                campaign_performance.avg_cpc,
                                campaign_performance.avg_cpa,
                                campaign_performance.roi,
                                campaign_performance.status,
                            ),
                        )
                        self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"PostgreSQL loader error : {e}")
            raise

    def insert_monthly_revenue(
        self, list_monthly_revenue: list[MonthlyRevenue]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI_POSTGRESQL}")
            with psycopg.connect(URI_POSTGRESQL) as connection:
                self.logger.info("\tSuccess")
                with connection.cursor() as cursor:
                    for monthly_revenue in list_monthly_revenue:
                        self.logger.info(f"Loading : {monthly_revenue.month}")
                        cursor.execute(
                            """INSERT INTO customer_metrics (
                                month,
                                total_revenue,
                                total_transactions,
                                unique_customers,
                                avg_transaction_value)
                            VALUES (%s, %s, %s, %s, %s) RETURNING *;""",
                            (
                                monthly_revenue.month,
                                monthly_revenue.total_revenue,
                                monthly_revenue.total_transactions,
                                monthly_revenue.unique_customers,
                                monthly_revenue.avg_transaction_value,
                            ),
                        )
                        self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"PostgreSQL loader error : {e}")
            raise

    def insert_country_statistics(
        self, list_country_statistics: list[CountryStatistics]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI_POSTGRESQL}")
            with psycopg.connect(URI_POSTGRESQL) as connection:
                self.logger.info("\tSuccess")
                with connection.cursor() as cursor:
                    for country_statistics in list_country_statistics:
                        self.logger.info(f"Loading : {country_statistics.country}")
                        cursor.execute(
                            """INSERT INTO customer_metrics (
                                country,
                                total_customers,
                                total_revenue,
                                avg_customer_value,
                                marketing_consent_rate)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;""",
                            (
                                country_statistics.country,
                                country_statistics.total_customers,
                                country_statistics.total_revenue,
                                country_statistics.avg_customer_value,
                                country_statistics.marketing_consent_rate,
                            ),
                        )
                        self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"PostgreSQL loader error : {e}")
            raise


# ===
# Pipelines
# ===


class PipelineCustomerMetrics:
    def __init__(self, config: dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.extractor = MongoDBExtractor(logger=self.logger)
        self.loader = PostgreSQLDBLoader(logger=self.logger)

    def run(self):
        try:
            self.logger.info("Pipeline customer_metrics start")
            self.logger.info("[1/3] Extraction")
            data_extracted = self._extract()
            self.logger.info("[2/3] Transformation")
            data_transformed = self._transform(data_extracted)
            self.logger.info("[3/3] Loading")
            self._load(data_transformed)
            self.logger.info("Pipeline customers end")
        except Exception as e:
            self.logger.error(f"Pipeline customers error : {e}")

    def _extract(self) -> pd.DataFrame:
        df_customers = pd.DataFrame(
            self.extractor.extract(
                db_name=self.config["db_silver"],
                collection_name=self.config["collection_customers"],
            )
        )
        df_transactions = pd.DataFrame(
            self.extractor.extract(
                db_name=self.config["db_silver"],
                collection_name=self.config["collection_transactions"],
            )
        )
        return pd.merge(
            left=df_customers, right=df_transactions, how="right", on="customer_id"
        )

    def _transform(self, df: pd.DataFrame) -> list[CustomerMetric]:
        df_customer_metrics = df.groupby(["customer_id"], as_index=False).agg(
            full_name=(
                "full_name",
                lambda x: pd.Series.mode(x)[0]
                if not pd.Series.mode(x).empty
                else "Unknown",
            ),
            country=(
                "country",
                lambda x: pd.Series.mode(x)[0]
                if not pd.Series.mode(x).empty
                else "Unknown",
            ),
            city=(
                "city",
                lambda x: pd.Series.mode(x)[0]
                if not pd.Series.mode(x).empty
                else "Unknown",
            ),
            total_transactions=("customer_id", "count"),
            total_spent=("amount", "sum"),
            avg_transaction_amount=("amount", "mean"),
            first_purchase_date=("timestamp", "min"),
            last_purchase_date=("timestamp", "max"),
        )

        return [
            CustomerMetric(**data)
            for data in df_customer_metrics.to_dict(orient="records")
        ]

    def _load(self, list_customer_metrics: list[CustomerMetric]) -> None:
        self.loader.insert_customer_metrics(list_customer_metrics)


def main():
    logger_path = DIR_PATH / "aggregator.log"
    logger = setup_logger(name="aggregator", log_file=logger_path)
    config = {
        "db_silver": "silver_db",
        "collection_customers": "customers",
        "collection_transactions": "transactions",
        "collection_campaigns": "campaigns",
    }
    init_db()
    pipeline_customers = PipelineCustomerMetrics(config=config, logger=logger)
    pipeline_customers.run()


if __name__ == "__main__":
    main()

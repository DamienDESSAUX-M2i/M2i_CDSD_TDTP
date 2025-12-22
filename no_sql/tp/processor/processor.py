import hashlib
import logging
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
import pymongo

DIR_PATH = Path(__file__).parent.resolve()
URI = "mongodb://admin:admin123@localhost:27017"


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


class MongoDBExtractor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extract(self, db_name: str, collection_name: str) -> list[dict[str, Any]]:
        try:
            self.logger.info(f"Connexion: {URI}")
            with pymongo.MongoClient(URI) as client:
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


class MongoDBLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load(
        self, db_name: str, collection_name: str, data: list[dict[str, Any]]
    ) -> None:
        try:
            self.logger.info(f"Connexion: {URI}")
            with pymongo.MongoClient(URI) as client:
                self.logger.info("\tSuccess")
                self.logger.info(f"Loading : {db_name}/{collection_name}")
                db = client.get_database(db_name)
                collection = db.get_collection(collection_name)
                collection.insert_many(data)
                self.logger.info(f"\tSuccess: {len(data)} records loaded.")
        except Exception as e:
            self.logger.error(f"MongoDB loader error : {e}")
            raise


class PipelineCustomers:
    def __init__(self, config: dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.extractor = MongoDBExtractor(logger=self.logger)
        self.loader = MongoDBLoader(logger=self.logger)

    def run(self):
        try:
            self.logger.info("Pipeline customers start")
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
        return pd.DataFrame(
            self.extractor.extract(
                db_name=self.config["db_bronze"],
                collection_name=self.config["collection_customers"],
            )
        )

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("\tDrop duplicates")
        df.drop_duplicates()

        self.logger.info("\tFill NAN")
        df["first_name"] = df["first_name"].fillna(value="Unknown")
        df["last_name"] = df["last_name"].fillna(value="Unknown")
        df["email"] = df["email"].fillna(value="Unknown")
        df["phone"] = df["phone"].fillna(value="Unknown")
        df["age"] = df["age"].fillna(value=0)
        df["country"] = df["country"].fillna(value="Unknown")
        df["city"] = df["city"].fillna(value="Unknown")
        df["gender"] = df["gender"].fillna(value="Unknown")
        df["marketing_consent"] = df["marketing_consent"].fillna(value="Unknown")

        self.logger.info("\tConcat first_name and last_name")
        df["full_name"] = df[["first_name", "last_name"]].agg("_".join, axis=1)
        df.drop(columns=["first_name", "last_name"], inplace=True)

        self.logger.info("\tHash email")
        df["email"] = df["email"].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

        self.logger.info("\tHash phone")
        df["phone"] = df["phone"].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

        return df

    def _load(self, df: pd.DataFrame) -> None:
        self.loader.load(
            db_name=self.config["db_silver"],
            collection_name=self.config["collection_customers"],
            data=df.to_dict(orient="records"),
        )


class PipelineTransactions:
    def __init__(self, config: dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.extractor = MongoDBExtractor(logger=self.logger)
        self.loader = MongoDBLoader(logger=self.logger)

    def run(self):
        try:
            self.logger.info("Pipeline customers start")
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
        return pd.DataFrame(
            self.extractor.extract(
                db_name=self.config["db_bronze"],
                collection_name=self.config["collection_transactions"],
            )
        )

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("\tDrop duplicates")
        df.drop_duplicates()

        self.logger.info("\tFill NAN")
        df["customer_id"] = df["customer_id"].fillna(value="Unknown")
        df["product"] = df["product"].fillna(value="Unknown")
        df["amount"] = df["amount"].fillna(value=0)
        df["quantity"] = df["quantity"].fillna(value=0)
        df["payment_method"] = df["payment_method"].fillna(value="Unknown")
        df["discount_applied"] = df["discount_applied"].fillna(value=0)
        df["shipping_cost"] = df["shipping_cost"].fillna(value=0)

        self.logger.info("\tCompute total_amout")
        df["total_amout"] = (
            df["quantity"] * df["amount"] * (1 - df["discount_applied"] / 100)
        )

        return df

    def _load(self, df: pd.DataFrame) -> None:
        self.loader.load(
            db_name=self.config["db_silver"],
            collection_name=self.config["collection_transactions"],
            data=df.to_dict(orient="records"),
        )


class PipelineCampaigns:
    def __init__(self, config: dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.extractor = MongoDBExtractor(logger=self.logger)
        self.loader = MongoDBLoader(logger=self.logger)

    def run(self):
        try:
            self.logger.info("Pipeline campaigns start")
            self.logger.info("[1/3] Extraction")
            data_extracted = self._extract()
            self.logger.info("[2/3] Transformation")
            data_transformed = self._transform(data_extracted)
            self.logger.info("[3/3] Loading")
            self._load(data_transformed)
            self.logger.info("Pipeline campaigns end")
        except Exception as e:
            self.logger.error(f"Pipeline campaigns error : {e}")

    def _extract(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.extractor.extract(
                db_name=self.config["db_bronze"],
                collection_name=self.config["collection_campaigns"],
            )
        )

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("\tDrop duplicates")
        df.drop_duplicates()

        self.logger.info("\tFill NAN")
        df["campaign_name"] = df["campaign_name"].fillna(value="Unknown")
        df["campaign_type"] = df["campaign_type"].fillna(value="Unknown")
        df["budget"] = df["budget"].fillna(value=0)
        df["spend"] = df["spend"].fillna(value=0)
        df["impressions"] = df["impressions"].fillna(value=0)
        df["clicks"] = df["clicks"].fillna(value=0)
        df["conversions"] = df["conversions"].fillna(value=0)
        df["target_audience"] = df["target_audience"].fillna(value="Unknown")
        df["status"] = df["status"].fillna(value="Unknown")

        self.logger.info("\tCompute KPI")
        df["CTR"] = (df["clicks"] / df["impressions"]) * 100
        df["conversion_rate"] = (df["conversions"] / df["clicks"]) * 100
        df["CPC"] = df["spend"] / df["clicks"]
        df["CPA"] = df["clicks"] / df["conversions"]
        df["ROI"] = ((df["budget"] - df["spend"]) / df["budget"]) * 100

        # Replace nan, inf and -inf
        df["CTR"].replace([np.nan, np.inf, -np.inf], 0, inplace=True)
        df["conversion_rate"].replace([np.nan, np.inf, -np.inf], 0, inplace=True)
        df["CPC"].replace([np.nan, np.inf, -np.inf], 0, inplace=True)
        df["CPA"].replace([np.nan, np.inf, -np.inf], 0, inplace=True)
        df["ROI"].replace([np.nan, np.inf, -np.inf], 0, inplace=True)

        return df

    def _load(self, df: pd.DataFrame) -> None:
        self.loader.load(
            db_name=self.config["db_silver"],
            collection_name=self.config["collection_campaigns"],
            data=df.to_dict(orient="records"),
        )


def main():
    logger_path = DIR_PATH / "processor.log"
    logger = setup_logger(name="processor", log_file=logger_path)
    config = {
        "db_bronze": "bronze_db",
        "db_silver": "silver_db",
        "collection_customers": "customers",
        "collection_transactions": "transactions",
        "collection_campaigns": "campaigns",
    }
    pipeline_customers = PipelineCustomers(config=config, logger=logger)
    pipeline_customers.run()
    pipeline_transactions = PipelineTransactions(config=config, logger=logger)
    pipeline_transactions.run()
    pipeline_campaigns = PipelineCampaigns(config=config, logger=logger)
    pipeline_campaigns.run()


if __name__ == "__main__":
    main()

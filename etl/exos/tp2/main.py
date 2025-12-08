import os
from pathlib import Path

from dotenv import load_dotenv
from src.pipelines.etl_pipeline import ETLPipeline
from src.utils.config import load_config
from src.utils.logger import setup_logger

DIR_PATH = Path(__file__).parent.resolve()
load_dotenv(DIR_PATH / "config" / ".env")

API_KEY = os.getenv("API_KEY")


def main():
    logger = setup_logger("ETL", DIR_PATH / "logs" / "etl.log")
    config = load_config(DIR_PATH / "config" / "config.yaml")
    pipeline = ETLPipeline(
        config=config, logger=logger, dir_path=DIR_PATH, api_key=API_KEY
    )
    pipeline.run()


if __name__ == "__main__":
    main()

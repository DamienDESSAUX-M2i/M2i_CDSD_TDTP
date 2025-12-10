import pandas as pd
import requests
from src.extractor import WebScrapingExtractor
from src.loader import EXCELLoader
from src.transformer import ResponsesTransformer


class ETLPipeline:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.web_scraping_extractor = WebScrapingExtractor(logger=logger)
        self.responses_transformer = ResponsesTransformer(logger=logger)
        self.excel_loader = EXCELLoader(logger=logger)

    def run(self):
        try:
            self.logger.info("=" * 3)
            self.logger.info("PIPELINE ETL STARTED")
            self.logger.info("=" * 3)

            self.logger.info("[1/3] EXTRACTION")
            responses = self._extract()

            self.logger.info("[2/3] TRANSFORMATION")
            dataset = self._transform(responses)

            self.logger.info("[3/3] LOADING")
            self._load(dataset)

            self.logger.info("=" * 3)
            self.logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 3)

        except Exception as e:
            self.logger.error(f"PIPELINE ERROR : {e}")

    def _extract(self) -> list[requests.Response]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
        }
        return self.web_scraping_extractor.fetch_pages_auto(
            base_url=self.config["BASE_URL"],
            headers=headers,
            max_pages=self.config["MAX_PAGES"],
        )

    def _transform(self, responses: list[requests.Response]) -> dict[str, pd.DataFrame]:
        dict_dataframes = self.responses_transformer.transform(responses=responses)
        dict_dataframes.update(self.responses_transformer.stats(dict_dataframes))
        return dict_dataframes

    def _load(self, dict_dataframes: dict[str, pd.DataFrame]) -> None:
        file_path = self.config["DIR_OUTPUT"] / "report.xlsx"
        self.excel_loader.load(dict_dataframes, file_path)

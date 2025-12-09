import pandas as pd
import requests
from src.extractor import WebScrapingExtractor
from src.loader import CSVLoader, HTMLLoader
from src.transformer import ResponsesTransformer


class ETLPipeline:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.web_scraping_extractor = WebScrapingExtractor(logger=logger)
        self.responses_transformer = ResponsesTransformer(logger=logger)
        self.html_loader = HTMLLoader(logger=logger)
        self.csv_loader = CSVLoader(logger=logger)

    def run(self):
        try:
            self.logger.info("=" * 3)
            self.logger.info("PIPELINE ETL STARTED")
            self.logger.info("=" * 3)

            self.logger.info("[1/3] EXTRACTION")
            responses = self._extract()

            self.logger.info("[2/3] TRANSFORMATION")
            responses_html, df = self._transform(responses)

            self.logger.info("[3/3] LOADING")
            self._load(responses_html, df)

            self.logger.info("=" * 3)
            self.logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 3)

        except Exception as e:
            self.logger.error(f"PIPELINE ERROR : {e}")

    def _extract(self) -> list[requests.Response]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:145.0) Gecko/20100101 Firefox/145.0"
        }
        return self.web_scraping_extractor.fetch_pages(
            base_url=self.config["BASE_URL"],
            headers=headers,
            nb_pages=self.config["NB_PAGES"],
        )

    def _transform(self, responses: list[requests.Response]) -> pd.DataFrame:
        return self.responses_transformer.transform(responses=responses)

    def _load(self, responses_html, df):
        self.html_loader.load(
            directory=self.config["DIR_OUTPUT"], responses_html=responses_html
        )
        self.csv_loader.load(directory=self.config["DIR_OUTPUT"], df=df)

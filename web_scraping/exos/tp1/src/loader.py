import logging
from pathlib import Path

import pandas as pd


class HTMLLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load(self, directory: Path, responses_html: list[str]) -> None:
        if not directory.exists():
            directory.mkdir()

        try:
            for k in range(1, len(responses_html) + 1):
                html_path = directory / f"page{k}.html"
                self.logger.info(f"Save page{k} to : {html_path}")
                with open(html_path, "wt", encoding="utf-8") as f:
                    f.writelines(responses_html[k - 1])
                self.logger.info("\tSuccess")
        except Exception as e:
            print(f"HTML Loader Error : {e}")
            raise


class CSVLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load(self, df: pd.DataFrame, directory: Path) -> None:
        if not directory.exists():
            directory.mkdir()

        try:
            csv_path = directory / "report.csv"
            self.logger.info(f"Save DataFrame to : {csv_path}")
            df.to_csv(csv_path, index=False)
            self.logger.info("\tSuccess")
        except Exception as e:
            print(f"CSV Loader Error : {e}")
            raise

import logging
from pathlib import Path

import pandas as pd


class EXCELLoader:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def load(self, dict_dataframes: dict[str, pd.DataFrame], file_path: Path):
        """Charge plusieurs feuilles Excel"""
        try:
            self.logger.info(f"Load to {file_path}")
            with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
                for sheet_name, df in dict_dataframes.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    self.logger.info(f"\tSheet load '{sheet_name}'")
            self.logger.info("\tSuccess")
        except Exception as e:
            self.logger.error(f"EXCEL Loader Error : {e}")
            raise

from logging import Logger
from typing import Callable

import pandas as pd


class DataTransformer:
    """Transformateur de données"""

    def __init__(self, logger: Logger):
        self.logger = logger

    def clean(self, df: pd.DataFrame):
        """Nettoie les données"""
        try:
            self.logger.info("Nettoyage des données")
            initial_count = len(df)

            df = df.drop_duplicates()
            self.logger.info(f"  - {initial_count - len(df)} doublons supprimés")

            df = df.dropna(axis=1, how="all")

            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].str.strip()

            self.logger.info(f"Nettoyage terminé: {len(df)} lignes")
            return df

        except Exception as e:
            self.logger.error(f"Erreur nettoyage: {e}")
            raise

    def validate(self, df: pd.DataFrame, required_columns: list[str]):
        """Valide la structure des données"""
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Colonnes manquantes: {missing_cols}")

        self.logger.info("Validation réussie")
        return True

    def enrich(self, df: pd.DataFrame, enrichment_func: Callable):
        """Enrichit les données"""
        try:
            self.logger.info("Enrichissement des données")
            df = enrichment_func(df)
            self.logger.info("Enrichissement terminé")
            return df
        except Exception as e:
            self.logger.error(f"Erreur enrichissement: {e}")
            raise

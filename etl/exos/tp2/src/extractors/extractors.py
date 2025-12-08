import json
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
import requests


class BaseExtractor(ABC):
    """Classe de base pour les extracteurs"""

    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    def extract(self) -> Any:
        """Logique d'extraction"""
        raise NotImplementedError


class CSVExtractor(BaseExtractor):
    """Extracteur pour fichiers CSV"""

    def extract(self, filepath) -> pd.DataFrame:
        """Extrait données d'un CSV"""
        try:
            self.logger.info(f"Extraction de {filepath}")
            df = pd.read_csv(filepath)
            self.logger.info(f"{len(df)} lignes extraites")
            return df
        except Exception as e:
            self.logger.error(f"Erreur extraction CSV: {e}")
            raise


class APIExtractor(BaseExtractor):
    """Extracteur pour API REST"""

    def __init__(self, logger, base_url, api_key=None):
        super().__init__(logger)
        self.base_url = base_url
        self.api_key = api_key

    def extract(self, endpoint, params=None):
        """Extrait données d'une API"""
        try:
            self.logger.info(f"Extraction de {self.base_url}/{endpoint}")
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            self.logger.info("Données extraites")
            return data
        except Exception as e:
            self.logger.error(f"Erreur extraction API: {e}")
            raise


class JSONExtractor(BaseExtractor):
    def extract(self, filepath):
        """Extrait données d'un JSON"""
        try:
            self.logger.info(f"Extraction de {filepath}")

            with open(filepath, "r", encoding="utf-8") as f:
                data: dict = json.load(f)

            df_data = {"produit_id": [], "nom": [], "categorie": []}
            for key in data.keys():
                df_data["produit_id"].append(int(key))
                df_data["nom"].append(data[key]["nom"])
                df_data["categorie"].append(data[key]["categorie"])
            df = pd.DataFrame(df_data)

            self.logger.info(f"{len(df)} lignes extraites")

            return df

        except Exception as e:
            self.logger.error(f"Erreur extraction JSON: {e}")
            raise

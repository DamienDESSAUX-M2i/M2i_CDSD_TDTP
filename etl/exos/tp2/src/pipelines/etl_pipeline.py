import os
from pathlib import Path

import pandas as pd
from src.extractors.extractors import APIExtractor, CSVExtractor, JSONExtractor
from src.loaders.loader import DataLoader
from src.pipelines.base_etl_pipeline import BaseETLPipeline
from src.transformers.cleaner import DataTransformer


class ETLPipeline(BaseETLPipeline):
    """Pipeline ETL"""

    def __init__(self, config, logger, dir_path: Path, api_key):
        super().__init__(config, logger)
        self.dir_path = dir_path
        self.api_key = api_key

    def _extract(self) -> pd.DataFrame:
        """Extraction des posts depuis l'API JSONPlaceholder."""

        base_url = self.config["api_meteo"]["base_url"]
        extractor_api = APIExtractor(
            logger=self.logger, base_url=base_url, api_key=None
        )
        params = {"q": "Lille", "appid": self.api_key, "units": "metric", "lang": "fr"}
        data = extractor_api.extract("weather", params=params)
        self.logger.info("Transformation données météo")
        dict_data = {"name": [], "temp": []}
        dict_data["name"].append(data["name"])
        dict_data["temp"].append(data["main"]["temp"])
        df_meteo = pd.DataFrame(dict_data)
        self.logger.info("Données météo transformée")

        extractor_csv = CSVExtractor(logger=self.logger)
        df_ventes = extractor_csv.extract(
            filepath=self.dir_path / self.config["csv_ventes"]["path"]
        )

        extraction_json = JSONExtractor(logger=self.logger)
        df_produits = extraction_json.extract(
            filepath=self.dir_path / self.config["json_produits"]["path"]
        )

        return (df_meteo, df_ventes, df_produits)

    def _transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Nettoie, valide et enrichit les données issues de l'API."""
        df_meteo, df_ventes, df_produits = data

        df_merge = pd.merge(df_ventes, df_produits, how="inner", on="produit_id")
        transformer = DataTransformer(logger=self.logger)
        df_clean = transformer.clean(df_merge)

        required_cols = [
            "date",
            "produit_id",
            "quantite",
            "prix_unitaire",
            "client_id",
            "nom",
            "categorie",
        ]
        transformer.validate(df_clean, required_cols)

        df_clean["date"] = pd.to_datetime(df_clean["date"])

        def add_total_amout(df: pd.DataFrame) -> pd.DataFrame:
            df = df.copy()
            df["montant_total"] = df["quantite"] * df["prix_unitaire"]
            return df

        df_enriched: pd.DataFrame = transformer.enrich(df_clean, add_total_amout)

        df_agg_produit = (
            df_enriched.groupby("nom")
            .agg({"quantite": "sum", "montant_total": "sum"})
            .reset_index()
            .rename(
                columns={"quantite": "total_quantite", "montant_total": "total_vente"}
            )
            .sort_values("total_vente", ascending=False)
        )

        df_agg_categorie = (
            df_enriched.groupby("categorie")
            .agg({"quantite": "sum", "montant_total": "sum"})
            .reset_index()
            .rename(
                columns={"quantite": "total_quantite", "montant_total": "total_vente"}
            )
            .sort_values("total_vente", ascending=False)
        )

        return (df_meteo, df_enriched, df_agg_produit, df_agg_categorie)

    def _load(self, data: pd.DataFrame) -> None:
        """Charge les données transformées dans un fichier Excel."""

        df_meteo, df_enriched, df_agg_produit, df_agg_categorie = data
        dataframes_dict = {
            "Métadonnées": df_meteo,
            "Ventes détaillées": df_enriched,
            "Par produit": df_agg_produit,
            "Par catégorie": df_agg_categorie,
        }

        output_dir = self.config["paths"]["output"]
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(self.dir_path / output_dir, "posts_api.xlsx")

        loader = DataLoader(logger=self.logger)
        loader.load_multiple_sheets(
            dataframes_dict=dataframes_dict, filepath=output_file
        )

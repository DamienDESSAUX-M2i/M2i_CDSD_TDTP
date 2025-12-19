"""Pipeline de données pour les citations."""

from datetime import datetime
from typing import Optional

import pandas as pd
import structlog
from tqdm import tqdm

from src.scrapper import Product, ProductsScraper
from src.storage import MinIOStorage, MongoDBStorage

logger = structlog.get_logger()


class ProductsPipeline:
    """
    Pipeline ETL pour les produits.

    Workflow :
    1. Extract : Scraping des produits
    2. Transform : Nettoyage et enrichissement
    3. Load : Stockage MongoDB + exports MinIO
    """

    def __init__(self):
        self.scraper = ProductsScraper()
        self.minio = MinIOStorage()
        self.mongodb = MongoDBStorage()
        self.stats = {"products_scraped": 0, "errors": []}

    def process_product(self, product: Product) -> Optional[dict]:
        """Traite et stocke un produit."""
        try:
            product_data = product.to_dict()
            self.mongodb.insert_product(product_data)
            self.stats["products_scraped"] += 1
            return product_data
        except Exception as e:
            self.stats["errors"].append(str(e))
            return None

    def run(
        self,
        max_pages: int = 10,
        show_progress: bool = True,
    ) -> dict:
        """
        Exécute le pipeline complet.

        Args:
            max_pages: Nombre max de pages
            show_progress: Afficher la progression

        Returns:
            Statistiques d'exécution
        """
        start_time = datetime.utcnow()
        logger.info("pipeline_started", max_pages=max_pages)

        try:
            # Scrape complet
            data = self.scraper.scrape_complete(max_pages=max_pages)

            # Traiter les produits
            products = data["products"]
            iterator = (
                tqdm(products, desc="Processing products")
                if show_progress
                else products
            )

            for product in iterator:
                self.process_product(product)

            # Log du run
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.mongodb.log_scraping_run(
                status="success",
                products_scraped=self.stats["products_scraped"],
                duration_seconds=duration,
                errors=self.stats["errors"],
            )

        except Exception as e:
            logger.error("pipeline_failed", error=str(e))
            self.mongodb.log_scraping_run(
                status="failed",
                products_scraped=self.stats["products_scraped"],
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                errors=[str(e)],
            )

        finally:
            end_time = datetime.utcnow()
            self.stats["duration_seconds"] = (end_time - start_time).total_seconds()
            self.stats["start_time"] = start_time.isoformat()
            self.stats["end_time"] = end_time.isoformat()

        logger.info("pipeline_completed", stats=self.stats)
        return self.stats

    def export_csv(self, filepath: str = None) -> Optional[str]:
        """
        Exporte les produits en CSV.

        Args:
            filepath: Chemin local (optionnel)

        Returns:
            URI MinIO
        """
        products = self.mongodb.find_products(limit=10000)

        if not products:
            return None

        # Convertir en DataFrame
        df = pd.DataFrame(products)

        # Nettoyer
        if "_id" in df.columns:
            df["_id"] = df["_id"].astype(str)

        # Sauvegarder localement
        if filepath:
            df.to_csv(filepath, index=False)

        # Upload vers MinIO
        csv_content = df.to_csv(index=False)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        return self.minio.upload_csv(csv_content, f"products_export_{timestamp}.csv")

    def export_json(self) -> Optional[str]:
        """Exporte toutes les données en JSON."""
        data = self.mongodb.get_all_data()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        return self.minio.upload_json(data, f"full_export_{timestamp}.json")

    def create_backup(self) -> Optional[str]:
        """Crée une sauvegarde complète."""
        data = self.mongodb.get_all_data()
        return self.minio.create_backup(data, "products_backup")

    def get_analytics(self) -> dict:
        """Génère un rapport d'analytics."""
        return {
            "overview": self.mongodb.get_stats(),
            "storage": self.minio.get_storage_stats(),
            "scraping_history": self.mongodb.get_scraping_history(5),
        }

    def close(self) -> None:
        """Ferme les connexions."""
        self.scraper.close()
        self.mongodb.close()

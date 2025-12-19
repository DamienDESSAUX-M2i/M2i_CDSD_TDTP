from datetime import datetime
from typing import Any, Optional

import structlog
from config.settings import mongo_config
from pymongo import ASCENDING, DESCENDING, TEXT, MongoClient
from pymongo.errors import PyMongoError

logger = structlog.get_logger()


class MongoDBStorage:
    """
    Gestionnaire MongoDB pour les données structurées.

    Collections :
    - produits : Produits avec titre, prix, description, avis, image_url et details_url
    - scraping_logs : Historique des exécutions
    """

    def __init__(self):
        self.client = MongoClient(mongo_config.connection_string)
        self.db = self.client[mongo_config.database]
        self.products = self.db["produits"]
        self.stats = self.db["stats"]
        self.scraping_logs = self.db["scraping_logs"]
        self._create_indexes()

    def _create_indexes(self) -> None:
        """Crée les index pour optimiser les requêtes."""
        # Index sur les produits
        self.products.create_index([("title", TEXT)])
        self.products.create_index([("price", ASCENDING)])
        self.products.create_index([("rating", ASCENDING)])
        self.products.create_index([("scraped_at", DESCENDING)])

        logger.info("mongodb_indexes_created")

    # ============ PRODUITS ============

    def insert_product(self, product: dict) -> Optional[str]:
        """
        Insère ou met à jour un produit.

        Args:
            product: {title, price, description, rating, ...}

        Returns:
            ID du document ou None
        """
        try:
            product["scraped_at"] = datetime.utcnow()
            product["updated_at"] = datetime.utcnow()

            # Upsert basé sur title
            result = self.products.update_one(
                {"title": product["title"]},
                {"$set": product},
                upsert=True,
            )

            if result.upserted_id:
                logger.debug("product_inserted", title=product["title"])
                return str(result.upserted_id)

            return "updated"

        except PyMongoError as e:
            logger.error("product_insert_failed", error=str(e))
            return None

    def bulk_insert_products(self, products: list[dict]) -> dict:
        """Insère plusieurs citations."""
        results = {"inserted": 0, "updated": 0, "errors": 0}

        for product in products:
            result = self.insert_product(product)
            if result == "updated":
                results["updated"] += 1
            elif result:
                results["inserted"] += 1
            else:
                results["errors"] += 1

        return results

    def find_products(
        self,
        query: dict = None,
        projection: dict = None,
        sort: list = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[dict]:
        """Recherche des products."""
        query = query or {}
        cursor = self.products.find(query, projection)

        if sort:
            cursor = cursor.sort(sort)

        return list(cursor.skip(skip).limit(limit))

    def get_products_by_rating(self, rating: int) -> list[dict]:
        """Récupère toutes les citations d'un auteur."""
        return self.find_products({"rating": rating})

    # ============ STATS ============

    def get_stats(self) -> dict:
        """Statistiques globales."""
        return {
            "total_products": self.products.count_documents({}),
        }

    # def _avg_tags_per_quote(self) -> float:
    #     """Calcule le nombre moyen de tags par citation."""
    #     pipeline = [
    #         {"$project": {"tag_count": {"$size": "$tags"}}},
    #         {"$group": {"_id": None, "avg": {"$avg": "$tag_count"}}},
    #     ]
    #     result = list(self.quotes.aggregate(pipeline))
    #     return result[0]["avg"] if result else 0

    # def get_quotes_by_author_stats(self) -> list[dict]:
    #     """Nombre de citations par auteur."""
    #     pipeline = [
    #         {
    #             "$group": {
    #                 "_id": "$author",
    #                 "quote_count": {"$sum": 1},
    #                 "tags": {"$push": "$tags"},
    #             }
    #         },
    #         {"$sort": {"quote_count": -1}},
    #     ]
    #     return list(self.quotes.aggregate(pipeline))

    # def get_tag_co_occurrence(self) -> list[dict]:
    #     """
    #     Analyse la co-occurrence des tags.
    #     Quels tags apparaissent souvent ensemble ?
    #     """
    #     pipeline = [
    #         {"$unwind": "$tags"},
    #         {"$group": {"_id": "$_id", "tags": {"$push": "$tags"}}},
    #         {"$match": {"tags.1": {"$exists": True}}},  # Au moins 2 tags
    #         {"$unwind": "$tags"},
    #         {"$group": {"_id": "$tags", "co_tags": {"$push": "$tags"}}},
    #     ]
    #     return list(self.quotes.aggregate(pipeline))

    # def get_author_tag_analysis(self) -> list[dict]:
    #     """Analyse des tags préférés par auteur."""
    #     pipeline = [
    #         {"$unwind": "$tags"},
    #         {
    #             "$group": {
    #                 "_id": {"author": "$author", "tag": "$tags"},
    #                 "count": {"$sum": 1},
    #             }
    #         },
    #         {"$sort": {"count": -1}},
    #         {
    #             "$group": {
    #                 "_id": "$_id.author",
    #                 "top_tags": {"$push": {"tag": "$_id.tag", "count": "$count"}},
    #             }
    #         },
    #     ]
    #     return list(self.quotes.aggregate(pipeline))

    # def get_quote_length_distribution(self) -> list[dict]:
    #     """Distribution de la longueur des citations."""
    #     pipeline = [
    #         {"$project": {"length": {"$strLenCP": "$text"}, "author": 1}},
    #         {
    #             "$bucket": {
    #                 "groupBy": "$length",
    #                 "boundaries": [0, 50, 100, 150, 200, 300, 500],
    #                 "default": "500+",
    #                 "output": {
    #                     "count": {"$sum": 1},
    #                     "authors": {"$addToSet": "$author"},
    #                 },
    #             }
    #         },
    #     ]
    #     return list(self.quotes.aggregate(pipeline))

    # ============ LOGS ============

    def log_scraping_run(
        self,
        status: str,
        products_scraped: int,
        duration_seconds: float,
        errors: list = None,
    ) -> None:
        """Enregistre un log de scraping."""
        self.scraping_logs.insert_one(
            {
                "timestamp": datetime.utcnow(),
                "status": status,
                "products_scraped": products_scraped,
                "duration_seconds": duration_seconds,
                "errors": errors or [],
            }
        )

    def get_scraping_history(self, limit: int = 10) -> list[dict]:
        """Historique des runs."""
        return list(
            self.scraping_logs.find().sort("timestamp", DESCENDING).limit(limit)
        )

    # ============ UTILITAIRES ============

    def count_products(self, query: dict = None) -> int:
        """Compte les citations."""
        return self.products.count_documents(query or {})

    def get_all_data(self) -> dict:
        """Exporte toutes les données."""
        products = list(self.products.find({}, {"_id": 0}))

        return {
            "products": products,
            "exported_at": datetime.utcnow().isoformat(),
        }

    def delete_all(self) -> dict:
        """Supprime toutes les données (reset)."""
        products_deleted = self.products.delete_many({}).deleted_count

        logger.warning("all_data_deleted", products=products_deleted)

        return {"products": products_deleted}

    def close(self) -> None:
        """Ferme la connexion."""
        self.client.close()

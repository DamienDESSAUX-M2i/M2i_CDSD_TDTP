from datetime import datetime
from typing import Optional

import pymongo
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
                {"id_product": product["id_product"]},
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
            "total_computers": self.products.count_documents({"category": "computers"}),
            "total_laptops": self.products.count_documents({"sub_category": "laptops"}),
            "total_tablets": self.products.count_documents({"sub_category": "tablets"}),
            "total_phones": self.products.count_documents({"category": "phones"}),
            "total_touch": self.products.count_documents({"sub_category": "touch"}),
        }

    def get_cheap_laptops(self) -> list[dict]:
        """Trouve les laptops inférieurs à 500€"""
        return self.find_products(
            {"sub_category": "laptops", "price": {"$lt": 500}},
            {"_id": 0, "title": 1, "price": 1},
            [("price", pymongo.DESCENDING)],
        )

    def get_most_expensive_by_cat(self) -> list[dict]:
        """Trouve les produits les plus cher par catégorie"""
        pipeline = [
            {
                "$group": {
                    "_id": {"category": "$category"},
                    "max_price": {"$max": "$price"},
                }
            },
            {"$project": {"_id": 0, "category": "$_id.category", "max_price": 1}},
        ]
        return list(self.products.aggregate(pipeline))

    def get_avg_price_good_rating(self, rating: int) -> float:
        """Calcule la moyenne des prix des produits dont le note est supérieur ou égale à rating"""
        pipeline = [
            {"$match": {"rating": {"$gte": rating}}},
            {"$group": {"_id": None, "avg_price": {"$avg": "$price"}}},
        ]
        result = list(self.products.aggregate(pipeline))
        return result[0]["avg_price"] if result else 0

    def get_brand_products(self, text_inside: list[str]) -> list[dict]:
        """Trouve les produit dont le nom contient un des item de la list text_inside"""
        regex = "|".join(text_inside)
        return self.find_products(
            {"title": {"$regex": regex, "$options": "i"}}, {"_id": 0, "title": 1}
        )

    def get_value_ranking(self) -> list[dict]:
        """Trouve les 10 produits ayant le meilleur score où score=rating/(price/100)"""
        pipeline = [
            {
                "$addFields": {
                    "score": {"$divide": ["$rating", {"$divide": ["$price", 100]}]}
                }
            },
            {"$sort": {"score": -1}},
            {"$limit": 10},
            {"$project": {"_id": 0, "title": 1, "score": 1}},
        ]
        return list(self.products.aggregate(pipeline))

    def get_price_ranges(self) -> list[dict]:
        """Groupe les produits par interval de prix et compte le nombre produits par groupe"""
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$price",
                    "boundaries": [0, 200, 500, 1000, float("inf")],
                    "default": "out_of_range",
                    "output": {
                        "number_of_products": {"$sum": 1},
                    },
                }
            }
        ]
        return list(self.products.aggregate(pipeline))

    def get_same_price_products(self) -> list[dict]:
        """Trouve les produits ayant le même prix"""
        pipeline = [
            {"$group": {"_id": {"price": "$price"}, "nb_occurrences": {"$sum": 1}}},
            {"$match": {"nb_occurrences": {"$gt": 1}}},
        ]
        return list(self.products.aggregate(pipeline))

    # ============ LOGS ============

    def log_scraping_run(
        self,
        status: str,
        products_scraped: int,
        images_scraped: int,
        duration_seconds: float,
        errors: list = None,
    ) -> None:
        """Enregistre un log de scraping."""
        self.scraping_logs.insert_one(
            {
                "timestamp": datetime.utcnow(),
                "status": status,
                "products_scraped": products_scraped,
                "images_scraped": images_scraped,
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

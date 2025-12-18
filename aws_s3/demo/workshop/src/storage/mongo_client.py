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
    - quotes : Citations avec texte, auteur, tags
    - authors : Informations détaillées sur les auteurs
    - tags : Statistiques et métadonnées des tags
    - scraping_logs : Historique des exécutions
    """

    def __init__(self):
        self.client = MongoClient(mongo_config.connection_string)
        self.db = self.client[mongo_config.database]
        self.quotes = self.db["quotes"]
        self.authors = self.db["authors"]
        self.tags = self.db["tags"]
        self.scraping_logs = self.db["scraping_logs"]
        self._create_indexes()

    def _create_indexes(self) -> None:
        """Crée les index pour optimiser les requêtes."""
        # Index sur les citations
        self.quotes.create_index([("text", TEXT)])
        self.quotes.create_index([("author", ASCENDING)])
        self.quotes.create_index([("tags", ASCENDING)])
        self.quotes.create_index([("scraped_at", DESCENDING)])
        self.quotes.create_index(
            [("text", ASCENDING), ("author", ASCENDING)], unique=True
        )

        # Index sur les auteurs
        self.authors.create_index([("name", ASCENDING)], unique=True)
        self.authors.create_index([("born_date", ASCENDING)])
        self.authors.create_index([("bio", TEXT)])

        # Index sur les tags
        self.tags.create_index([("name", ASCENDING)], unique=True)
        self.tags.create_index([("count", DESCENDING)])

        logger.info("mongodb_indexes_created")

    # ============ CITATIONS ============

    def insert_quote(self, quote: dict) -> Optional[str]:
        """
        Insère ou met à jour une citation.

        Args:
            quote: {text, author, tags, author_url, ...}

        Returns:
            ID du document ou None
        """
        try:
            quote["scraped_at"] = datetime.utcnow()
            quote["updated_at"] = datetime.utcnow()

            # Upsert basé sur texte + auteur
            result = self.quotes.update_one(
                {"text": quote["text"], "author": quote["author"]},
                {"$set": quote},
                upsert=True,
            )

            if result.upserted_id:
                logger.debug("quote_inserted", author=quote["author"])
                return str(result.upserted_id)

            return "updated"

        except PyMongoError as e:
            logger.error("quote_insert_failed", error=str(e))
            return None

    def bulk_insert_quotes(self, quotes: list[dict]) -> dict:
        """Insère plusieurs citations."""
        results = {"inserted": 0, "updated": 0, "errors": 0}

        for quote in quotes:
            result = self.insert_quote(quote)
            if result == "updated":
                results["updated"] += 1
            elif result:
                results["inserted"] += 1
            else:
                results["errors"] += 1

        return results

    def find_quotes(
        self,
        query: dict = None,
        projection: dict = None,
        sort: list = None,
        limit: int = 100,
        skip: int = 0,
    ) -> list[dict]:
        """Recherche des citations."""
        query = query or {}
        cursor = self.quotes.find(query, projection)

        if sort:
            cursor = cursor.sort(sort)

        return list(cursor.skip(skip).limit(limit))

    def search_quotes(self, text: str, limit: int = 20) -> list[dict]:
        """Recherche full-text dans les citations."""
        return list(
            self.quotes.find(
                {"$text": {"$search": text}}, {"score": {"$meta": "textScore"}}
            )
            .sort([("score", {"$meta": "textScore"})])
            .limit(limit)
        )

    def get_quotes_by_author(self, author: str) -> list[dict]:
        """Récupère toutes les citations d'un auteur."""
        return self.find_quotes({"author": author})

    def get_quotes_by_tag(self, tag: str) -> list[dict]:
        """Récupère toutes les citations avec un tag."""
        return self.find_quotes({"tags": tag})

    def get_quotes_by_tags(
        self, tags: list[str], match_all: bool = False
    ) -> list[dict]:
        """
        Récupère les citations avec plusieurs tags.

        Args:
            tags: Liste de tags
            match_all: True = tous les tags, False = au moins un
        """
        if match_all:
            query = {"tags": {"$all": tags}}
        else:
            query = {"tags": {"$in": tags}}

        return self.find_quotes(query)

    def get_random_quotes(self, count: int = 5) -> list[dict]:
        """Récupère des citations aléatoires."""
        pipeline = [{"$sample": {"size": count}}]
        return list(self.quotes.aggregate(pipeline))

    # ============ AUTEURS ============

    def insert_author(self, author: dict) -> Optional[str]:
        """
        Insère ou met à jour un auteur.

        Args:
            author: {name, bio, born_date, born_location, ...}
        """
        try:
            author["updated_at"] = datetime.utcnow()

            result = self.authors.update_one(
                {"name": author["name"]}, {"$set": author}, upsert=True
            )

            if result.upserted_id:
                logger.debug("author_inserted", name=author["name"])
                return str(result.upserted_id)

            return "updated"

        except PyMongoError as e:
            logger.error("author_insert_failed", error=str(e))
            return None

    def get_author(self, name: str) -> Optional[dict]:
        """Récupère un auteur par son nom."""
        return self.authors.find_one({"name": name})

    def get_all_authors(self) -> list[dict]:
        """Récupère tous les auteurs."""
        return list(self.authors.find())

    def search_authors(self, text: str) -> list[dict]:
        """Recherche dans les biographies."""
        return list(self.authors.find({"$text": {"$search": text}}))

    # ============ TAGS ============

    def update_tag_stats(self) -> None:
        """Met à jour les statistiques des tags."""
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]

        tag_stats = list(self.quotes.aggregate(pipeline))

        for tag in tag_stats:
            self.tags.update_one(
                {"name": tag["_id"]},
                {
                    "$set": {
                        "name": tag["_id"],
                        "count": tag["count"],
                        "updated_at": datetime.utcnow(),
                    }
                },
                upsert=True,
            )

        logger.info("tag_stats_updated", count=len(tag_stats))

    def get_popular_tags(self, limit: int = 20) -> list[dict]:
        """Récupère les tags les plus populaires."""
        return list(self.tags.find().sort("count", DESCENDING).limit(limit))

    def get_all_tags(self) -> list[str]:
        """Liste tous les tags uniques."""
        return self.quotes.distinct("tags")

    # ============ AGRÉGATIONS ============

    def get_stats(self) -> dict:
        """Statistiques globales."""
        return {
            "total_quotes": self.quotes.count_documents({}),
            "total_authors": self.authors.count_documents({}),
            "total_tags": len(self.get_all_tags()),
            "avg_tags_per_quote": self._avg_tags_per_quote(),
        }

    def _avg_tags_per_quote(self) -> float:
        """Calcule le nombre moyen de tags par citation."""
        pipeline = [
            {"$project": {"tag_count": {"$size": "$tags"}}},
            {"$group": {"_id": None, "avg": {"$avg": "$tag_count"}}},
        ]
        result = list(self.quotes.aggregate(pipeline))
        return result[0]["avg"] if result else 0

    def get_quotes_by_author_stats(self) -> list[dict]:
        """Nombre de citations par auteur."""
        pipeline = [
            {
                "$group": {
                    "_id": "$author",
                    "quote_count": {"$sum": 1},
                    "tags": {"$push": "$tags"},
                }
            },
            {"$sort": {"quote_count": -1}},
        ]
        return list(self.quotes.aggregate(pipeline))

    def get_tag_co_occurrence(self) -> list[dict]:
        """
        Analyse la co-occurrence des tags.
        Quels tags apparaissent souvent ensemble ?
        """
        pipeline = [
            {"$unwind": "$tags"},
            {"$group": {"_id": "$_id", "tags": {"$push": "$tags"}}},
            {"$match": {"tags.1": {"$exists": True}}},  # Au moins 2 tags
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "co_tags": {"$push": "$tags"}}},
        ]
        return list(self.quotes.aggregate(pipeline))

    def get_author_tag_analysis(self) -> list[dict]:
        """Analyse des tags préférés par auteur."""
        pipeline = [
            {"$unwind": "$tags"},
            {
                "$group": {
                    "_id": {"author": "$author", "tag": "$tags"},
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
            {
                "$group": {
                    "_id": "$_id.author",
                    "top_tags": {"$push": {"tag": "$_id.tag", "count": "$count"}},
                }
            },
        ]
        return list(self.quotes.aggregate(pipeline))

    def get_quote_length_distribution(self) -> list[dict]:
        """Distribution de la longueur des citations."""
        pipeline = [
            {"$project": {"length": {"$strLenCP": "$text"}, "author": 1}},
            {
                "$bucket": {
                    "groupBy": "$length",
                    "boundaries": [0, 50, 100, 150, 200, 300, 500],
                    "default": "500+",
                    "output": {
                        "count": {"$sum": 1},
                        "authors": {"$addToSet": "$author"},
                    },
                }
            },
        ]
        return list(self.quotes.aggregate(pipeline))

    # ============ LOGS ============

    def log_scraping_run(
        self,
        status: str,
        quotes_scraped: int,
        authors_scraped: int,
        duration_seconds: float,
        errors: list = None,
    ) -> None:
        """Enregistre un log de scraping."""
        self.scraping_logs.insert_one(
            {
                "timestamp": datetime.utcnow(),
                "status": status,
                "quotes_scraped": quotes_scraped,
                "authors_scraped": authors_scraped,
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

    def count_quotes(self, query: dict = None) -> int:
        """Compte les citations."""
        return self.quotes.count_documents(query or {})

    def count_authors(self) -> int:
        """Compte les auteurs."""
        return self.authors.count_documents({})

    def get_all_data(self) -> dict:
        """Exporte toutes les données."""
        quotes = list(self.quotes.find({}, {"_id": 0}))
        authors = list(self.authors.find({}, {"_id": 0}))

        return {
            "quotes": quotes,
            "authors": authors,
            "exported_at": datetime.utcnow().isoformat(),
        }

    def delete_all(self) -> dict:
        """Supprime toutes les données (reset)."""
        quotes_deleted = self.quotes.delete_many({}).deleted_count
        authors_deleted = self.authors.delete_many({}).deleted_count
        tags_deleted = self.tags.delete_many({}).deleted_count

        logger.warning(
            "all_data_deleted",
            quotes=quotes_deleted,
            authors=authors_deleted,
            tags=tags_deleted,
        )

        return {
            "quotes": quotes_deleted,
            "authors": authors_deleted,
            "tags": tags_deleted,
        }

    def close(self) -> None:
        """Ferme la connexion."""
        self.client.close()

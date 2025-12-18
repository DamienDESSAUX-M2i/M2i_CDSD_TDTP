"""Pipeline de données pour les citations."""

from datetime import datetime
from typing import Optional

import pandas as pd
import structlog
from tqdm import tqdm

from src import Author, Quote, QuotesScraper
from src.storage import MinIOStorage, MongoDBStorage

logger = structlog.get_logger()


class QuotesPipeline:
    """
    Pipeline ETL pour les citations.

    Workflow :
    1. Extract : Scraping des citations et auteurs
    2. Transform : Nettoyage et enrichissement
    3. Load : Stockage MongoDB + exports MinIO
    """

    def __init__(self):
        self.scraper = QuotesScraper()
        self.minio = MinIOStorage()
        self.mongodb = MongoDBStorage()
        self.stats = {"quotes_scraped": 0, "authors_scraped": 0, "errors": []}

    def process_quote(self, quote: Quote) -> Optional[dict]:
        """Traite et stocke une citation."""
        try:
            quote_data = quote.to_dict()
            self.mongodb.insert_quote(quote_data)
            self.stats["quotes_scraped"] += 1
            return quote_data
        except Exception as e:
            self.stats["errors"].append(str(e))
            return None

    def process_author(self, author: Author) -> Optional[dict]:
        """Traite et stocke un auteur."""
        try:
            author_data = author.to_dict()
            self.mongodb.insert_author(author_data)
            self.stats["authors_scraped"] += 1
            return author_data
        except Exception as e:
            self.stats["errors"].append(str(e))
            return None

    def run(
        self,
        max_pages: int = 10,
        include_authors: bool = True,
        show_progress: bool = True,
    ) -> dict:
        """
        Exécute le pipeline complet.

        Args:
            max_pages: Nombre max de pages
            include_authors: Scraper les détails des auteurs
            show_progress: Afficher la progression

        Returns:
            Statistiques d'exécution
        """
        start_time = datetime.utcnow()
        logger.info("pipeline_started", max_pages=max_pages)

        try:
            # Scrape complet
            data = self.scraper.scrape_complete(
                max_pages=max_pages, include_authors=include_authors
            )

            # Traiter les citations
            quotes = data["quotes"]
            iterator = (
                tqdm(quotes, desc="Processing quotes") if show_progress else quotes
            )

            for quote in iterator:
                self.process_quote(quote)

            # Traiter les auteurs
            authors = data["authors"]
            if include_authors:
                author_iter = (
                    tqdm(authors, desc="Processing authors")
                    if show_progress
                    else authors
                )
                for author in author_iter:
                    self.process_author(author)

            # Mettre à jour les stats des tags
            self.mongodb.update_tag_stats()

            # Log du run
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.mongodb.log_scraping_run(
                status="success",
                quotes_scraped=self.stats["quotes_scraped"],
                authors_scraped=self.stats["authors_scraped"],
                duration_seconds=duration,
                errors=self.stats["errors"],
            )

        except Exception as e:
            logger.error("pipeline_failed", error=str(e))
            self.mongodb.log_scraping_run(
                status="failed",
                quotes_scraped=self.stats["quotes_scraped"],
                authors_scraped=self.stats["authors_scraped"],
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

    def run_by_tags(self, tags: list[str], max_pages_per_tag: int = 3) -> dict:
        """
        Scrape par tags spécifiques.

        Args:
            tags: Liste de tags à scraper
            max_pages_per_tag: Pages max par tag

        Returns:
            Statistiques
        """
        start_time = datetime.utcnow()

        for tag in tags:
            logger.info("scraping_tag", tag=tag)

            for quote in self.scraper.scrape_by_tag(tag, max_pages_per_tag):
                self.process_quote(quote)

        self.mongodb.update_tag_stats()

        self.stats["duration_seconds"] = (
            datetime.utcnow() - start_time
        ).total_seconds()
        return self.stats

    def export_csv(self, filepath: str = None) -> Optional[str]:
        """
        Exporte les citations en CSV.

        Args:
            filepath: Chemin local (optionnel)

        Returns:
            URI MinIO
        """
        quotes = self.mongodb.find_quotes(limit=10000)

        if not quotes:
            return None

        # Convertir en DataFrame
        df = pd.DataFrame(quotes)

        # Nettoyer
        if "_id" in df.columns:
            df["_id"] = df["_id"].astype(str)

        # Convertir les tags en string
        if "tags" in df.columns:
            df["tags"] = df["tags"].apply(lambda x: ", ".join(x) if x else "")

        # Sauvegarder localement
        if filepath:
            df.to_csv(filepath, index=False)

        # Upload vers MinIO
        csv_content = df.to_csv(index=False)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        return self.minio.upload_csv(csv_content, f"quotes_export_{timestamp}.csv")

    def export_json(self) -> Optional[str]:
        """Exporte toutes les données en JSON."""
        data = self.mongodb.get_all_data()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        return self.minio.upload_json(data, f"full_export_{timestamp}.json")

    def create_backup(self) -> Optional[str]:
        """Crée une sauvegarde complète."""
        data = self.mongodb.get_all_data()
        return self.minio.create_backup(data, "quotes_backup")

    def get_analytics(self) -> dict:
        """Génère un rapport d'analytics."""
        return {
            "overview": self.mongodb.get_stats(),
            "by_author": self.mongodb.get_quotes_by_author_stats(),
            "popular_tags": self.mongodb.get_popular_tags(20),
            "quote_lengths": self.mongodb.get_quote_length_distribution(),
            "author_tags": self.mongodb.get_author_tag_analysis(),
            "storage": self.minio.get_storage_stats(),
            "scraping_history": self.mongodb.get_scraping_history(5),
        }

    def close(self) -> None:
        """Ferme les connexions."""
        self.scraper.close()
        self.mongodb.close()


def main():
    """Point d'entrée CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="Quotes Scraping Pipeline")
    parser.add_argument("--pages", type=int, default=5, help="Max pages to scrape")
    parser.add_argument("--no-authors", action="store_true", help="Skip author details")
    parser.add_argument("--tags", nargs="+", help="Specific tags to scrape")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON")
    parser.add_argument("--backup", action="store_true", help="Create backup")

    args = parser.parse_args()

    pipeline = QuotesPipeline()

    try:
        # Exécuter le scraping
        if args.tags:
            stats = pipeline.run_by_tags(args.tags)
        else:
            stats = pipeline.run(
                max_pages=args.pages, include_authors=not args.no_authors
            )

        # Afficher les résultats
        print("\n" + "=" * 50)
        print("PIPELINE COMPLETED")
        print("=" * 50)
        print(f"Quotes scraped: {stats['quotes_scraped']}")
        print(f"Authors scraped: {stats['authors_scraped']}")
        print(f"Duration: {stats['duration_seconds']:.2f}s")
        print(f"Errors: {len(stats['errors'])}")

        # Exports
        if args.export_csv:
            ref = pipeline.export_csv()
            print(f"\nCSV exported: {ref}")

        if args.export_json:
            ref = pipeline.export_json()
            print(f"JSON exported: {ref}")

        if args.backup:
            ref = pipeline.create_backup()
            print(f"Backup created: {ref}")

        # Analytics
        analytics = pipeline.get_analytics()
        print("\n" + "=" * 50)
        print("ANALYTICS")
        print("=" * 50)

        overview = analytics.get("overview", {})
        print(f"Total quotes: {overview.get('total_quotes', 0)}")
        print(f"Total authors: {overview.get('total_authors', 0)}")
        print(f"Total tags: {overview.get('total_tags', 0)}")

        print("\nTop 5 tags:")
        for tag in analytics.get("popular_tags", [])[:5]:
            print(f"  - {tag['name']}: {tag['count']} quotes")

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()

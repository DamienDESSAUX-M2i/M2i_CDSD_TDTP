import argparse

from src import ProductsPipeline


def main():
    """Point d'entrée CLI."""

    parser = argparse.ArgumentParser(description="Products Scraping Pipeline")
    parser.add_argument("--pages", type=int, default=5, help="Max pages to scrape")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON")
    parser.add_argument("--backup", action="store_true", help="Create backup")

    args = parser.parse_args()

    pipeline = ProductsPipeline()

    try:
        # Exécuter le scraping
        stats = pipeline.run(max_pages=args.pages)

        # Afficher les résultats
        print("\n" + "=" * 50)
        print("PIPELINE COMPLETED")
        print("=" * 50)
        print(f"Products scraped: {stats['products_scraped']}")
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
        print(f"Total products: {overview.get('total_products', 0)}")

    finally:
        pipeline.close()


if __name__ == "__main__":
    main()

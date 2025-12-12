import json
import re
from pathlib import Path

import pandas as pd
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class JsonWriterPipeline:
    def open_spider(self, spider):
        output_dir_path = Path("output")
        if not output_dir_path.exists():
            output_dir_path.mkdir()
        json_path = output_dir_path / "books.json"
        self.file = open(json_path, "w", encoding="utf-8")
        self.items = []

    def close_spider(self, spider):
        json.dump(self.items, self.file, indent=4, ensure_ascii=False)
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item


class ExcelWriterPipeline:
    def open_spider(self, spider):
        output_dir_path = Path("output")
        if not output_dir_path.exists():
            output_dir_path.mkdir()
        excel_path = output_dir_path / "books.xlsx"
        self.writer = pd.ExcelWriter(excel_path, engine="openpyxl")
        self.items = []

    def close_spider(self, spider):
        df_books = pd.DataFrame(self.items)
        df_categories = (
            df_books.groupby("category", as_index=False)
            .agg(
                nb_books=("title", "count"),
                avg_price=("price", "mean"),
                avg_rating=("rating", "mean"),
            )
            .sort_values(by="category", ascending=True)
        )
        df_books.to_excel(self.writer, sheet_name="Books", index=False)
        df_categories.to_excel(self.writer, sheet_name="Categories", index=False)
        self.writer.close()

    def process_item(self, item, spider):
        self.items.append(ItemAdapter(item).asdict())
        return item


class CategoryConversionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("category"):
            adapter["category"] = adapter["category"].replace("\n", " ").strip()
            return item


class PriceConversionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("price"):
            adapter["price"] = float(re.findall(r"[\d.]+", adapter["price"])[0])
            return item


class AvailabilityConversionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("availability"):
            adapter["availability"] = "in stock" in adapter["availability"].lower()
            return item


class RatingConversionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("rating"):
            map_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            adapter["rating"] = map_rating.get(adapter["rating"].split()[1])
            return item


class NbReviewsConversionPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("nb_reviews"):
            adapter["nb_reviews"] = int(adapter["nb_reviews"])
            return item


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] in self.ids_seen:
            raise DropItem(f"Duplicate: {item}")
        else:
            self.ids_seen.add(adapter["title"])
            return item

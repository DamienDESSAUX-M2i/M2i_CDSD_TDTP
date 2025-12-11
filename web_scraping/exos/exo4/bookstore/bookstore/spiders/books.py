import re

import scrapy

from bookstore.items import BookItem

map_rating = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        "DEPTH_LIMIT": 2,
        "FEED_EXPORT_FIELDS": ["title", "price", "rating", "availability"],
        "FEEDS": {
            "outputs/books.jsonl": {
                "format": "jsonlines",
                "encoding": "utf8",
                "overwrite": True,
            },
            "outputs/books.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
                "indent": 4,
            },
            "outputs/books.csv": {
                "format": "csv",
                "encoding": "utf8",
                "overwrite": True,
            },
        },
    }

    def parse(self, response):
        for article in response.css("article.product_pod"):
            item = BookItem()
            item["title"] = article.css("h3 a::attr(title)").get()
            item["price"] = re.findall(
                r"[\d.]+", article.css("p.price_color::text").get()
            )[0]
            item["rating"] = map_rating.get(
                article.css("p.star-rating::attr(class)").get().split()[1], None
            )
            item["availability"] = (
                "in stock"
                in "".join(article.css("p.instock.availability::text").getall()).lower()
            )
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

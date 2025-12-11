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
    }

    def parse(self, response):
        for article in response.css("article.product_pod"):
            item = BookItem()
            item["title"] = article.css("h3 a::attr(title)").get()
            item["price"] = re.findall(
                r"[\d.]+", article.css("p.price_color::text").get()
            )
            item["rating"] = map_rating.get(
                article.css("p.star-rating::attr(class)").get().split()[1], None
            )
            item["availability"] = any(
                [
                    "in stock" in text.lower()
                    for text in article.css("p.instock.availability::text").getall()
                ]
            )
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

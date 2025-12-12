import scrapy

from e_commerce.items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        "DEPTH_LIMIT": 3,
        "CLOSESPIDER_PAGECOUNT": 20,
        "FEEDS": {
            "outputs/books.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
                "indent": 4,
            },
        },
    }

    def parse(self, response):
        categories = response.css("ul.nav.nav-list li ul li")
        for category in categories:
            category_text = category.css("a::text").get()
            item = BookItem()
            item["category"] = category_text

            category_url = category.css("a::attr(href)").get()
            next_url = response.urljoin(category_url)
            if next_url:
                yield scrapy.Request(
                    next_url, callback=self.parse_book_urls, meta={"item": item}
                )

    def parse_book_urls(self, response):
        item = response.meta["item"]
        articles = response.css("article.product_pod")
        for article in articles:
            book_url = response.urljoin(
                article.css("div.image_container a::attr(href)").get()
            )
            item["url"] = book_url

            if book_url:
                yield scrapy.Request(
                    book_url, callback=self.parse_book_infos, meta={"item": item}
                )

        next_page = response.urljoin(response.css("li.next a::attr(href)").get())
        if next_page:
            yield scrapy.Request(
                next_page, callback=self.parse_book_urls, meta={"item": item}
            )

    def parse_book_infos(self, response):
        item = response.meta["item"]
        div_row = response.css("article.product_page div.row")
        if div_row:
            div_row = div_row[0]
            item["title"] = div_row.css("h1::text").get()
            item["price"] = div_row.css("p.price_color::text").get()
            item["availability"] = div_row.css("p.instock.availability::text").getall()[
                1
            ]
            item["rating"] = div_row.css("p.star-rating::attr(class)").get()
            item["image_url"] = response.urljoin(
                div_row.css("div.item.active img::attr(src)").get()
            )
        item["description"] = response.css("#product_description + p::text").get()
        table = response.css("article table")
        if table:
            table = table[0]
            table_rows = table.css("tr")
            if table_rows:
                table_row = table_rows[-1]
                item["nb_reviews"] = table_row.css("td::text").get()

        yield item

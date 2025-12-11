import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        categories = response.css("ul.nav.nav-list li ul li")
        for category in categories:
            category_text = category.css("a::text").get()
            yield {"category_text": category_text}

            category_url = category.css("a::attr(href)").get()
            next_url = response.urljoin(category_url)
            if next_url:
                yield response.follow(next_url, callback=self.parse_book_urls)

    def parse_book_urls(self, response):
        articles = response.css("article.product_pod")
        for article in articles:
            book_url = article.css("div.image_container a::attr(href)").get()
            yield {"book_url": book_url}

        next_url = response.urljoin(book_url)
        if next_url:
            yield response.follow(next_url, callback=self.parse_book_infos)

    def parse_book_infos(self, reponse):
        pass

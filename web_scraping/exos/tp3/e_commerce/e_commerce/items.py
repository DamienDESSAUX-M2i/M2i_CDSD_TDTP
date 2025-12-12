import scrapy


class BookItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    nb_reviews = scrapy.Field()
    availability = scrapy.Field()

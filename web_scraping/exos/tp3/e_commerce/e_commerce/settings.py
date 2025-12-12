SPIDER_MODULES = ["e_commerce.spiders"]
NEWSPIDER_MODULE = "e_commerce.spiders"

ADDONS = {}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
)
BOT_NAME = "e_commerce"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 0.5

FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "e_commerce.pipelines.CategoryConversionPipeline": 101,
    "e_commerce.pipelines.PriceConversionPipeline": 102,
    "e_commerce.pipelines.AvailabilityConversionPipeline": 103,
    "e_commerce.pipelines.RatingConversionPipeline": 104,
    "e_commerce.pipelines.NbReviewsConversionPipeline": 105,
    "e_commerce.pipelines.DuplicatesPipeline": 200,
    "e_commerce.pipelines.JsonWriterPipeline": 301,
    "e_commerce.pipelines.ExcelWriterPipeline": 302,
}

DOWNLOADER_MIDDLEWARES = {"e_commerce.middlewares.RandomUserAgentMiddleware": 100}

LOG_LEVEL = "INFO"
LOG_FILE = "e_commerce.log"

# DEPTH_LIMIT = 2
# CLOSESPIDER_PAGECOUNT = 20

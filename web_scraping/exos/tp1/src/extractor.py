import logging
import time

import requests


class WebScrapingExtractor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def fetch_page(self, session: requests.Session, url: str) -> requests.Response:
        try:
            self.logger.info(f"Fetch page - url : {url}")
            response = session.get(url=url)
            self.logger.info("\tSuccess")
            return response
        except Exception as e:
            self.logger.error(f"Fetch page - error : {e}")
            raise

    def fetch_pages(
        self, base_url: str, headers: dict[str, str], nb_pages: int
    ) -> list[requests.Response]:
        try:
            pages: list[requests.Response] = []
            with requests.Session() as session:
                session.headers.update(headers)

                for k in range(1, nb_pages + 1):
                    url = "/".join([base_url, f"page/{k}/"])
                    pages.append(self.fetch_page(session=session, url=url))
                    time.sleep(1)
            return pages
        except Exception as e:
            self.logger.error(f"Fetch pages - error : {e}")
            raise

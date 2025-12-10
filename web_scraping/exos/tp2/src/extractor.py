import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


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

    def _get_link_next(self, page: requests.Response) -> str:
        try:
            self.logger.info("Attempting to get the link to the next page.")
            soup = BeautifulSoup(page.text, "lxml")
            href = soup.select(".next > a")[0].get("href")
            self.logger.info("\tSuccess")
            return href
        except Exception as e:
            self.logger.error(f"No link find error : {e}.")

    def fetch_pages_auto(
        self, base_url: str, headers: dict[str, str], max_pages: int
    ) -> list[requests.Response]:
        try:
            pages: list[requests.Response] = []
            with requests.Session() as session:
                session.headers.update(headers)

                nb_pages = 1
                url = base_url
                while True:
                    page = self.fetch_page(session=session, url=url)
                    pages.append(page)
                    if nb_pages == max_pages:
                        break
                    href = self._get_link_next(page)
                    url = urljoin(base_url, href)
                    time.sleep(1)
                    nb_pages += 1

            return pages
        except Exception as e:
            self.logger.error(f"Fetch pages - error : {e}")
            raise

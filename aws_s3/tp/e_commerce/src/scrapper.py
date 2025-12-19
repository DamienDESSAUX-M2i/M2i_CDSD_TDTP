import re
import time
from dataclasses import dataclass
from typing import Generator, Optional
from urllib.parse import urljoin

import requests
import structlog
from bs4 import BeautifulSoup
from config.settings import scraper_config
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()


@dataclass
class Product:
    """Représentation d'une citation."""

    category: str
    sub_category: str
    title: str
    price: float | int
    description: str
    rating: int
    image_url: str
    details_url: str

    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour MongoDB."""
        return {
            "category": self.category,
            "sub_category": self.sub_category,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "rating": self.rating,
            "image_url": self.image_url,
            "details_url": self.details_url,
        }


## Class de Scrapping


class ProductsScraper:
    """
    Scraper pour le site Quotes to Scrape.

    Fonctionnalités :
    - Scraping des citations avec pagination
    - Extraction des détails des auteurs
    - Navigation par tags
    """

    def __init__(self):
        self.base_urls = scraper_config.base_urls
        self.base_url = None
        self.delay = scraper_config.delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()

    def _setup_session(self) -> None:
        """Configure la session HTTP."""
        self.session.headers.update(
            {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page.

        Args:
            url: URL à récupérer

        Returns:
            BeautifulSoup ou None
        """
        try:
            logger.debug("fetching", url=url)
            response = self.session.get(url, timeout=scraper_config.timeout)
            response.raise_for_status()

            # Politesse
            time.sleep(self.delay)

            return BeautifulSoup(response.content, "lxml")

        except requests.RequestException as e:
            logger.error("fetch_failed", url=url, error=str(e))
            raise

    def _clean_price(self, text: str) -> str:
        """Nettoie le texte d'une description."""
        try:
            price = float(re.findall(r"[\d.]+", text)[0])
            return price
        except Exception as e:
            logger.error("clean_price failled", error=str(e))
            return None

    def _clean_rating(self, text: str) -> str:
        """Nettoie le texte d'une description."""
        try:
            rating = int(text)
            return rating
        except Exception as e:
            logger.error("clean_rating failled", error=str(e))
            return None

    def scrape_products_page(self, url: str) -> list[Product]:
        """
        Scrape une page de produits.

        Args:
            url: URL de la page

        Returns:
            Liste de produits
        """
        soup = self._fetch(url)
        if not soup:
            return []

        products = []
        product_divs = soup.find_all("div", class_="product-wrapper")

        for div in product_divs:
            product = self._parse_product(div)
            if product:
                products.append(product)

        return products

    def _parse_product(self, element) -> Optional[Product]:
        """
        Parse un élément de produit.

        Args:
            element: Élément BeautifulSoup

        Returns:
            Objet Product ou None
        """
        try:
            # Categorie du produit
            category = self.base_url.split("/")[-2]

            # Sous Categorie du produit
            sub_category = self.base_url.split("/")[-1]

            # Titre du produit
            title_elem = element.find("a", class_="title")
            title = title_elem["title"] if title_elem else "Unknown"

            # Prix du produit
            price_elem = element.find("h4", class_="price").find("span")
            price = self._clean_price(price_elem.text) if price_elem else ""

            # Description du produit
            text_elem = element.find("p", class_="description")
            description = text_elem.text if text_elem else ""

            # Avis du produit
            rating_elem = element.select("p.review-count + p")[0]
            rating = (
                self._clean_rating(rating_elem.get("data-rating"))
                if rating_elem
                else ""
            )

            # Image URL du produit
            image_link = element.find("img")
            image_url = urljoin(self.base_url, image_link["src"]) if image_link else ""

            # Détails URL du produit
            details_link = element.find("a", class_="title")
            details_url = (
                urljoin(self.base_url, details_link["href"]) if details_link else ""
            )

            return Product(
                category=category,
                sub_category=sub_category,
                title=title,
                price=price,
                description=description,
                rating=rating,
                image_url=image_url,
                details_url=details_url,
            )

        except Exception as e:
            logger.error("product_parse_failed", error=str(e))
            return None

    def scrape_all_products(
        self, max_pages: int = None
    ) -> Generator[Product, None, None]:
        """
        Scrape tous les produits avec pagination.

        Args:
            max_pages: Limite de pages (None = toutes)

        Yields:
            Objets Product
        """
        max_pages = max_pages or scraper_config.max_pages

        for base_url in self.base_urls:
            self.base_url = base_url
            page = 1
            url = self.base_url

            while url and page <= max_pages:
                logger.info("scraping_page", page=page)

                soup = self._fetch(url)
                if not soup:
                    break

                # Parser les produits de la page
                product_divs = soup.find_all("div", class_="product-wrapper")

                for div in product_divs:
                    product = self._parse_product(div)
                    if product:
                        yield product

                # Page suivante
                url = self._get_next_page(soup)
                page += 1

    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Trouve l'URL de la page suivante."""
        next_link = soup.find("a", class_="next")

        if next_link:
            return urljoin(self.base_url, next_link["href"])

        return None

    def scrape_complete(self, max_pages: int = None) -> dict:
        """
        Scrape complet : citations + auteurs.

        Args:
            max_pages: Limite de pages

        Returns:
            {products: [...]}
        """
        products = []

        for product in self.scrape_all_products(max_pages):
            products.append(product)

        return {"products": products}

    def close(self) -> None:
        """Ferme la session."""
        self.session.close()

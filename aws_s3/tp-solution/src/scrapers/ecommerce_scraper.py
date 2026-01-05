"""
Scraper pour webscraper.io/test-sites/e-commerce.

Ce module implémente un scraper robuste pour collecter les données
du site de démonstration e-commerce de webscraper.io.

Site cible : https://webscraper.io/test-sites/e-commerce/allinone

⚠️ Ce site est EXPLICITEMENT conçu pour l'apprentissage du scraping.
   Il est légal et encouragé de le scraper à des fins éducatives.

Fonctionnalités :
- Scraping des produits (laptops, tablets, phones)
- Gestion de la pagination
- Téléchargement des images
- Retry automatique en cas d'erreur
- Délai entre requêtes (politesse)
"""

import hashlib
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Generator, Optional
from urllib.parse import urljoin

import requests
import structlog
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import scraper_config

logger = structlog.get_logger()


@dataclass
class Product:
    """
    Représentation d'un produit e-commerce.

    Attributes:
        title: Nom du produit
        price: Prix en dollars
        description: Description courte
        rating: Note (1-5 étoiles)
        reviews_count: Nombre d'avis
        image_url: URL de l'image
        product_url: URL de la page produit
        category: Catégorie (computers, phones)
        subcategory: Sous-catégorie (laptops, tablets, touch)
        specs: Spécifications techniques (optionnel)
        image_data: Données binaires de l'image (optionnel)
    """

    title: str
    price: float
    description: str
    rating: int
    reviews_count: int
    image_url: str
    product_url: str
    category: str = ""
    subcategory: str = ""
    specs: dict = field(default_factory=dict)
    image_data: bytes = field(default=None, repr=False)

    @property
    def sku(self) -> str:
        """
        Génère un SKU unique basé sur le titre.

        Le SKU est un hash MD5 tronqué pour être plus lisible.
        """
        return hashlib.md5(self.title.encode()).hexdigest()[:12].upper()

    def to_dict(self) -> dict:
        """
        Convertit le produit en dictionnaire pour MongoDB.

        Exclut image_data car c'est stocké dans MinIO.
        """
        return {
            "sku": self.sku,
            "title": self.title,
            "price": self.price,
            "description": self.description,
            "rating": self.rating,
            "reviews_count": self.reviews_count,
            "image_url": self.image_url,
            "product_url": self.product_url,
            "category": self.category,
            "subcategory": self.subcategory,
            "specs": self.specs,
        }


class EcommerceScraper:
    """
    Scraper pour le site e-commerce de test.

    Ce scraper collecte les données de produits depuis :
    - /computers/laptops
    - /computers/tablets
    - /phones/touch

    Attributes:
        base_url: URL de base du site
        delay: Délai entre requêtes (secondes)
        session: Session HTTP réutilisable

    Example:
        >>> scraper = EcommerceScraper()
        >>> for product in scraper.scrape_all():
        ...     print(product.title, product.price)
        >>> scraper.close()
    """

    # Mapping des catégories disponibles
    CATEGORIES = {
        "computers": {"laptops": "/computers/laptops", "tablets": "/computers/tablets"},
        "phones": {"touch": "/phones/touch"},
    }

    def __init__(self):
        """Initialise le scraper avec une session HTTP configurée."""
        self.base_url = scraper_config.base_url
        self.delay = scraper_config.delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()

    def _setup_session(self) -> None:
        """
        Configure la session HTTP avec des headers réalistes.

        Utilise un User-Agent aléatoire pour éviter le blocage.
        """
        self.session.headers.update(
            {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0",
            }
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page HTML.

        Inclut :
        - Retry automatique (3 tentatives avec backoff exponentiel)
        - Délai de politesse entre requêtes
        - Logging structuré

        Args:
            url: URL à récupérer

        Returns:
            BeautifulSoup ou None en cas d'erreur

        Raises:
            requests.RequestException: En cas d'erreur HTTP après 3 tentatives
        """
        try:
            logger.debug("fetching_url", url=url)

            response = self.session.get(url, timeout=scraper_config.timeout)
            response.raise_for_status()

            # Délai de politesse
            time.sleep(self.delay)

            return BeautifulSoup(response.content, "lxml")

        except requests.RequestException as e:
            logger.error("fetch_failed", url=url, error=str(e))
            raise

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5)
    )
    def _fetch_image(self, url: str) -> Optional[bytes]:
        """
        Télécharge une image.

        Args:
            url: URL de l'image

        Returns:
            Contenu binaire ou None
        """
        try:
            response = self.session.get(url, timeout=scraper_config.timeout)
            response.raise_for_status()
            time.sleep(self.delay / 2)  # Délai réduit pour les images
            return response.content
        except requests.RequestException as e:
            logger.error("image_fetch_failed", url=url, error=str(e))
            return None

    def _parse_price(self, text: str) -> float:
        """
        Extrait le prix d'une chaîne de texte.

        Gère les formats : $999.99, $1,299.00, etc.

        Args:
            text: Texte contenant le prix

        Returns:
            Prix en float ou 0.0 si non trouvé
        """
        # Supprimer les virgules et extraire les chiffres
        text = text.replace(",", "")
        match = re.search(r"[\d.]+", text)
        return float(match.group()) if match else 0.0

    def _parse_rating(self, element) -> int:
        """
        Extrait le rating d'un élément HTML.

        Le site utilise data-rating ou des étoiles visuelles.

        Args:
            element: Élément BeautifulSoup contenant le rating

        Returns:
            Rating de 0 à 5
        """
        if not element:
            return 0

        # Méthode 1 : attribut data-rating
        rating_attr = element.get("data-rating")
        if rating_attr:
            try:
                return int(rating_attr)
            except ValueError:
                pass

        # Méthode 2 : compter les étoiles
        stars = element.find_all("span", class_="ws-icon-star")
        return len(stars)

    def _parse_reviews(self, text: str) -> int:
        """
        Extrait le nombre d'avis.

        Args:
            text: Texte contenant le nombre d'avis

        Returns:
            Nombre d'avis ou 0
        """
        if not text:
            return 0
        match = re.search(r"(\d+)\s*review", text.lower())
        return int(match.group(1)) if match else 0

    def get_all_category_urls(self) -> list[tuple[str, str, str]]:
        """
        Retourne toutes les URLs de catégories à scraper.

        Returns:
            Liste de tuples (category, subcategory, url)
        """
        urls = []
        for category, subcats in self.CATEGORIES.items():
            for subcategory, path in subcats.items():
                full_url = self.base_url + path
                urls.append((category, subcategory, full_url))
        return urls

    def scrape_category(
        self, url: str, category: str = "", subcategory: str = "", max_pages: int = None
    ) -> Generator[Product, None, None]:
        """
        Scrape tous les produits d'une catégorie avec pagination.

        Args:
            url: URL de la catégorie
            category: Nom de la catégorie
            subcategory: Nom de la sous-catégorie
            max_pages: Limite de pages (None = toutes)

        Yields:
            Objets Product

        Example:
            >>> for product in scraper.scrape_category(
            ...     "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
            ...     category="computers",
            ...     subcategory="laptops"
            ... ):
            ...     print(product.title)
        """
        max_pages = max_pages or scraper_config.max_pages
        page = 1
        current_url = url

        while current_url and page <= max_pages:
            logger.info(
                "scraping_page", category=subcategory, page=page, url=current_url
            )

            try:
                soup = self._fetch(current_url)
                if not soup:
                    break

                # Parser les produits de la page
                products = soup.find_all("div", class_="thumbnail")

                if not products:
                    logger.warning("no_products_found", url=current_url)
                    break

                for product_elem in products:
                    product = self._parse_product(product_elem, category, subcategory)
                    if product:
                        yield product

                # Trouver la page suivante
                current_url = self._get_next_page(soup, url)
                page += 1

            except Exception as e:
                logger.error(
                    "category_scraping_failed",
                    category=subcategory,
                    page=page,
                    error=str(e),
                )
                break

    def _parse_product(
        self, element, category: str, subcategory: str
    ) -> Optional[Product]:
        """
        Parse un élément HTML de produit.

        Structure attendue :
        <div class="thumbnail">
            <img class="img-responsive" src="...">
            <div class="caption">
                <h4 class="price">$999.99</h4>
                <a class="title" title="Product Name" href="...">...</a>
                <p class="description">...</p>
            </div>
            <div class="ratings">
                <p data-rating="4">...</p>
            </div>
        </div>

        Args:
            element: Élément BeautifulSoup du produit
            category: Catégorie parente
            subcategory: Sous-catégorie

        Returns:
            Objet Product ou None si parsing échoue
        """
        try:
            # Titre et URL
            title_elem = element.find("a", class_="title")
            if not title_elem:
                return None

            title = title_elem.get("title", title_elem.text.strip())
            product_url = ""
            if title_elem.get("href"):
                product_url = urljoin(self.base_url, title_elem["href"])

            # Prix
            price_elem = element.find("h4", class_="price")
            price = self._parse_price(price_elem.text) if price_elem else 0.0

            # Description
            desc_elem = element.find("p", class_="description")
            description = desc_elem.text.strip() if desc_elem else ""

            # Rating
            ratings_div = element.find("div", class_="ratings")
            rating = 0
            reviews = 0

            if ratings_div:
                # Chercher l'élément avec data-rating
                rating_elem = ratings_div.find("p", attrs={"data-rating": True})
                if rating_elem:
                    rating = self._parse_rating(rating_elem)

                # Chercher le nombre de reviews
                review_elem = ratings_div.find("p", class_="review-count")
                if review_elem:
                    reviews = self._parse_reviews(review_elem.text)

            # Image
            img_elem = element.find("img", class_="img-responsive")
            image_url = ""
            if img_elem and img_elem.get("src"):
                image_url = urljoin("https://webscraper.io", img_elem["src"])

            return Product(
                title=title,
                price=price,
                description=description,
                rating=rating,
                reviews_count=reviews,
                image_url=image_url,
                product_url=product_url,
                category=category,
                subcategory=subcategory,
            )

        except Exception as e:
            logger.error("product_parse_failed", error=str(e))
            return None

    def _get_next_page(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """
        Trouve l'URL de la page suivante.

        Cherche un lien de pagination "next" ou "»".

        Args:
            soup: Page actuelle parsée
            base_url: URL de base de la catégorie

        Returns:
            URL de la page suivante ou None
        """
        # Chercher la pagination
        pagination = soup.find("ul", class_="pagination")

        if not pagination:
            return None

        # Chercher le lien "next" ou "»"
        next_link = pagination.find("a", string=re.compile(r"»|next|›", re.I))

        if next_link and next_link.get("href"):
            href = next_link["href"]
            # Construire l'URL complète
            if href.startswith("/"):
                return urljoin("https://webscraper.io", href)
            else:
                return urljoin(base_url, href)

        # Alternative : chercher la page active et prendre la suivante
        active = pagination.find("li", class_="active")
        if active:
            next_li = active.find_next_sibling("li")
            if next_li and "disabled" not in next_li.get("class", []):
                link = next_li.find("a")
                if link and link.get("href"):
                    href = link["href"]
                    if href.startswith("/"):
                        return urljoin("https://webscraper.io", href)
                    return urljoin(base_url, href)

        return None

    def scrape_all(
        self, max_pages_per_category: int = None
    ) -> Generator[Product, None, None]:
        """
        Scrape toutes les catégories.

        Args:
            max_pages_per_category: Limite de pages par catégorie

        Yields:
            Objets Product de toutes les catégories

        Example:
            >>> scraper = EcommerceScraper()
            >>> products = list(scraper.scrape_all(max_pages_per_category=2))
            >>> print(f"Total: {len(products)} produits")
        """
        for category, subcategory, url in self.get_all_category_urls():
            logger.info("starting_category", category=category, subcategory=subcategory)

            for product in self.scrape_category(
                url=url,
                category=category,
                subcategory=subcategory,
                max_pages=max_pages_per_category,
            ):
                yield product

    def download_image(self, product: Product) -> Product:
        """
        Télécharge l'image d'un produit.

        Args:
            product: Produit avec image_url

        Returns:
            Produit avec image_data rempli
        """
        if product.image_url:
            product.image_data = self._fetch_image(product.image_url)
            if product.image_data:
                logger.debug(
                    "image_downloaded",
                    title=product.title,
                    size_kb=len(product.image_data) // 1024,
                )
        return product

    def close(self) -> None:
        """Ferme la session HTTP."""
        self.session.close()
        logger.info("scraper_session_closed")


# Test du module
if __name__ == "__main__":
    print("Test du scraper e-commerce...")

    scraper = EcommerceScraper()

    # Test sur une seule page
    products = []
    for product in scraper.scrape_category(
        url="https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops",
        category="computers",
        subcategory="laptops",
        max_pages=1,
    ):
        products.append(product)
        print(f"- {product.title}: ${product.price} ({product.rating}★)")

    print(f"\nTotal: {len(products)} produits scrapés")

    scraper.close()
    print("Test terminé!")

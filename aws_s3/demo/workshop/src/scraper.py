import re
import time
from dataclasses import dataclass, field
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
class Quote:
    """Représentation d'une citation."""

    text: str
    author: str
    author_url: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour MongoDB."""
        return {
            "text": self.text,
            "author": self.author,
            "author_url": self.author_url,
            "tags": self.tags,
        }


@dataclass
class Author:
    """Représentation d'un auteur."""

    name: str
    bio: str = ""
    born_date: str = ""
    born_location: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        """Convertit en dictionnaire pour MongoDB."""
        return {
            "name": self.name,
            "bio": self.bio,
            "born_date": self.born_date,
            "born_location": self.born_location,
            "url": self.url,
        }


## Class de Scrapping


class QuotesScraper:
    """
    Scraper pour le site Quotes to Scrape.

    Fonctionnalités :
    - Scraping des citations avec pagination
    - Extraction des détails des auteurs
    - Navigation par tags
    """

    def __init__(self):
        self.base_url = scraper_config.base_url
        self.delay = scraper_config.delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()

        # Cache pour éviter de re-scraper les auteurs
        self.authors_cache: dict[str, Author] = {}

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

    def _clean_text(self, text: str) -> str:
        """Nettoie le texte d'une citation."""
        # Supprimer les guillemets décoratifs
        text = text.strip()
        text = re.sub(r'^[""\u201c\u201d]+|[""\u201c\u201d]+$', "", text)
        return text.strip()

    def scrape_quotes_page(self, url: str) -> list[Quote]:
        """
        Scrape une page de citations.

        Args:
            url: URL de la page

        Returns:
            Liste de citations
        """
        soup = self._fetch(url)
        if not soup:
            return []

        quotes = []
        quote_divs = soup.find_all("div", class_="quote")

        for div in quote_divs:
            quote = self._parse_quote(div)
            if quote:
                quotes.append(quote)

        return quotes

    def _parse_quote(self, element) -> Optional[Quote]:
        """
        Parse un élément de citation.

        Args:
            element: Élément BeautifulSoup

        Returns:
            Objet Quote ou None
        """
        try:
            # Texte de la citation
            text_elem = element.find("span", class_="text")
            text = self._clean_text(text_elem.text) if text_elem else ""

            # Auteur
            author_elem = element.find("small", class_="author")
            author = author_elem.text.strip() if author_elem else "Unknown"

            # URL de l'auteur
            author_link = element.find("a", href=True)
            author_url = ""
            if author_link and "/author/" in author_link["href"]:
                author_url = urljoin(self.base_url, author_link["href"])

            # Tags
            tags = []
            tags_div = element.find("div", class_="tags")
            if tags_div:
                tag_links = tags_div.find_all("a", class_="tag")
                tags = [tag.text.strip() for tag in tag_links]

            return Quote(text=text, author=author, author_url=author_url, tags=tags)

        except Exception as e:
            logger.error("quote_parse_failed", error=str(e))
            return None

    def scrape_all_quotes(self, max_pages: int = None) -> Generator[Quote, None, None]:
        """
        Scrape toutes les citations avec pagination.

        Args:
            max_pages: Limite de pages (None = toutes)

        Yields:
            Objets Quote
        """
        max_pages = max_pages or scraper_config.max_pages
        page = 1
        url = self.base_url

        while url and page <= max_pages:
            logger.info("scraping_page", page=page)

            soup = self._fetch(url)
            if not soup:
                break

            # Parser les citations de la page
            quote_divs = soup.find_all("div", class_="quote")

            for div in quote_divs:
                quote = self._parse_quote(div)
                if quote:
                    yield quote

            # Page suivante
            url = self._get_next_page(soup)
            page += 1

    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Trouve l'URL de la page suivante."""
        next_li = soup.find("li", class_="next")

        if next_li:
            next_link = next_li.find("a", href=True)
            if next_link:
                return urljoin(self.base_url, next_link["href"])

        return None

    def scrape_author(self, url: str) -> Optional[Author]:
        """
        Scrape les détails d'un auteur.

        Args:
            url: URL de la page auteur

        Returns:
            Objet Author ou None
        """
        # Vérifier le cache
        if url in self.authors_cache:
            return self.authors_cache[url]

        soup = self._fetch(url)
        if not soup:
            return None

        try:
            # Nom
            name_elem = soup.find("h3", class_="author-title")
            name = name_elem.text.strip() if name_elem else "Unknown"

            # Date de naissance
            born_date_elem = soup.find("span", class_="author-born-date")
            born_date = born_date_elem.text.strip() if born_date_elem else ""

            # Lieu de naissance
            born_loc_elem = soup.find("span", class_="author-born-location")
            born_location = born_loc_elem.text.strip() if born_loc_elem else ""
            # Nettoyer "in " au début
            born_location = re.sub(r"^in\s+", "", born_location)

            # Biographie
            bio_elem = soup.find("div", class_="author-description")
            bio = bio_elem.text.strip() if bio_elem else ""

            author = Author(
                name=name,
                bio=bio,
                born_date=born_date,
                born_location=born_location,
                url=url,
            )

            # Mettre en cache
            self.authors_cache[url] = author
            logger.info("author_scraped", name=name)

            return author

        except Exception as e:
            logger.error("author_parse_failed", url=url, error=str(e))
            return None

    def scrape_by_tag(
        self, tag: str, max_pages: int = 5
    ) -> Generator[Quote, None, None]:
        """
        Scrape les citations par tag.

        Args:
            tag: Nom du tag
            max_pages: Limite de pages

        Yields:
            Objets Quote
        """
        url = f"{self.base_url}/tag/{tag}/"
        page = 1

        while url and page <= max_pages:
            logger.info("scraping_tag", tag=tag, page=page)

            soup = self._fetch(url)
            if not soup:
                break

            for div in soup.find_all("div", class_="quote"):
                quote = self._parse_quote(div)
                if quote:
                    yield quote

            url = self._get_next_page(soup)
            page += 1

    def get_available_tags(self) -> list[str]:
        """
        Récupère la liste des tags disponibles.

        Returns:
            Liste des tags
        """
        soup = self._fetch(self.base_url)
        if not soup:
            return []

        tags = []
        tag_box = soup.find("div", class_="tags-box")

        if tag_box:
            tag_links = tag_box.find_all("a", class_="tag")
            tags = [tag.text.strip() for tag in tag_links]

        return tags

    def scrape_complete(
        self, max_pages: int = None, include_authors: bool = True
    ) -> dict:
        """
        Scrape complet : citations + auteurs.

        Args:
            max_pages: Limite de pages
            include_authors: Scraper aussi les auteurs

        Returns:
            {quotes: [...], authors: [...]}
        """
        quotes = []
        authors = {}

        for quote in self.scrape_all_quotes(max_pages):
            quotes.append(quote)

            # Scraper l'auteur si demandé et pas déjà fait
            if include_authors and quote.author_url:
                if quote.author not in authors:
                    author = self.scrape_author(quote.author_url)
                    if author:
                        authors[quote.author] = author

        return {"quotes": quotes, "authors": list(authors.values())}

    def close(self) -> None:
        """Ferme la session."""
        self.session.close()

"""
Package principal du TP E-Commerce.

Ce package contient :
- storage : Clients MinIO et MongoDB
- scrapers : Scraper pour webscraper.io
- pipeline : Pipeline ETL complet
"""

from .pipeline import EcommercePipeline

__all__ = ["EcommercePipeline"]

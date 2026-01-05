"""
Package de stockage.

Fournit les clients pour :
- MinIO : Stockage d'objets (images, exports)
- MongoDB : Base de données documentaire (produits, stats)
"""

from .minio_client import MinIOStorage
from .mongo_client import MongoDBStorage

__all__ = ["MinIOStorage", "MongoDBStorage"]

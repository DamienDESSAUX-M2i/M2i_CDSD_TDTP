import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Chemins
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Mistral Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "votre-cle-mistral-api")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-medium-latest")

# Embeddings Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Vector Store Configuration
COLLECTION_NAME = "documentation"
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "40"))

# RAG Configuration
DEFAULT_K = 4
DEFAULT_TEMPERATURE = 0.0

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# Logging
LOG_LEVEL = "INFO"

from typing import List, Dict, Tuple, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """
    Gère le vector store et les opérations de retrieval
    """

    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "documentation"
    ):
        """
        Initialise le gestionnaire de vector store

        Args:
            persist_dir: Répertoire de persistance
            embedding_model: Modèle d'embeddings HuggingFace
            collection_name: Nom de la collection
        """
        self.persist_dir = persist_dir
        self.collection_name = collection_name

        # Embeddings
        logger.info(f"Chargement du modèle d'embeddings: {embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.vectorstore = None

    def create_index(self, documents: List[Document]):
        """
        Crée l'index vectoriel

        Args:
            documents: Liste de documents à indexer
        """
        logger.info(f"Création de l'index avec {len(documents)} documents...")
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_dir,
            collection_name=self.collection_name
        )

        logger.info(f"✓ Index créé avec {len(documents)} documents")

    def load_index(self):
        """
        Charge un index existant
        """
        logger.info("Chargement de l'index existant...")
        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_dir,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            logger.info("✓ Index chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de l'index: {e}")
            raise

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Recherche par similarité classique

        Args:
            query: Question de l'utilisateur
            k: Nombre de documents à récupérer

        Returns:
            Liste de documents pertinents
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        return self.vectorstore.similarity_search(query, k=k)

    def mmr_search(self, query: str, k: int = 4, fetch_k: int = 20) -> List[Document]:
        """
        Recherche MMR (Maximum Marginal Relevance) pour diversité

        Args:
            query: Question de l'utilisateur
            k: Nombre de documents à retourner
            fetch_k: Nombre de documents à récupérer avant re-ranking

        Returns:
            Liste de documents diversifiés
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        return self.vectorstore.max_marginal_relevance_search(
            query, k=k, fetch_k=fetch_k
        )

    def search_with_scores(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """
        Recherche avec scores de similarité

        Args:
            query: Question de l'utilisateur
            k: Nombre de documents à récupérer

        Returns:
            Liste de tuples (document, score)
        """
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")

        return self.vectorstore.similarity_search_with_score(query, k=k)

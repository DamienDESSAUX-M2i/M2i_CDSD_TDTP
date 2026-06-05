import numpy as np
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Gère le chargement et le découpage des documents
    """

    def __init__(
        self,
        chunk_size: int = 400,
        chunk_overlap: int = 40,
        separators: Optional[List[str]] = None
    ):
        """
        Initialise le processeur de documents

        Args:
            chunk_size: Taille maximale des chunks
            chunk_overlap: Chevauchement entre les chunks
            separators: Liste des séparateurs pour le découpage
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ". ", " ", ""]
        )

    def process(self, texts: List[str], metadatas: List[Dict]) -> List[Document]:
        """
        Traite les documents : conversion en Documents + chunking

        Args:
            texts: Liste des textes
            metadatas: Liste des métadonnées

        Returns:
            Liste de documents découpés
        """
        # Créer les documents
        documents = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(texts, metadatas)
        ]

        # Chunking
        chunks = self.splitter.split_documents(documents)

        # Enrichir les métadonnées
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
            chunk.metadata["chunk_length"] = len(chunk.page_content)

        logger.info(f"Traitement terminé : {len(documents)} documents -> {len(chunks)} chunks")
        return chunks

    def analyze_chunks(self, chunks: List[Document]) -> Dict:
        """
        Analyse les statistiques des chunks

        Args:
            chunks: Liste de chunks

        Returns:
            Dictionnaire de statistiques
        """
        lengths = [len(chunk.page_content) for chunk in chunks]

        stats = {
            "num_chunks": len(chunks),
            "avg_length": float(np.mean(lengths)),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "std_length": float(np.std(lengths))
        }

        return stats

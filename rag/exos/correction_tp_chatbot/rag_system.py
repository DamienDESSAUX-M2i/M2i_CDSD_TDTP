import logging
from config import MISTRAL_API_KEY, CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL
from data_loader import get_documents, get_metadatas
from document_processor import DocumentProcessor
from vectorstore_manager import VectorStoreManager
from rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_system():

    # 1. Charger les données
    logger.info("\n1. Chargement des données...")
    documents = get_documents()
    metadatas = get_metadatas()
    logger.info(f"{len(documents)} documents chargés")

    # 2. Traiter les documents
    logger.info("\n2. Traitement des documents...")
    processor = DocumentProcessor(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = processor.process(documents, metadatas)
    stats = processor.analyze_chunks(chunks)
    logger.info(f"{stats['num_chunks']} chunks créés")
    logger.info(f"  Longueur moyenne: {stats['avg_length']:.1f} caractères")

    # 3. Créer l'index vectoriel
    logger.info("\n3. Création de l'index vectoriel...")
    vs_manager = VectorStoreManager(
        persist_dir=str(CHROMA_DIR),
        embedding_model=EMBEDDING_MODEL,
        collection_name=COLLECTION_NAME
    )
    vs_manager.create_index(chunks)

    # 4. Initialiser le pipeline RAG
    logger.info("\n4. Initialisation du pipeline RAG avec Mistral...")
    rag_pipeline = RAGPipeline(
        vectorstore_manager=vs_manager,
        api_key=MISTRAL_API_KEY
    )

    return rag_pipeline, vs_manager


def test_system(rag_pipeline):
    logger.info("TESTS DU SYSTÈME")

    test_questions = [
        "Comment créer une liste en Python?",
        "Qu'est-ce que le RAG et comment utilise-t-il les embeddings?",
        "Quelle est la capitale de la France?"  # Question hors sujet
    ]

    for i, question in enumerate(test_questions, 1):
        logger.info(f"\n--- Test {i} ---")
        logger.info(f"Question: {question}")

        try:
            result = rag_pipeline.answer(question)
            logger.info(f"Réponse: {result['answer'][:200]}...")
            logger.info(f"Sources: {result['sources']}")
        except Exception as e:
            logger.error(f"Erreur: {e}")


if __name__ == "__main__":
    rag_pipeline, vs_manager = initialize_system()

    test_system(rag_pipeline)
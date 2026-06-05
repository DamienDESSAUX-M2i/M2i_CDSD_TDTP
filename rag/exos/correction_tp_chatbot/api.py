from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from datetime import datetime
from config import MISTRAL_API_KEY, CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL
from vectorstore_manager import VectorStoreManager
from rag_pipeline import RAGPipeline

# Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Question a poser")
    k: int = Field(4, ge=1, le=10, description="Nombre de documents a recuperer")
    use_mmr: bool = Field(False, description="Utiliser MMR pour la diversite")
    topic_filter: Optional[str] = Field(None, description="Filtrer par topic (python, ml)")

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    num_docs_retrieved: int
    retrieval_method: str
    timestamp: str

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    k: int = Field(4, ge=1, le=10)

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    vectorstore_initialized: bool

vs_manager = None
rag_pipeline = None


@app.on_event("startup")
async def startup_event():
    global vs_manager, rag_pipeline

    logger.info("Initialisation du système RAG...")

    try:
        vs_manager = VectorStoreManager(
            persist_dir=str(CHROMA_DIR),
            embedding_model=EMBEDDING_MODEL,
            collection_name=COLLECTION_NAME
        )
        vs_manager.load_index()

        rag_pipeline = RAGPipeline(
            vectorstore_manager=vs_manager,
            api_key=MISTRAL_API_KEY
        )

        logger.info("Système RAG initialisé avec succès")

    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        raise

@app.get("/", tags=["Info"])
async def root():
    """Informations sur l'API."""
    return {
        "name": "Documentation Chatbot API",
        "version": "1.0.0",
        "description": "API RAG pour documentation technique",
        "endpoints": {
            "GET /": "Info sur l'API",
            "GET /health": "Health check",
            "POST /ask": "Poser une question",
            "POST /search": "Recherche seule (sans generation)"
        },
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check de l'API."""
    # Vérifier que le vectorstore est initialisé
    vectorstore_ok = (
        rag_pipeline is not None and
        rag_pipeline.vectorstore_manager.vectorstore is not None
    )

    return HealthResponse(
        status="healthy" if vectorstore_ok else "initializing",
        timestamp=datetime.now().isoformat(),
        vectorstore_initialized=vectorstore_ok
    )

@app.post("/ask", response_model=AnswerResponse, tags=["RAG"])
async def ask(request: QuestionRequest):
    """
    Pose une question au chatbot et obtient une réponse générée.
    """
    if rag_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Le système RAG n'est pas encore initialisé"
        )

    try:
        logger.info(f"Question reçue: {request.question}")

        # Préparer les filtres
        filters = None
        if request.topic_filter:
            filters = {"topic": request.topic_filter}

        # Appeler le pipeline RAG avec Mistral
        result = rag_pipeline.answer(
            question=request.question,
            k=request.k,
            use_mmr=request.use_mmr,
            filters=filters
        )

        return AnswerResponse(
            **result,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Erreur lors du traitement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", tags=["Retrieval"])
async def search(request: SearchRequest):
    """
    Recherche de documents pertinents sans génération.
    """
    if rag_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Le système RAG n'est pas encore initialisé"
        )

    try:
        logger.info(f"Recherche: {request.query}")

        # Recherche seule
        docs = rag_pipeline.vectorstore_manager.similarity_search(
            request.query, k=request.k
        )

        # Formater les résultats
        formatted_docs = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]

        return {
            "query": request.query,
            "num_results": len(formatted_docs),
            "documents": formatted_docs
        }

    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
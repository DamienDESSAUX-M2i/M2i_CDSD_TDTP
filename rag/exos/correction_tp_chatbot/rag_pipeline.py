from typing import Dict, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from vectorstore_manager import VectorStoreManager
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Pipeline RAG complet : retrieval + generation avec Mistral
    """

    def __init__(
        self,
        vectorstore_manager: VectorStoreManager,
        api_key: str,
        model_name: str = "mistral-large-latest",
        temperature: float = 0.0
    ):
        """
        Initialise le pipeline RAG

        Args:
            vectorstore_manager: Gestionnaire du vector store
            api_key: Clé API Mistral
            model_name: Nom du modèle Mistral
            temperature: Température de génération
        """
        self.vectorstore_manager = vectorstore_manager

        # Initialisation du LLM Mistral
        logger.info(f"Initialisation de Mistral: {model_name}")
        self.llm = ChatMistralAI(
            model=model_name,
            mistral_api_key=api_key,
            temperature=temperature
        )

        # Prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un assistant expert en documentation technique.
Réponds aux questions en te basant UNIQUEMENT sur le contexte fourni.
TOUJOURS citer les sources (ex: [python_lists.md]).
Si l'information n'est pas dans le contexte, dis "Je ne trouve pas cette information dans la documentation fournie."
Sois précis, concis et structure tes réponses."""),
            ("user", """Contexte:
{context}

Question: {question}

Réponse:""")
        ])

    def answer(
        self,
        question: str,
        k: int = 4,
        use_mmr: bool = False,
        filters: Optional[Dict] = None
    ) -> Dict:
        """
        Pipeline complet : retrieval + generation

        Args:
            question: Question de l'utilisateur
            k: Nombre de documents à récupérer
            use_mmr: Utiliser MMR pour la diversité
            filters: Filtres sur les métadonnées

        Returns:
            Dict avec answer, sources, contexts, metadata
        """
        logger.info(f"Question reçue: {question}")

        # 1. Retrieval
        if filters:
            logger.info(f"Recherche filtrée: {filters}")
            retrieved_docs = self.vectorstore_manager.filtered_search(
                question, filters, k=k
            )
        elif use_mmr:
            logger.info("Recherche MMR")
            retrieved_docs = self.vectorstore_manager.mmr_search(question, k=k)
        else:
            logger.info("Recherche par similarité")
            retrieved_docs = self.vectorstore_manager.similarity_search(question, k=k)

        # 2. Préparer le contexte
        context_parts = []
        sources = []

        for i, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get('source', 'unknown')
            context_parts.append(f"[Document {i} - {source}]\n{doc.page_content}")
            sources.append(source)

        context = "\n\n".join(context_parts)

        # 3. Génération avec Mistral
        logger.info("Génération de la réponse avec Mistral...")
        messages = self.prompt_template.format_messages(
            context=context,
            question=question
        )

        response = self.llm.invoke(messages)

        # 4. Résultat
        result = {
            "answer": response.content,
            "sources": list(set(sources)),  # Sources uniques
            "contexts": [doc.page_content for doc in retrieved_docs],
            "num_docs_retrieved": len(retrieved_docs),
            "retrieval_method": "mmr" if use_mmr else ("filtered" if filters else "similarity")
        }

        logger.info(f"Réponse générée (sources: {result['sources']})")
        return result

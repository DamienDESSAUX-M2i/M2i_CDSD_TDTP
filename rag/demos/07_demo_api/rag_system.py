from typing import Dict, List

from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI


class RAGSystem:
    def __init__(
        self,
        mistral_api_key: str,
        persist_dir: str = "./chroma_db",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        # Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )

        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        # Vector store
        self.persist_dir = persist_dir
        self.vectorstore = None

        # LLM
        self.llm = ChatMistralAI(
            model="mistral-small-latest", temperature=0, api_key=mistral_api_key
        )

        # Prompt
        self.prompt_template = ChatPromptTemplate.from_template("""
Tu es un assistant qui répond aux questions en utilisant UNIQUEMENT le contexte fourni.
Si la réponse n'est pas dans le contexte, dis "Je n'ai pas cette information."

Contexte:
{context}

Question: {question}

Réponse:""")

    def index_documents(self, texts: List[str], metadatas: List[Dict] = None):
        # Créer des documents
        documents = [
            Document(page_content=text, metadata=metadatas[i] if metadatas else {})
            for i, text in enumerate(texts)
        ]

        # Chunker
        chunks = self.splitter.split_documents(documents)

        # Indexer
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir,
        )

        return len(chunks)

    def load_index(self):
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir, embedding_function=self.embeddings
        )

    def query(self, question: str, k: int = 4) -> Dict:
        if self.vectorstore is None:
            raise ValueError(
                "Index not loaded. Call load_index() or index_documents() first."
            )

        # Retrieval
        docs = self.vectorstore.similarity_search(question, k=k)

        # Construire le contexte
        context = "\n\n".join(
            [f"Document {i + 1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
        )

        # Génération
        prompt = self.prompt_template.format(context=context, question=question)
        response = self.llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": [
                {"content": doc.page_content, "metadata": doc.metadata} for doc in docs
            ],
        }

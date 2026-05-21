from contextlib import asynccontextmanager
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_system import RAGSystem


class Question(BaseModel):
    text: str
    k: Optional[int] = 4


class Answer(BaseModel):
    question: str
    answer: str
    sources: List[Dict]


rag_system = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_system

    mistral_api_key = "n1gnUla1CUVYBINxBo2Qh23wOI7kbtLg"

    rag_system = RAGSystem(mistral_api_key)
    rag_system.load_index()

    print("API RAG démarrée")
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/ask", response_model=Answer)
async def ask(question: Question):
    if rag_system is None:
        raise HTTPException(status_code=503, detail="Rag system pas encore prêt")

    result = rag_system.query(question.text, k=question.k)

    return Answer(
        question=question.text, answer=result["answer"], sources=result["sources"]
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

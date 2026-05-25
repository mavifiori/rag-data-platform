from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.business.rag_engine import RAGEngine

router = APIRouter(prefix="/query", tags=["RAG Query Engine"])
engine = RAGEngine()

class QueryRequest(BaseModel):
    question: str
    limit: int = 3

@router.post("")
async def ask_question(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
    
    response = await engine.ask(payload.question, payload.limit)
    return response
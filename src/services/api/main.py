from fastapi import FastAPI

from services.api.routes import documents_router, query_router 


app = FastAPI(
    title="Enterprise RAG Data Platform",
    description="Plataforma modular de dados e buscas vetoriais (RAG).",
    version="1.0.0"
)

app.include_router(documents_router)
app.include_router(query_router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy", "service": "rag-api-core"}

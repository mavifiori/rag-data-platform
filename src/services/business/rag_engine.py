from shared.database.session import get_db_session, SessionLocal, IS_ASYNC
from services.ai.embeddings import EmbeddingService
from services.ai.llm_client import LLMClient
from sqlalchemy import text

class RAGEngine:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm_client = LLMClient()

    async def ask(self, question: str, limit: int = 3) -> dict:
        # 1. Converte a pergunta do usuário em vetor
        question_vector = self.embedding_service.generate(question)
        
        context_chunks = []
        
        # 2. Busca os trechos mais parecidos por similaridade de cosseno no pgvector
        query = text("""
                SELECT content, document_name, 1 - (embedding <=> :vector) as similarity
                FROM document_sections
                ORDER BY embedding <=> :vector
                LIMIT :limit
            """)

        if IS_ASYNC:
            async with SessionLocal() as session:
                result = await session.execute(query, {
                    "vector": str(question_vector),
                    "limit": limit
                })
                rows = result.all()
        else:
            with get_db_session() as session:
                result = session.execute(query, {
                    "vector": str(question_vector),
                    "limit": limit
                })
                rows = result.all()

        for row in rows:
            if row.similarity > 0.7:
                context_chunks.append(row.content)

        # 3.  avisa a LLM para não inventar coisas (Alucinação)
        context_text = "\n---\n".join(context_chunks) if context_chunks else "Nenhum documento relevante encontrado."

        # 4. Cria o Prompt injetando o contexto recuperado do banco
        prompt = f"""
        Você é um assistente virtual focado em responder dúvidas com base estritamente nos documentos fornecidos abaixo.
        Se a resposta não puder ser encontrada no contexto fornecido, diga educadamente que não sabe e não tente inventar fatos.

        CONTEXTO DOS DOCUMENTOS:
        {context_text}

        PERGUNTA DO USUÁRIO:
        {question}

        RESPOSTA:
        """

        # 5. Gera a resposta final usando a LLM
        answer = self.llm_client.generate_response(prompt)

        return {
            "answer": answer,
            "sources_used": len(context_chunks) > 0
        }
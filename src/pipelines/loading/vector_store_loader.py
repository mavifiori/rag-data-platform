from typing import List, Dict
from shared.database.session import get_db_session
from services.ai.embeddings import EmbeddingService
from sqlalchemy import text

class VectorStoreLoader:
    
    
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def load_chunks(self, document_name: str, storage_uri: str, chunks: List[Dict[str, any]]):
    
        if not chunks:
            print("[Loading] Nenhum chunk enviado para gravação.")
            return

        print(f"[Loading] Gerando embeddings para {len(chunks)} chunks de '{document_name}'...")

        # Abre uma sessão com o banco de dados (gerenciada via Context Manager)
        with get_db_session() as session:
            try:
                # Query SQL  (ajuste os nomes das colunas conforme seu init.sql)
                # Tabela 'document_sections'
                query = text("""
                    INSERT INTO document_sections (document_name, storage_uri, chunk_index, content, embedding)
                    VALUES (:doc_name, :uri, :idx, :content, :embedding_vector)
                """)

                for chunk in chunks:
                   
                    vector = self.embedding_service.generate(chunk["text"])
                    
                    session.execute(query, {
                        "doc_name": document_name,
                        "uri": storage_uri,
                        "idx": chunk["meta"]["chunk_index"],
                        "content": chunk["text"],
                        "embedding_vector": str(vector) 
                    })
                
                # Confirma a transação no banco de dados para todos os chunks de uma vez
                session.commit()
                print(f"[Loading] Sucesso! {len(chunks)} vetores inseridos no banco de dados.")
                
            except Exception as e:
                session.rollback() # Cancela tudo se houver falha, garantindo consistência
                raise RuntimeError(f"Falha ao carregar vetores no banco de dados: {str(e)}")
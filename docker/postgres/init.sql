-- 1. Habilita a extensão de busca vetorial no PostgreSQL
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Cria a tabela que armazenará os metadados do documento e os chunks de texto
CREATE TABLE IF NOT EXISTS document_sections (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    storage_uri VARCHAR(512) NOT NULL,       -- Caminho do arquivo bruto no MinIO (Lineage)
    chunk_index INT NOT NULL,                -- Ordem do pedaço no documento original
    content TEXT NOT NULL,                   -- O pedaço de texto transformado
    embedding VECTOR(384),                   -- Vetor gerado (384 dimensões é o padrão do all-MiniLM-L6-v2)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Cria um índice IVFFlat ou HNSW para acelerar as buscas vetoriais em larga escala
-- (O operador vector_cosine_ops é usado para a similaridade de cosseno <=> que usamos na API)
CREATE INDEX IF NOT EXISTS document_sections_embedding_idx 
ON document_sections USING hnsw (embedding vector_cosine_ops);
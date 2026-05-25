import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """
    Centraliza e valida todas as variáveis de ambiente e configurações globais do projeto.
    Se uma variável obrigatória estiver faltando, o Pydantic impede o sistema de ligar.
    """
    
    # --- CONFIGURAÇÕES DO POSTGRES ---
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@postgres:5432/rag_db",
        description="URL de conexão completa com o PostgreSQL"
    )
    
    # --- CONFIGURAÇÕES DO MINIO / S3 ---
    MINIO_ENDPOINT: str = Field(default="minio:9000")
    MINIO_ROOT_USER: str = Field(default="minioadmin")
    MINIO_ROOT_PASSWORD: str = Field(default="minioadmin")
    RAW_BUCKET_NAME: str = Field(default="raw-documents")
    
    # --- CONFIGURAÇÕES DE IA (LLM & EMBEDDINGS) ---
    OLLAMA_ENDPOINT: str = Field(default="http://ollama:11434")
    LLM_MODEL_NAME: str = Field(default="llama3")
    EMBEDDING_MODEL_NAME: str = Field(default="all-MiniLM-L6-v2")
    
    # --- CONFIGURAÇÕES DO PIPELINE DE INGESTÃO ---
    WATCH_DIRECTORY: str = Field(
        default="/app/data",
        description="Diretório local monitorado pelo Worker de Ingestão"
    )
    CHUNK_SIZE: int = Field(default=1000, description="Tamanho máximo de cada bloco de texto")
    CHUNK_OVERLAP: int = Field(default=200, description="Sobreposição de caracteres entre blocos")

    # Configuração do Pydantic para ler arquivos .env automaticamente se existirem localmente
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore" # Ignora variáveis de ambiente extras que não estão mapeadas aqui
    )

# Instancia o objeto de configurações como um Singleton global
settings = Settings()
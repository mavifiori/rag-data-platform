import os
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    
    _instance = None

    def __new__(cls):
    
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
           
            model_name = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
            print(f"[AI] Carregando modelo de embeddings: {model_name}...")
            cls._instance.model = SentenceTransformer(model_name)
        return cls._instance

    def generate(self, text: str) -> list:
        
        if not text:
            return []
        embedding = self.model.encode(text)
        return embedding.tolist()
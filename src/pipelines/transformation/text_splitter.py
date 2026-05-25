from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter as LangChainSplitter

class RecursiveTextSplitter:
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        
        self.splitter = LangChainSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_text(self, text: str) -> List[Dict[str, any]]:
        if not text:
            return []

        # O LangChain quebra o texto e devolve uma lista de strings
        raw_chunks = self.splitter.split_text(text)
        
      
        structured_chunks = []
        for index, chunk in enumerate(raw_chunks):
            structured_chunks.append({
                "text": chunk,
                "meta": {
                    "chunk_index": index,
                    "character_count": len(chunk),
                    "word_count": len(chunk.split())
                }
            })
            
        return structured_chunks
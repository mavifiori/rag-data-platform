from abc import ABC, abstractmethod
from typing import List, Dict
from pipelines.transformation import TextCleaner, RecursiveTextSplitter

class BaseLoader(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def extract_text(self) -> str:
        pass

    def extract_and_chunk(self, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, any]]:
        raw_text = self.extract_text()
        
        # Limpa ruídos básicos do texto
        cleaned_text = TextCleaner.clean(raw_text) 
        
        # Divide usando o novo splitter turbinado com LangChain
        splitter = RecursiveTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return splitter.split_text(cleaned_text)
from .pdf_loader import PDFLoader
from .txt_loader import TextLoader

# Define o que será importado ao usar "from pipelines.extraction import *"
__all__ = ["PDFLoader", "TextLoader"]
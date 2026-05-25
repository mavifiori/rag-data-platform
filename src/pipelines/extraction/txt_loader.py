from pipelines.extraction.base import BaseLoader

class TextLoader(BaseLoader):
    def extract_text(self) -> str:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                full_text = f.read()
            return " ".join(full_text.split())
        
        except UnicodeEncodeError: 
            with open(self.file_path, "r", encoding="iso-8859-1") as f:
                full_text = f.read()
            return " ".join(full_text.split())
        
        except Exception as e:
            print(f"[X] Erro ao ler o TXT {self.file_path}: {str(e)}")
            return ""
        
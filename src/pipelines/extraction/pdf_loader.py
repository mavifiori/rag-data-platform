from pipelines.extraction.base import BaseLoader
import pypdf

class PDFLoader(BaseLoader):

    def extract_text(self) -> str:
        text_content = []
        try:
            with open(self.file_path, "rb") as file:
                reader = pypdf.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            full_text = "\n".join(text_content)
            return " ".join(full_text.split())
        except Exception as e:
            print(f"[X] Erro ao ler o PDF {self.file_path}: {str(e)}")
            return ""
        
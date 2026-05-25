import re

class TextCleaner:
    
    @staticmethod
    def clean(text: str) -> str:  # <--- Nome corrigido para 'clean'
        if not text:
            return ""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove caracteres especiais e números (Mantendo sua lógica)
        text = re.sub(r'[^A-Za-z\s]', '', text)
        
        # Converte para minúsculas
        text = text.lower()
        
        return text.strip()
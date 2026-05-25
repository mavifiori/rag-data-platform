import os
import time
from pipelines.extraction.pdf_loader import PDFLoader
from pipelines.extraction.txt_loader import TextLoader  
# 📑 LINHA ADICIONADA: Importa os loaders da camada de carregamento de dados
from pipelines.loading import DataLakeLoader, VectorStoreLoader
from config.settings import settings

def process_pipeline(local_file_path: str):
    file_name = os.path.basename(local_file_path)
    print(f"[Pipeline] Iniciando processamento do arquivo: {file_name}")
    
    # 1. INICIALIZA OS LOADERS (Camada de Loading)
    lake_loader = DataLakeLoader()
    vector_loader = VectorStoreLoader()
    
    # [L do ETL - Parte 1] Carrega o bruto direto no Data Lake antes de tudo
    storage_uri = lake_loader.load_to_raw_zone(local_file_path)

    # 2. SELECIONA O EXTRACTOR COM BASE NA EXTENSÃO (Camada de Extraction)
    if file_name.endswith('.pdf'):
        loader = PDFLoader(local_file_path)
    else:
        loader = TextLoader(local_file_path)

    # 3. EXTRAI E TRANSFORMA (Camada de Extraction + Transformation embutida)
    text_chunks = loader.extract_and_chunk(
        chunk_size=settings.CHUNK_SIZE, 
        overlap=settings.CHUNK_OVERLAP
    )

    # 4. PERSISTE OS VETORES (Camada de Loading )
    vector_loader.load_chunks(
        document_name=file_name, 
        storage_uri=storage_uri, 
        chunks=text_chunks
    )
    
    print(f"[Pipeline] Processamento do arquivo {file_name} concluído com sucesso!")

def start_pipeline_worker():
    """
    Garante o monitoramento do diretório configurado. 
    Lê os arquivos existentes e mantém o container ativo de forma estável.
    """
    path_to_watch = settings.WATCH_DIRECTORY
    
    # Garante que a pasta de entrada exista no container mapeado
    os.makedirs(path_to_watch, exist_ok=True)
    print(f"[Worker] Monitorando a pasta de dados em: {path_to_watch}")
    
    # Loop contínuo para manter o container ativo em segundo plano
    while True:
        files = [os.path.join(path_to_watch, f) for f in os.listdir(path_to_watch) 
                 if f.endswith(('.pdf', '.txt'))]
        
        for file_path in files:
            try:
                process_pipeline(file_path)
                # Remove ou move o arquivo após o processamento para não reprocessar em loop
                os.remove(file_path) 
            except Exception as e:
                print(f"[X] Erro crítico ao processar {os.path.basename(file_path)}: {str(e)}")
        
        # Aguarda um intervalo antes de varrer o diretório novamente
        time.sleep(5)

if __name__ == "__main__":
    start_pipeline_worker()
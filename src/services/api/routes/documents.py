import os
from fastapi import APIRouter, UploadFile, File, HTTPException

# 1. Criação do roteador (Apenas uma vez)
router = APIRouter(prefix="/documents", tags=["Documents Management"])

# 2. Caminho para a pasta onde o Ingestion Worker (Watchdog) está escutando
UPLOAD_DIR = "/app/data"

# 3. Definição da rota com o parâmetro 'file' corrigido
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Recebe um arquivo PDF ou TXT e o envia para a Landing Zone
    para ser processado de forma assíncrona pelo Pipeline de Dados.
    """
    # Validação de formato de arquivo
    allowed_extensions = [".pdf", ".txt", ".md"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Extensão {file_ext} não suportada. Envie apenas: {', '.join(allowed_extensions)}"
        )

    # Garante que o diretório local exista
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Define o caminho final do arquivo salvo localmente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Salva o arquivo em blocos (chunks de memória) para suportar arquivos grandes
        with open(file_path, "wb") as buffer:
            while content := await file.read(1024 * 1024):  # 1MB por vez
                buffer.write(content)
                
        return {
            "status": "success",
            "message": f"Arquivo '{file.filename}' recebido com sucesso. O processamento foi iniciado em segundo plano."
        }
        
    except Exception as e:
        print(f"[X] Erro ao salvar arquivo no endpoint de upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno ao salvar o arquivo no servidor.")
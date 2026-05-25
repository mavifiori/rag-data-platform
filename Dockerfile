# ==========================================
# 1. Estágio Base (Compartilhado)
# ==========================================
# ==========================================
# 1. Estágio Base (Compartilhado)
# ==========================================
FROM python:3.11-slim AS base

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configurar a variável de ambiente para o Python encontrar o diretório 'src'
ENV PYTHONPATH=/app/src

# Copiar todo o código fonte para dentro do container
COPY src/ /app/src/

# ==========================================
# 2. Alvo para o Serviço de API
# ==========================================
FROM base AS api
WORKDIR /app
EXPOSE 8000
# Força o Uvicorn a olhar a pasta src como diretório raiz do código
CMD ["uvicorn", "src.services.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# 3. Alvo para o Serviço de Ingestão (Worker)
# ==========================================
FROM base AS ingestion
WORKDIR /app
# Aponta o caminho absoluto do arquivo a partir da raiz /app
CMD ["python", "src/pipelines/run_ingestion.py"]
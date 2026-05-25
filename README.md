# 🚀 RAG Data Platform: Plataforma de Dados e Ingestão Escalável para LLMs

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-blue.svg)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20Framework-green.svg)](https://fastapi.tiangolo.com/)

Uma infraestrutura corporativa local e ponta a ponta para **Engenharia de Dados aplicada a LLMs (Retrieval-Augmented Generation)**. Este projeto simula um ambiente produtivo de microsserviços para ingestão, processamento, vetorização e consumo de dados não estruturados (PDFs).

```mermaid
graph TD
    subgraph Frontend [Camada 1: Fontes & Frontend]
        UI[Streamlit UI<br/>Painel de Utilizador]
    end

    subgraph Storage [Camada 2: Armazenamento & Orquestração]
        API[FastAPI<br/>API Gateway / Orquestrador]
        MinIO[(MinIO Object Storage<br/>Data Lake: Bronze/Silver/Gold)]
        Worker[Python Worker<br/>Ingestão Assíncrona]
    end

    subgraph AI_DB [Camada 3: Serving & Consumo IA]
        Ollama((Ollama<br/>LLM Local & Embeddings))
        PG[(PostgreSQL + pgvector<br/>Base de Dados Vetorial)]
    end

    %% Fluxo de Ingestão (Linhas sólidas)
    UI -- "1. Upload de PDF" --> API
    API -- "2. Guarda Ficheiro Bruto" --> MinIO
    Worker -- "3. Extrai Texto/Chunks" --> MinIO
    Worker -- "4. Pede Embeddings" --> Ollama
    Worker -- "5. Guarda Chunks Vetorizados" --> PG

    %% Fluxo de Consulta RAG (Linhas a tracejado)
    UI -. "A. Pergunta do Utilizador" .-> API
    API -. "B. Converte Pergunta em Vetor" .-> Ollama
    API -. "C. Busca Semântica (Cosseno)" .-> PG
    API -. "D. Gera Resposta (Prompt + Contexto)" .-> Ollama
    Ollama -. "E. Resposta Final" .-> API
    API -. "F. Exibe Resposta" .-> UI

    %% Estilos de cor para diferenciar
    classDef storage fill:#f9d0c4,stroke:#e06666,stroke-width:2px,color:#000;
    classDef compute fill:#c9daf8,stroke:#6d9eeb,stroke-width:2px,color:#000;
    classDef frontend fill:#d9ead3,stroke:#93c47d,stroke-width:2px,color:#000;
    classDef ai fill:#fff2cc,stroke:#ffd966,stroke-width:2px,color:#000;
    
    class MinIO,PG storage;
    class API,Worker compute;
    class UI frontend;
    class Ollama ai;
```
---

## 🚀 Objetivo

Construir um pipeline de dados e inteligência artificial que:
- ingere documentos em diferentes formatos;
- armazena dados em PostgreSQL com `pgvector`;
- mantém arquivos em MinIO como data lake;
- utiliza um modelo LLM local via Ollama;
- expõe API REST e UI Streamlit para consulta e pesquisa.

## 🧱 Stack principal

- Python 3.11
- FastAPI
- Streamlit
- PostgreSQL + pgvector
- MinIO
- Ollama
- SQLAlchemy
- LangChain text splitters
- Sentence Transformers

## 📁 Estrutura do projeto

- `docker-compose.yml` - orquestra os serviços: `postgres`, `minio`, `ollama`, `api`, `ingestion`, `frontend`
- `Dockerfile` - imagem base Python para serviços de produção/local
- `requirements.txt` - dependências Python necessárias
- `src/`
  - `config/settings.py` - configurações e variáveis de ambiente
  - `frontend/app.py` - app Streamlit
  - `pipelines/run_ingestion.py` - workflow de ingestão de dados
  - `pipelines/extraction/` - carregadores de documentos (`pdf_loader.py`, `txt_loader.py`)
  - `pipelines/transformation/` - limpeza e quebra de texto (`text_cleaner.py`, `text_splitter.py`)
  - `pipelines/loading/` - carregamento para data lake e vetor store
  - `services/ai/` - embeddings e cliente LLM
  - `services/api/main.py` - app FastAPI
  - `services/api/routes/` - rotas da API (`documents.py`, `query.py`)
  - `services/business/rag_engine.py` - lógica de RAG
  - `shared/database/session.py` - sessão de banco de dados
  - `shared/storage/minio_client.py` - cliente MinIO
- `data/` - local para dados e conteúdos ingestados
- `docker/` - scripts e arquivos de inicialização de containers

## ⚙️ Serviços em `docker-compose`

- `postgres`: banco de dados com `pgvector`
- `minio`: armazenamento de objetos compatível com S3
- `ollama`: LLM local para inferência
- `api`: API FastAPI em `http://localhost:8000`
- `ingestion`: worker de ingestão de dados
- `frontend`: interface Streamlit em `http://localhost:8501`

## ▶️ Como rodar o projeto

### 1. Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11 (opcional para execução local sem Docker)

### 2. Rodar com Docker Compose

```bash
cd "C:\Users\vicsf\OneDrive\Área de Trabalho\RAG"
docker compose up --build
```

### 3. Acessar serviços

- API: `http://localhost:8000`
- Documentação OpenAPI: `http://localhost:8000/docs`
- Front-end Streamlit: `http://localhost:8501`
- MinIO Console: `http://localhost:9001`

### 4. Variáveis de ambiente

O `docker-compose.yml` já define valores padrão para:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`
- `DATABASE_URL`
- `MINIO_ENDPOINT`
- `OLLAMA_ENDPOINT`

Se quiser personalizar, crie um arquivo `.env` ou exporte as variáveis antes de executar.

## 🧪 Fluxo de ingestão

O serviço `ingestion` executa o pipeline de ingestão:
- faz extração de textos de arquivos
- limpa e quebra conteúdo
- gera embeddings
- salva no banco e no data lake

Se você quiser rodar localmente dentro do container, o comando já está configurado em `docker-compose.yml`.

## 💡 Dicas de desenvolvimento

- O serviço `api` depende de `postgres`, `minio` e `ollama`
- Se precisar reiniciar somente o front-end ou API, use:
  - `docker compose restart api`
  - `docker compose restart frontend`
- Para remover containers e volumes:
  - `docker compose down -v`

## 🔎 Endpoints principais

- `GET /health` - health check do serviço API
- `GET /docs` - documentação interativa da API
- `POST /documents/upload` - upload de documento (`.pdf`, `.txt`, `.md`)
- `POST /query` - consulta RAG com pergunta e limite de resultados

## 🧪 Exemplos de uso

### Consulta RAG

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual é o objetivo do projeto?", "limit": 3}'
```

### Upload de documento

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/caminho/para/seu/arquivo.pdf"
```

## 📌 Observações

- O projeto já está preparado para rodar em container com dependências instaladas à cada inicialização.
- Caso use `docker compose up` e deseje ver logs específicos de um serviço, execute `docker compose logs -f api`.

---

Desenvolvido como base para uma arquitetura RAG modular e orientada a dados, com pipeline de ingestão, vetor store e interface de consulta.

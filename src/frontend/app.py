import streamlit as st
import requests
import os


st.set_page_config(
    page_title="RAG Data Platform Portal",
    page_icon="🤖",
    layout="wide"
)

# Endpoints da sua API FastAPI (Mapeados pelo Docker ou Local)
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🤖 Plataforma de Dados RAG - Portal do Usuário")
st.subheader("Gerencie seus documentos e faça consultas inteligentes com IA")

# Criação das abas estruturadas
tab_chat, tab_ingestion = st.tabs(["💬 Chatbot Inteligente", "⚙️ Ingestão & Data Lake"])

# =========================================================================
# ABA 1: INTERFACE DE CHAT (Consumo do RAG)
# =========================================================================
with tab_chat:
    st.header("Converse com seus Documentos")
    
    # Inicializa o histórico de mensagens na memória da sessão do navegador
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Renderiza as mensagens anteriores do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if prompt := st.chat_input("O que você deseja saber sobre os documentos armazenados?"):
        # Exibe a pergunta do usuário no chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            with st.spinner("Buscando contexto e gerando resposta com LLM..."):
                try:
                    # Envia a requisição para a rota /query que criamos na API
                    response = requests.post(
                        f"{API_URL}/query",
                        json={"question": prompt, "limit": 3},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "Sem resposta.")
                        sources = data.get("sources_used", False)
                        
                        # Renderiza a resposta da IA
                        st.markdown(answer)
                        
                        # Exibe se fontes do Data Lake foram usadas (Rastreabilidade)
                        if sources:
                            st.caption("✅ *Resposta gerada com base em fragmentos do seu Data Lake.*")
                        else:
                            st.caption("⚠️ *Nenhum fragmento correspondente foi encontrado. Resposta gerada por conhecimento geral.*")
                        
                        # Salva no histórico
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Erro na API ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Não foi possível conectar à API de IA: {str(e)}")

# =========================================================================
# ABA 2: PIPELINE E INGESTÃO (Visão de Engenharia de Dados)
# =========================================================================
with tab_ingestion:
    st.header("Gerenciamento do Pipeline de Dados")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Fazer Upload de Novo Documento")
        uploaded_file = st.file_uploader(
            "Arraste ou selecione um arquivo (PDF, TXT)", 
            type=["pdf", "txt", "md"]
        )
        
        if uploaded_file is not None:
            if st.button("🚀 Enviar para o Pipeline", use_container_width=True):
                with st.spinner("Enviando arquivo para a API..."):
                    try:
                        # Prepara o payload de multipart form-data para o FastAPI
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        
                        # Envia para a nossa rota de documentos/upload
                        res = requests.post(f"{API_URL}/documents/upload", files=files)
                        
                        if res.status_code == 200:
                            st.success(f"🎉 {res.json().get('message')}")
                            st.balloons() # Feedback visual divertido de sucesso
                        else:
                            st.error(f"Falha no upload: {res.text}")
                    except Exception as e:
                        st.error(f"Erro ao conectar ao serviço de upload: {str(e)}")
                        
    with col2:
        st.subheader("Status dos Repositórios e Observabilidade")
        st.info("💡 **Fluxo Assíncrono:** Os arquivos enviados na coluna ao lado entram na Zona de Landing do servidor. O *Worker de Ingestão* (Watchdog) vai processar, extrair o texto com LangChain, gerar os embeddings e salvar no banco de dados automaticamente.")
        
        # Exemplo visual de cards de monitoramento
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric(label="Zona de Armazenamento (MinIO)", value="raw-documents", delta="Conectado")
        metric_col2.metric(label="Banco Vetorial (PostgreSQL)", value="document_sections", delta="Ativo (pgvector)")
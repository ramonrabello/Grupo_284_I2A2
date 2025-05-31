import os
import pandas as pd
import zipfile
import streamlit as st
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (onde está sua API Key)
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# --- Configuração do LLM (Google Gemini) ---
# Pega a chave da variável de ambiente carregada por dotenv
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("Erro: A GOOGLE_API_KEY não foi encontrada no arquivo .env ou nas variáveis de ambiente.")
    st.stop() # Interrompe a execução do Streamlit

# Opção A (mais provável de funcionar):
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.0)

# Opção B (se a A não funcionar, mas menos comum para o que precisamos):
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.0)

# --- Funções Auxiliares para o Agente ---

def get_dataframe_from_file(file_path):
    """Carrega um arquivo CSV ou Excel em um DataFrame do Pandas."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        st.warning(f"Formato de arquivo não suportado: {file_path}. Suportamos .csv, .xls, .xlsx.")
        return None

def find_data_file(data_folder, query):
    """
    Tenta identificar qual arquivo nos dados deve ser usado para responder a pergunta.
    Pode ser melhorado com lógica mais avançada de correspondência de tópicos ou metadados.
    """
    files = [f for f in os.listdir(data_folder) if f.endswith(('.csv', '.xls', '.xlsx'))]
    
    # Lógica simples para selecionar o arquivo:
    # Se houver apenas um arquivo, usa ele.
    if len(files) == 1:
        st.info(f"Usando o arquivo único: {files[0]}")
        return os.path.join(data_folder, files[0])
    
    # Tenta adivinhar baseado em palavras-chave
    if "fornecedor" in query.lower() or "montante" in query.lower() or "recebido" in query.lower():
        for f in files:
            if "fornecedor" in f.lower() or "venda" in f.lower() or "recebimento" in f.lower():
                st.info(f"Parece que você está perguntando sobre fornecedores/vendas. Usando: {f}")
                return os.path.join(data_folder, f)
    
    if "item" in query.lower() or "volume" in query.lower() or "quantidade" in query.lower() or "entrega" in query.lower():
        for f in files:
            if "item" in f.lower() or "produto" in f.lower() or "entrega" in f.lower() or "estoque" in f.lower():
                st.info(f"Parece que você está perguntando sobre itens/entregas. Usando: {f}")
                return os.path.join(data_folder, f)

    # Se não encontrar uma correspondência específica, pede ao usuário para especificar ou escolhe o primeiro.
    if files:
        st.warning("Não consegui determinar qual arquivo usar automaticamente. Por favor, seja mais específico ou nomeie seus arquivos de forma descritiva. Usando o primeiro arquivo encontrado por padrão.")
        return os.path.join(data_folder, files[0])
    return None

def unpack_zip_files(data_folder):
    """Descompacta todos os arquivos .zip na pasta de dados."""
    zip_files = [f for f in os.listdir(data_folder) if f.endswith('.zip')]
    if not zip_files:
        return False # Nenhum arquivo .zip encontrado

    st.info("Descompactando arquivos ZIP...")
    for zip_file in zip_files:
        zip_path = os.path.join(data_folder, zip_file)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_folder)
            st.success(f"Arquivo '{zip_file}' descompactado com sucesso.")
            os.remove(zip_path) # Opcional: remover o .zip após descompactar
        except Exception as e:
            st.error(f"Erro ao descompactar '{zip_file}': {e}")
    return True # Arquivos .zip foram processados


# --- Interface do Usuário com Streamlit ---
st.title("Agente de Perguntas sobre CSVs")
st.write("Faça perguntas sobre seus dados nos arquivos CSV/Excel.")

# Campo para o usuário enviar a pasta dos dados (opcional, mas bom para organização)
data_folder = st.text_input("Pasta dos seus arquivos de dados (CSV/Excel/ZIP):", value="./data")

# Cria a pasta 'data' se não existir
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Upload de arquivos pelo usuário
uploaded_files = st.file_uploader("Ou faça upload de seus arquivos CSV/Excel/ZIP aqui:", type=["csv", "xls", "xlsx", "zip"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path_in_data_folder = os.path.join(data_folder, uploaded_file.name)
        with open(file_path_in_data_folder, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Arquivo '{uploaded_file.name}' carregado para a pasta '{data_folder}'.")

# Descompacta arquivos após o upload ou se já existirem na pasta
unpack_zip_files(data_folder)

# Verifica se há arquivos de dados para processar
available_data_files = [f for f in os.listdir(data_folder) if f.endswith(('.csv', '.xls', '.xlsx'))]

if not available_data_files:
    st.warning("Nenhum arquivo CSV ou Excel encontrado na pasta de dados. Por favor, faça upload ou coloque seus arquivos na pasta especificada.")
else:
    user_question = st.text_input("Sua pergunta:")

    if st.button("Obter Resposta"):
        if user_question:
            st.info("Buscando a resposta...")

            # 1. Tenta identificar o arquivo relevante para a pergunta
            selected_file_path = find_data_file(data_folder, user_question)

            if selected_file_path:
                df = get_dataframe_from_file(selected_file_path)

                if df is not None:
                    # 2. Cria o agente do Pandas para interagir com o DataFrame
                    # verbose=True para ver o "pensamento" do agente no terminal
                    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
                    
                    try:
                        # 3. Executa a pergunta
                        response = agent.run(user_question)
                        st.success(f"**Resposta:** {response}")
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao processar sua pergunta: {e}")
                        st.warning("Tente reformular a pergunta ou verificar a integridade dos dados.")
                else:
                    st.error("Não foi possível carregar o arquivo de dados. Verifique o formato ou o conteúdo.")
            else:
                st.warning("Não foi possível encontrar um arquivo de dados relevante para sua pergunta.")
        else:
            st.warning("Por favor, digite sua pergunta.")
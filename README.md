# Contexto Geral
Este repositório contém o código-fonte do desafio 3, que é um agente inteligente capaz de responder a perguntas sobre arquivos de dados (CSV e Excel), utilizando uma interface amigável para o usuário. O objetivo principal foi criar uma solução que permitisse a interação em linguagem natural com os dados, sem a necessidade de conhecimento técnico em manipulação de planilhas ou programação
# Frameworks & Tools
- LangChain
- Google Gemini (via langchain-google-genai)
- Python
- Streamlit
- Pandas
- python-dotenv
- zipfile
- langchain-experimental
- tabulate

# Estrutura da Solução
A solução foi estruturada em um programa Python `app.py` que utiliza os conceitos de agentes e ferramentas do LangChain, orquestrados por uma interface web do Streamlit.
A arquitetura do agente segue os seguintes passos:

# Interface do Usuário (Streamlit):
Uma aplicação web simples é iniciada, fornecendo campos para o usuário inserir a pasta dos dados (opcional) ou fazer upload de arquivos diretamente. 
Há um campo de texto para o usuário digitar sua pergunta e um botão para "Obter Resposta". 

# Fluxo do app:
1. Ao iniciar ou quando arquivos são carregados, o agente verifica a pasta de dados configurada (./data por padrão). Ele possui uma função `unpack_zip_files` para descompactar automaticamente quaisquer arquivos .zip encontrados, garantindo que os arquivos CSV/Excel estejam acessíveis. 
2. Uma função `find_data_file` tenta identificar o arquivo de dados mais relevante para a pergunta do usuário. Atualmente, essa função usa uma lógica baseada em palavras-chave no nome do arquivo e na pergunta, ou seleciona o primeiro arquivo disponível. 
3. A API Key do Google Gemini é carregada de forma segura a partir de um arquivo .env (ocultada e não versionada). 
4. O LLM (e.g., gemini-1.5-pro-latest) é inicializado usando o objeto `ChatGoogleGenerativeAI`, que serve como o "cérebro" do agente para entender as perguntas e formular as respostas.
5. Para cada pergunta, o arquivo de dados relevante é carregado em um `Pandas` `DataFrame`. 
6. É criado um `create_pandas_dataframe_agent` do LangChain, que é um tipo de agente especializado em interagir com DataFrames. Este agente recebe o LLM e o DataFrame como entrada. 
7. Quando o usuário submete uma pergunta, o agente a processa. Internamente, o LLM recebe a pergunta e o "contexto" do DataFrame (incluindo o cabeçalho e algumas linhas de exemplo). 
8. O LLM, então, "pensa" sobre como responder à pergunta usando as operações do Pandas (como filtrar, somar, agrupar, encontrar o máximo/mínimo).
9. Esse processo de "pensamento" é visível no terminal (verbose=True). 
10. O agente executa as operações do Pandas necessárias nos dados reais. 
Finalmente, o agente usa o LLM para formatar a resposta de forma compreensível ao usuário e a exibe na interface do Streamlit.

# Guia Técnico: Streamlit, Google Gemini e LangChain para Aplicações de IA

Este guia técnico demonstra como integrar Streamlit para construção de interfaces web interativas, Google Gemini como modelo de linguagem poderoso e LangChain para orquestrar e gerenciar as interações com o modelo. Ao final, você terá as ferramentas e o conhecimento para desenvolver aplicações de IA robustas e dinâmicas.

# Pré-requisitos e Instalação
Para começar, certifique-se de ter o Python instalado (versão 3.9 ou superior é recomendada). Em seguida, instale as bibliotecas necessárias:

```bash
pip install streamlit
pip install google-generative-ai
pip install langchain
pip install langchain-experimental
pip install python-dotenv  # Para gerenciar variáveis de ambiente de forma segura
pip install pandas
pip install zipfile
```
# Configurando o Google Gemini
Para utilizar o Google Gemini, você precisará de uma API Key. Siga os passos abaixo para obtê-la e configurá-la:

Obtenha sua API Key: Acesse o Google AI Studio - https://aistudio.google.com/ - e siga as instruções para criar um novo projeto e gerar sua API Key. 
Armazenamento Seguro: Nunca exponha sua API Key diretamente no código. A melhor prática é armazená-la em um arquivo .env e carregá-la usando a biblioteca python-dotenv.
Configurar Arquivo .env: Crie um arquivo .env na raiz do seu projeto com o seguinte conteúdo:

   
 GOOGLE_API_KEY="SUA_API_KEY_AQUI"

   Substitua "SUA_API_KEY_AQUI" pela sua chave de API real.
Introdução ao Streamlit
Streamlit é um framework de código aberto para criar rapidamente aplicações web para ciência de dados e aprendizado de máquina. Ele permite transformar scripts Python em apps interativos com poucas linhas de código.

Exemplo Básico de Streamlit:
Crie um arquivo app.py:

```python
import streamlit as st

st.title("Meu Primeiro App Streamlit")
st.write("Bem-vindo ao Streamlit!")

user_input = st.text_input("Digite algo aqui:", "Olá, mundo!")
st.write(f"Você digitou: {user_input}")

if st.button("Clique-me"):
    st.success("Botão clicado!")
```

Para rodar o aplicativo, execute no terminal:

```bash
streamlit run app.py
```

Seu navegador abrirá automaticamente a aplicação no endereço `localhost:8051`.
Utilizando o Google Gemini com LangChain
LangChain é um framework projetado para simplificar o desenvolvimento de aplicações alimentadas por modelos de linguagem. Ele fornece abstrações e ferramentas para encadear diferentes componentes (modelos de linguagem, prompts, ferramentas, etc.) de forma eficiente.

# Configurando o Gemini com LangChain
Primeiro, vamos configurar o modelo Gemini no LangChain e carregar nossa API Key.

```python
# Em seu arquivo Python (ex: main.py ou app.py)
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import 
ChatGoogleGenerativeAI # Importação ajustada para a versão mais recente do LangChain

load_dotenv()  # Carrega as variáveis de ambiente do .env

# Configura a chave da API do Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada.")
    st.stop()

# Inicializa o modelo Gemini com LangChain
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Exemplo de uso direto do modelo Gemini
# response = llm.invoke("Qual é a capital do Brasil?")
# print(response.content)
```

Nota: A importação para o modelo Gemini no LangChain pode variar ligeiramente dependendo da versão específica da biblioteca `langchain_google_genai`. Certifique-se de que a o comando `import from langchain_google_genai import ChatGoogleGenerativeAI` está correta para sua instalação.
Criando um Sistema de Perguntas e Respostas com LangChain Chains
Vamos construir um sistema simples de perguntas e respostas usando um LLMChain do LangChain.

```python
# Adicione este código ao seu arquivo main.py ou app.py

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Define o template do prompt para o modelo Gemini
prompt_template = ChatPromptTemplate.from_template("Responda à seguinte pergunta de forma concisa: {question}")

# Cria uma LLMChain que combina o prompt e o modelo
qa_chain = LLMChain(llm=llm, prompt=prompt_template)

# Exemplo de uso da chain
# question = "Qual a importância da inteligência artificial?"
# response_chain = qa_chain.invoke({"question": question})
# print(response_chain['text'])
```
Integrando Streamlit, Google Gemini e LangChain
Agora, vamos combinar tudo para criar uma aplicação Streamlit interativa que utiliza o modelo Gemini via LangChain para responder a perguntas.

```python
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Carrega as variáveis de ambiente
load_dotenv()

# --- Configuração da API do Google Gemini ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Erro: A variável de ambiente GOOGLE_API_KEY não está configurada. Crie um arquivo .env com GOOGLE_API_KEY='SUA_API_KEY'.")
    st.stop()

# --- Inicialização do Modelo Gemini com LangChain ---
try:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Erro ao inicializar o modelo Gemini: {e}. Verifique sua API Key.")
    st.stop()

# --- Definição da Chain LangChain ---
prompt_template = ChatPromptTemplate.from_template("Responda à seguinte pergunta de forma clara e útil: {question}")
qa_chain = LLMChain(llm=llm, prompt=prompt_template)

# --- Interface do Streamlit ---
st.set_page_config(page_title="App de Perguntas e Respostas com Gemini e LangChain", page_icon="🤖")
st.title("🤖 App de Perguntas e Respostas com Gemini e LangChain")
st.markdown("Faça uma pergunta e deixe o Google Gemini responder!")

user_question = st.text_input("Sua pergunta:", placeholder="Ex: Qual o objetivo da missão Artemis?")

if st.button("Obter Resposta"):
    if user_question:
        with st.spinner("Pensando na resposta..."):
            try:
                response = qa_chain.invoke({"question": user_question})
                st.subheader("Resposta:")
                st.write(response['text'])
            except Exception as e:
                st.error(f"Ocorreu um erro ao processar sua pergunta: {e}")
    else:
        st.warning("Por favor, digite uma pergunta.")

st.markdown("---")
st.info("Desenvolvido com Streamlit, Google Gemini e LangChain.")
```

Para executar este aplicativo, salve o código acima como app.py e execute:

```bash
streamlit run app.py
```
Próximos Passos e Recursos Adicionais
Este guia forneceu uma base sólida para começar a construir aplicações de IA com Streamlit, Google Gemini e LangChain. Aqui estão algumas ideias para expandir e aprimorar seus projetos:
Histórico de Conversa (Memory): Explore os recursos de Memory do LangChain para manter o contexto em conversas multi-turn.
Ferramentas (Tools): Integre ferramentas externas (como pesquisa na web, APIs de banco de dados) via LangChain para permitir que o modelo Gemini acesse informações além de seu conhecimento pré-treinado.
Agentes (Agents): Utilize Agents do LangChain para permitir que o modelo Gemini raciocine e tome decisões sobre quais ferramentas usar para atingir um objetivo.
Mais Modelos: Experimente outros modelos do Google Gemini ou outros LLMs compatíveis com LangChain.
Deployment: Aprenda a fazer o deploy de suas aplicações Streamlit em plataformas como Streamlit Community Cloud, Hugging Face Spaces ou na nuvem (AWS, GCP, Azure).
Interface mais Complexa: Explore os componentes avançados do Streamlit para criar interfaces de usuário mais ricas e personalizadas.
Solução de Problemas Comuns
ModuleNotFoundError: Verifique se todas as bibliotecas listadas nos pré-requisitos foram instaladas corretamente.
google_api_key não configurada: Certifique-se de que seu arquivo .env está na raiz do projeto e que a chave de API está corretamente definida. Reinicie o terminal ou o ambiente de desenvolvimento se alterou o .env recentemente.
Erros da API Gemini: Verifique sua conexão com a internet e se a API Key é válida. Consulte a documentação do Google Gemini para limites de uso ou outros problemas de serviço.
Versões do LangChain: O LangChain está em constante evolução. Se encontrar erros de importação ou uso, consulte a documentação oficial do LangChain para a versão mais recente.

Com este guia, você está pronto para explorar o vasto potencial da inteligência artificial generativa e construir suas próprias aplicações inovadoras!

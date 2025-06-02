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

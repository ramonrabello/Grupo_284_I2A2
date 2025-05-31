import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # Carrega sua GOOGLE_API_KEY do .env

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Erro: GOOGLE_API_KEY não encontrada. Verifique seu arquivo .env.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    print("Modelos disponíveis:")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"  - {m.name} (compatível com generateContent)")
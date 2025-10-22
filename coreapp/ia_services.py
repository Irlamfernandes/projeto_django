from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def gerar_titulo_ia_gemini(descricao):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Baseado nesta descrição: '{descricao}', me diga o título mais provável do filme. Retorne apenas o título."
        )
        return response.text.strip()
    except Exception as e:
        print("Erro ao gerar título com Gemini:", e)
        return None

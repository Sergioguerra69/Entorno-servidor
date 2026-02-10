import os
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno
load_dotenv()

# Configurar cliente
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Probar la API
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Di hola en español"
    )
    print(" Respuesta exitosa:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
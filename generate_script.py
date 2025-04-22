import os
import google.generativeai as genai

# Configurar API de Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurar modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Generar guión
prompt = """
Escribe un guión breve (50-60 palabras) para un video de YouTube de 1 minuto sobre la belleza de la naturaleza. Usa un tono inspirador y en español latinoamericano. El guión debe ser claro, directo y adecuado para voz en off.
"""
response = model.generate_content(prompt)
script = response.text.strip()

# Guardar guión
with open("script.txt", "w") as f:
    f.write(script)

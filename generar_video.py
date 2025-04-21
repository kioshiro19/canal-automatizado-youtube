import os
import subprocess
import requests
import json
from TTS.api import TTS
import speech_recognition as sr
import pysrt

# Crear directorio temporal
os.makedirs("media", exist_ok=True)

# Paso 1: Generar guión con Hugging Face Inference API
def generar_guion(tema="curiosidades naturaleza", hf_token=os.getenv("HF_TOKEN")):
    try:
        url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {hf_token}"}
        prompt = f"Escribe un guión breve de 150 palabras en español sobre {tema} para un video de 1 minuto."
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 200, "num_return_sequences": 1}
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            guion = response.json()[0]["generated_text"].strip()
            return guion
        else:
            raise Exception(f"API error: {response.text}")
    except Exception as e:
        print(f"Error en guión: {e}")
        return "Este es un video sobre la naturaleza. Los bosques son hogar de miles de especies. Los ríos fluyen con vida. Cada día, la naturaleza nos enseña algo nuevo."

# Paso 2: Crear voz en off
def texto_a_voz(guion, archivo_salida="media/voz.wav"):
    try:
        tts = TTS(model_name="tts_models/es/css10/vits", progress_bar=True)
        tts.tts_to_file(text=guion, file_path=archivo_salida)
        return archivo_salida
    except Exception as e:
        print(f"Error en voz: {e}")
        # Fallback: Silencio
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "60", archivo_salida])
        return archivo_salida

# Paso 3: Descargar imágenes (Unsplash Source)
def descargar_imagenes(tema="nature", cantidad=3):
    imagenes = []
    for i in range(cantidad):
        url = f"https://source.unsplash.com/1920x1080/?{tema}&sig={i}"
        archivo = f"media/imagen_{i}.jpg"
        try:
            respuesta = requests.get(url, stream=True, timeout=10)
            if respuesta.status_code == 200:
                with open(archivo, "wb") as f:
                    f.write(respuesta.content)
                imagenes.append(archivo)
            else:
                raise Exception("Error al descargar")
        except Exception as e:
            print(f"Error en imagen {i}: {e}")
            # Fallback: Imagen negra

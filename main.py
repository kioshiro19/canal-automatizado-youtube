import requests
import os
from moviepy.editor import *
import random

# Función para obtener imágenes desde Pixabay
def obtener_imagenes():
    url = "https://pixabay.com/api/"
    api_key = "TU_API_KEY"  # Reemplaza con tu clave de API de Pixabay
    parametros = {
        "key": api_key,
        "q": "motivation",
        "image_type": "photo",
        "per_page": 5,
    }
    
    response = requests.get(url, params=parametros)
    data = response.json()
    return [hit["webformatURL"] for hit in data["hits"]]

# Función para crear un video con una imagen y un audio
def crear_video(imagen_url, audio_path):
    # Descargar imagen
    imagen = requests.get(imagen_url, stream=True).raw
    img = ImageClip(imagen).set_duration(10)  # Duración de 10 segundos por imagen
    
    # Agregar audio
    audio = AudioFileClip(audio_path)
    video = img.set_audio(audio)
    
    # Especificar el nombre del archivo de salida
    video.write_videofile("video_final.mp4", codec="libx264")

# Código principal
if __name__ == "__main__":
    imagenes = obtener_imagenes()
    imagen_aleatoria = random.choice(imagenes)  # Seleccionamos una imagen al azar
    crear_video(imagen_aleatoria, "audio.mp3")  # Usa tu archivo de audio



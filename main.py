import os
import requests
from gtts import gTTS
from PIL import Image
from moviepy.editor import *
from io import BytesIO

# Texto base (puede venir de IA luego)
texto = """
Los primeros días como padres pueden ser abrumadores. 
Es normal sentir miedo, ansiedad o inseguridad.
La ciencia demuestra que el contacto piel con piel ayuda al apego seguro.
"""
lineas = [line.strip() for line in texto.strip().split('\n') if line.strip()]

# Crear voz en off
tts = gTTS(text=texto, lang='es')
tts.save("audio.mp3")

# Descargar imágenes automáticamente desde Unsplash
def buscar_imagen(query, i):
    headers = {"Accept-Version": "v1"}
    params = {"query": query, "client_id": "TU_API_KEY_UNSPLASH", "orientation": "landscape"}
    response = requests.get("https://api.unsplash.com/photos/random", headers=headers, params=params)
    data = response.json()
    url_imagen = data["urls"]["regular"]
    img_data = requests.get(url_imagen).content
    with open(f"img{i}.jpg", "wb") as handler:
        handler.write(img_data)
    return f"img{i}.jpg"

imagenes = []
for idx, linea in enumerate(lineas):
    imagen_path = buscar_imagen(linea, idx)
    imagenes.append(imagen_path)

# Crear clips con subtítulos e imágenes
clips = []
duracion_por_linea = 5  # segundos por línea
for i, (linea, imagen_path) in enumerate(zip(lineas, imagenes)):
    img_clip = ImageClip(imagen_path).set_duration(duracion_por_linea).resize(height=720)
    txt_clip = TextClip(linea, fontsize=40, color='white', bg_color='black', method='caption', size=(img_clip.w, None))
    txt_clip = txt_clip.set_duration(duracion_por_linea).set_position(('center', 'bottom'))
    clip_final = CompositeVideoClip([img_clip, txt_clip])
    clips.append(clip_final)

video_final = concatenate_videoclips(clips)
audio_final = AudioFileClip("audio.mp3")
video_final = video_final.set_audio(audio_final)
video_final.write_videofile("output.mp4", fps=24)


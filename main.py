import requests
import os
from moviepy.editor import *
from gtts import gTTS

# Tu API Key de Pixabay (reemplázala con tu propia clave)
API_KEY = 'tu_api_key_pixabay'

# Definir la función para obtener imágenes desde la API de Pixabay
def obtener_imagenes(query, cantidad=5):
    url = f"https://pixabay.com/api/?key={API_KEY}&q={query}&image_type=photo&per_page={cantidad}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['totalHits'] > 0:
            imagenes = data['hits']
            urls = [imagen['webformatURL'] for imagen in imagenes]
            return urls
        else:
            print(f"No se encontraron imágenes para: {query}")
            return []
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return []

# Descargar las imágenes
def descargar_imagenes(urls, carpeta_destino="imagenes"):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    for i, url in enumerate(urls):
        img_data = requests.get(url).content
        with open(f"{carpeta_destino}/imagen_{i+1}.jpg", 'wb') as f:
            f.write(img_data)
        print(f"Imagen {i+1} descargada.")

# Generar el audio con GTTS (Google Text-to-Speech)
def generar_audio(texto, archivo_audio="audio.mp3"):
    tts = gTTS(texto, lang='es')
    tts.save(archivo_audio)
    print(f"Audio guardado como {archivo_audio}")

# Crear video con las imágenes y el audio
def crear_video(imagenes, audio_file="audio.mp3", output_file="video_generado.mp4"):
    clips = [ImageClip(imagen).set_duration(5) for imagen in imagenes]  # Duración de 5 segundos por imagen
    video = concatenate_videoclips(clips, method="compose")

    # Añadir el audio al video
    audio = AudioFileClip(audio_file)
    video = video.set_audio(audio)

    # Exportar el video
    video.write_videofile(output_file, fps=24)
    print(f"Video generado: {output_file}")

# Proceso principal
def crear_video_automático(query="parenting", cantidad_imagenes=5, texto_audio="Consejos para padres primerizos."):
    # Obtener las imágenes relacionadas con el tema
    imagenes_urls = obtener_imagenes(query, cantidad_imagenes)
    
    if imagenes_urls:
        # Descargar las imágenes
        descargar_imagenes(imagenes_urls)

        # Generar el audio con el texto proporcionado
        generar_audio(texto_audio)

        # Crear el video con las imágenes y el audio
        imagenes = [f"imagenes/imagen_{i+1}.jpg" for i in range(cantidad_imagenes)]
        crear_video(imagenes)

# Ejecutar el proceso
crear_video_automático(query="parenting", cantidad_imagenes=5, texto_audio="Consejos para padres primerizos. ¡Bienvenidos al canal!")


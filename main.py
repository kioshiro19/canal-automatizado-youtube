import requests
import os
import subprocess
from PIL import Image
import time

# 1. Función para descargar imágenes de Pixabay
def obtener_imagenes(api_key, cantidad=5):
    url = f"https://pixabay.com/api/?key={api_key}&q=nature&image_type=photo&per_page={cantidad}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        imagenes_urls = [hit["webformatURL"] for hit in data["hits"]]
        
        # Guardar las imágenes en local
        imagenes = []
        for i, url in enumerate(imagenes_urls):
            img_data = requests.get(url).content
            img_path = f"imagen_{i+1}.jpg"
            with open(img_path, "wb") as img_file:
                img_file.write(img_data)
            imagenes.append(img_path)
        
        return imagenes
    else:
        print("Error al obtener imágenes.")
        return []

# 2. Función para redimensionar las imágenes
def redimensionar_imagen(imagen_path, tamaño=(1920, 1080)):
    with Image.open(imagen_path) as img:
        img = img.resize(tamaño)  # Redimensionar imagen
        img.save(imagen_path)  # Guardar la imagen redimensionada

# 3. Función para generar el video con las imágenes descargadas
def generar_video(imagenes, archivo_salida, duracion_imagen=2):
    imagenes_str = '|'.join(imagenes)  # Crear string de imágenes
    comando = f"ffmpeg -y -t {duracion_imagen * len(imagenes)} -framerate 1 -pattern_type glob -i '{imagenes_str}' -c:v libx264 -r 30 -pix_fmt yuv420p {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)

# 4. Función para agregar el audio al video
def agregar_audio(video, audio, archivo_salida):
    comando = f"ffmpeg -i {video} -i {audio} -c:v copy -c:a aac -strict experimental {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)

# 5. Función principal
def main():
    api_key = "tu_api_key_de_pixabay"
    cantidad_imagenes = 5  # Número de imágenes a descargar
    audio_path = "audio.mp3"  # Ruta al archivo de audio

    # 1. Descargar imágenes
    imagenes = obtener_imagenes(api_key, cantidad_imagenes)
    if not imagenes:
        print("No se pudieron obtener las imágenes.")
        return
    
    # 2. Redimensionar imágenes
    for imagen in imagenes:
        redimensionar_imagen(imagen)

    # 3. Crear el video con las imágenes
    video_salida = "video_salida.mp4"
    generar_video(imagenes, video_salida)

    # 4. Agregar audio al video
    if os.path.exists(audio_path):
        video_con_audio = "video_con_audio.mp4"
        agregar_audio(video_salida, audio_path, video_con_audio)
        print(f"Video generado correctamente con audio: {video_con_audio}")
    else:
        print(f"Audio no encontrado en la ruta: {audio_path}")
    
    # Eliminar imágenes temporales
    for imagen in imagenes:
        os.remove(imagen)
        
    print("Proceso completado.")

if __name__ == "__main__":
    main()


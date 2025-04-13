import requests
from PIL import Image
from io import BytesIO
import os
import subprocess

# Crear carpeta temporal para imágenes
os.makedirs("imagenes", exist_ok=True)

# Puedes cambiar esta lista por tu propia API si tienes una
urls = [
    "https://picsum.photos/640/360?random=1",
    "https://picsum.photos/640/360?random=2",
    "https://picsum.photos/640/360?random=3"
]

# Descargar imágenes
for i, url in enumerate(urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_path = f"imagenes/img{i:03d}.png"
        img.save(img_path)
        print(f"Imagen guardada: {img_path}")
    else:
        print(f"Fallo al descargar: {url}")

# Crear lista de imágenes en txt para FFmpeg
with open("imagenes/list.txt", "w") as f:
    for i in range(len(urls)):
        f.write(f"file 'img{i:03d}.png'\n")
        f.write("duration 2\n")  # cada imagen 2 segundos
    f.write(f"file 'img{len(urls)-1:03d}.png'\n")  # última para cerrar

# Crear video desde imágenes
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", "imagenes/list.txt",
    "-vsync", "vfr", "-pix_fmt", "yuv420p",
    "video_sin_audio.mp4"
], check=True)

# Descargar audio de ejemplo (libre)
audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
audio_path = "audio.mp3"
audio_res = requests.get(audio_url)
with open(audio_path, "wb") as f:
    f.write(audio_res.content)

# Unir video + audio
subprocess.run([
    "ffmpeg", "-y", "-i", "video_sin_audio.mp4", "-i", audio_path,
    "-c:v", "copy", "-c:a", "aac", "-shortest", "video_salida.mp4"
], check=True)

print("✅ Video generado exitosamente: video_salida.mp4")


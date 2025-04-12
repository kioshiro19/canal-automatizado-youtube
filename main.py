from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import subprocess
import os

# 1. Generar el audio con gTTS
text = "Hola, este es un video de prueba generado automáticamente."
tts = gTTS(text, lang='es')
audio_filename = "audio.mp3"
tts.save(audio_filename)

# 2. Crear la imagen con texto usando Pillow
img = Image.new('RGB', (1280, 720), color=(0, 0, 0))
d = ImageDraw.Draw(img)
font = ImageFont.load_default()  # Usa una fuente por defecto
d.text((10, 10), text, fill=(255, 255, 255), font=font)

# Guardar la imagen
image_filename = "image.png"
img.save(image_filename)

# 3. Crear el video combinando la imagen y el audio usando FFmpeg
video_filename = "output.mp4"
subprocess.run(['ffmpeg', '-loop', '1', '-framerate', '1', '-t', '20', '-i', image_filename, '-i', audio_filename, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_filename])

# Limpiar archivos temporales
os.remove(audio_filename)
os.remove(image_filename)

print(f"Video generado: {video_filename}")

import subprocess
from gtts import gTTS
import os

# Paso 1: Generar la voz en off
texto = "Bienvenidos a este canal de apoyo para padres primerizos. Hoy hablaremos sobre cómo manejar el estrés en los primeros meses de paternidad."

# Crear el archivo de audio con la voz generada
tts = gTTS(texto, lang='es')
audio_filename = "audio.mp3"
tts.save(audio_filename)

# Paso 2: Crear el video usando ffmpeg
image_filename = "fondo.jpg"  # Imagen de fondo
video_filename = "output.mp4"  # Nombre del archivo de salida

# Comando para crear el video con la voz en off
subprocess.run([
    'ffmpeg', '-loop', '1', '-framerate', '1', '-t', '20', '-i', image_filename,
    '-i', audio_filename, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_filename
])

# Verificar si el video fue generado correctamente
if os.path.exists(video_filename):
    print(f"Video generado correctamente: {video_filename}")
else:
    print("Error: No se pudo generar el video.")

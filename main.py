from gtts import gTTS
from moviepy.editor import *
import subprocess

# Datos para el video (ajustalos a tu caso)
image_filename = 'fondo.jpg'
audio_filename = 'audio.mp3'  # Asegúrate de tener este archivo de audio disponible
video_filename = 'output.mp4'

# Crear el audio con voz en off (ejemplo)
tts = gTTS("Bienvenidos a este video de ayuda para padres primerizos", lang='es')
tts.save(audio_filename)

# Crear el video con la imagen de fondo y la voz en off
subprocess.run(['ffmpeg', '-loop', '1', '-framerate', '1', '-t', '20', '-i', image_filename, '-i', audio_filename, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', video_filename])


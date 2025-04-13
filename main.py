import subprocess
import requests
from gtts import gTTS
from PIL import Image
from io import BytesIO

# Texto generado por IA
texto = "¿Sabías que los bebés reconocen la voz de su madre desde el útero?"

# 1. Generar voz
tts = gTTS(texto, lang='es')
audio_filename = "audio.mp3"
tts.save(audio_filename)

# 2. Obtener duración del audio
result = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", audio_filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
duration = float(result.stdout)

# 3. Crear subtítulos
subtitles = f"""1
00:00:00,000 --> 00:00:05,000
{texto}
"""
with open("subtitulos.srt", "w", encoding="utf-8") as f:
    f.write(subtitles)

# 4. Buscar imagen relacionada usando Lexica.art
busqueda = texto.split("que")[-1].strip()  # Ej: "los bebés reconocen la voz de su madre desde el útero"
query = busqueda.replace(" ", "%20")
response = requests.get(f"https://lexica.art/api/v1/search?q={query}")

data = response.json()
if data['images']:
    image_url = data['images'][0]['src']
else:
    image_url = "https://via.placeholder.com/1280x720.png?text=No+imagen+encontrada"

# 5. Descargar y guardar imagen
img_data = requests.get(image_url).content
with open('fondo.jpg', 'wb') as handler:
    handler.write(img_data)

# 6. Ensamblar video
video_filename = "output.mp4"
subprocess.run([
    'ffmpeg', '-loop', '1', '-framerate', '1', '-t', str(duration), '-i', 'fondo.jpg',
    '-i', audio_filename, '-vf',
    "subtitles=subtitulos.srt:force_style='FontSize=26,OutlineColour=&H80000000&,BorderStyle=1,Outline=2'",
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', video_filename
])

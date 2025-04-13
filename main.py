import subprocess
from gtts import gTTS

# Texto de prueba
texto = "¿Sabías que los primeros años de vida marcan el desarrollo emocional de tu hijo?"

# Guardar audio
tts = gTTS(texto, lang='es')
audio_filename = "audio.mp3"
tts.save(audio_filename)

# Obtener duración del audio
result = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", audio_filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
duration = float(result.stdout)
print(f"Duración del audio: {duration:.2f} segundos")

# Crear archivo de subtítulos (formato .srt)
subtitles = """1
00:00:00,000 --> 00:00:05,000
¿Sabías que los primeros años de vida marcan el desarrollo emocional de tu hijo?
"""

with open("subtitulos.srt", "w", encoding="utf-8") as f:
    f.write(subtitles)

# Ensamblar video con ffmpeg
image_filename = "fondo.jpg"
video_filename = "output.mp4"

# Comando para generar video con subtítulos
subprocess.run([
    'ffmpeg', '-loop', '1', '-framerate', '1', '-t', str(duration), '-i', image_filename,
    '-i', audio_filename, '-vf', "subtitles=subtitulos.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,BorderStyle=1,Outline=2'",
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', video_filename
])

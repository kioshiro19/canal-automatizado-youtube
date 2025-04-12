import os
from gtts import gTTS
import subprocess

# 1. Generar guion con g4f
import g4f

respuesta = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{
        "role": "user",
        "content": "Escribe un guion de 20 minutos sobre cómo un padre primerizo puede manejar el estrés, con base científica y recomendaciones psicológicas."
    }]
)

guion = respuesta
with open("guion.txt", "w", encoding="utf-8") as f:
    f.write(guion)

# 2. Crear voz en off
tts = gTTS(text=guion, lang='es')
tts.save("voz.mp3")

# 3. Crear subtítulos básicos
lines = guion.split(". ")
with open("subtitulos.srt", "w", encoding="utf-8") as srt:
    for i, line in enumerate(lines):
        start = f"00:{i//6:02d}:{(i%6)*10:02d},000"
        end = f"00:{i//6:02d}:{(i%6)*10+9:02d},000"
        srt.write(f"{i+1}\n{start} --> {end}\n{line.strip()}.\n\n")

# 4. Generar video con ffmpeg
subprocess.run([
    "ffmpeg", "-loop", "1", "-i", "fondo.jpg",
    "-i", "voz.mp3", "-vf", "subtitles=subtitulos.srt",
    "-t", "1200", "-c:v", "libx264", "-c:a", "aac",
    "-shortest", "output.mp4"
])


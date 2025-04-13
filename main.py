import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
import moviepy.editor as mp

# Texto del video
texto = "Ser padre primerizo puede ser abrumador. Pero con amor, paciencia y guía, todo es posible."

# Descargar imagen desde Unsplash automáticamente
tema = "padres primerizos"
url = f"https://source.unsplash.com/1600x900/?{tema.replace(' ', '%20')}"
response = requests.get(url)
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    img.save("fondo.jpg")
    print("✅ Imagen descargada.")
else:
    print("❌ No se pudo descargar la imagen.")
    exit()

# Generar voz en off
tts = gTTS(text=texto, lang='es')
tts.save("voz.mp3")

# Crear video
clip = mp.ImageClip("fondo.jpg", duration=15)
audio = mp.AudioFileClip("voz.mp3")
clip = clip.set_audio(audio)

# Agregar subtítulos
txt_clip = mp.TextClip(texto, fontsize=24, color='white', bg_color='black', size=clip.size)
txt_clip = txt_clip.set_duration(clip.duration).set_position(('center', 'bottom'))

# Composición final
final = mp.CompositeVideoClip([clip, txt_clip])
final.write_videofile("output.mp4", fps=24)

from moviepy.editor import *
from gtts import gTTS

# El texto para el TTS (text-to-speech)
text = "Hola, este es un video de prueba generado automáticamente."

# Genera el audio usando gTTS
tts = gTTS(text, lang='es')
tts.save("audio.mp3")

# Crea un fondo de color negro para el video
clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=20)

# Crea un clip con el texto que aparece en el video
txt_clip = TextClip(text, fontsize=50, color='white')
txt_clip = txt_clip.set_position('center').set_duration(20)

# Agrega el audio al video
audio_background = AudioFileClip("audio.mp3")

# Combina los clips de video y audio
final_clip = CompositeVideoClip([clip, txt_clip])
final_clip = final_clip.set_audio(audio_background)

# Guarda el video final
final_clip.write_videofile("output.mp4", fps=24)

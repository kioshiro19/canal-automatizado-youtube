from moviepy.editor import *
from gtts import gTTS

text = "Hola, este es un video de prueba generado automáticamente."

tts = gTTS(text, lang='es')
tts.save("audio.mp3")

clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=20)

txt_clip = TextClip(text, fontsize=50, color='white')
txt_clip = txt_clip.set_position('center').set_duration(20)

audio_background = AudioFileClip("audio.mp3")

final_clip = CompositeVideoClip([clip, txt_clip])
final_clip = final_clip.set_audio(audio_background)

final_clip.write_videofile("output.mp4", fps=24)


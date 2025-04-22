from gtts import gTTS

# Leer guión
with open("script.txt", "r") as f:
    texto = f.read()

# Generar voz en off
tts = gTTS(text=texto, lang='es', tld='com.mx') # Acento mexicano
tts.save("audio.mp3")

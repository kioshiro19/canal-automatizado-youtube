from gtts import gTTS

# Leer guión
try:
    with open("script.txt", "r") as f:
        texto = f.read()
except FileNotFoundError:
    texto = "Error: No se encontró el guión. Usando texto de respaldo."
    print("Error: script.txt no encontrado")

# Generar voz en off
tts = gTTS(text=texto, lang='es', tld='com.mx')
tts.save("audio.mp3")

import whisper

# Cargar modelo Whisper
model = whisper.load_model("base")

# Transcribir audio
try:
    result = model.transcribe("audio.mp3")
except FileNotFoundError:
    print("Error: audio.mp3 no encontrado")
    with open("subtitulos.srt", "w") as f:
        f.write("1\n00:00:00.000 --> 00:00:01.000\nError: No se encontró audio.\n")
    exit(1)

# Guardar subtítulos en SRT
with open("subtitulos.srt", "w") as f:
    for i, segment in enumerate(result["segments"]):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        f.write(f"{i+1}\n{start:00.3f} --> {end:00.3f}\n{text}\n\n")

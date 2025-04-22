import whisper

# Cargar modelo Whisper
model = whisper.load_model("base")

# Transcribir audio
result = model.transcribe("audio.mp3")

# Guardar subtítulos en SRT
with open("subtitulos.srt", "w") as f:
    for i, segment in enumerate(result["segments"]):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        f.write(f"{i+1}\n{start:00.3f} --> {end:00.3f}\n{text}\n\n")

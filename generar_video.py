import os
import subprocess
import requests
import json
from gtts import gTTS
import speech_recognition as sr
import pysrt

# Crear directorio temporal
os.makedirs("media", exist_ok=True)

# Paso 1: Generar guión con Hugging Face Inference API
def generar_guion(tema="curiosidades naturaleza", hf_token=os.getenv("sk-9faea39633094b6295cc9682482afb1f")):
    print("Paso 1: Generando guión...")
    try:
        if not hf_token:
            raise Exception("HF_TOKEN no configurado")
        url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {hf_token}"}
        prompt = f"Escribe un guión breve de 150 palabras en español sobre {tema} para un video de 1 minuto."
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 200, "num_return_sequences": 1}
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            guion = response.json()[0]["generated_text"].strip()
            print(f"Guión generado: {guion[:50]}...")
            with open("media/guion.txt", "w") as f:
                f.write(guion)
            print(f"Guión guardado: media/guion.txt, tamaño: {os.path.getsize('media/guion.txt')} bytes")
            return guion
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error en guión: {e}")
        guion = "Este es un video sobre la naturaleza. Los bosques son hogar de miles de especies. Los ríos fluyen con vida. Cada día, la naturaleza nos enseña algo nuevo."
        with open("media/guion.txt", "w") as f:
            f.write(guion)
        print(f"Guión fallback guardado: media/guion.txt, tamaño: {os.path.getsize('media/guion.txt')} bytes")
        return guion

# Paso 2: Crear voz en off con gTTS
def texto_a_voz(guion, archivo_salida="media/voz.wav"):
    print("Paso 2: Generando voz...")
    try:
        tts = gTTS(text=guion, lang='es')
        temp_mp3 = "media/temp_voz.mp3"
        tts.save(temp_mp3)
        if not os.path.exists(temp_mp3):
            raise Exception("No se generó el archivo MP3")
        print(f"MP3 generado: {temp_mp3}, tamaño: {os.path.getsize(temp_mp3)} bytes")
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", temp_mp3, archivo_salida],
            check=True, capture_output=True, text=True
        )
        print(f"FFmpeg voz output: {result.stderr}")
        if not os.path.exists(archivo_salida):
            raise Exception("No se generó el archivo WAV")
        print(f"Voz generada: {archivo_salida}, tamaño: {os.path.getsize(archivo_salida)} bytes")
        return archivo_salida
    except Exception as e:
        print(f"Error en voz: {e}")
        # Fallback: Silencio
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "60", archivo_salida],
            capture_output=True, text=True
        )
        print(f"FFmpeg voz fallback output: {result.stderr}")
        print(f"Voz fallback generada: {archivo_salida}, tamaño: {os.path.getsize(archivo_salida)} bytes")
        return archivo_salida

# Paso 3: Descargar una imagen (Unsplash Source)
def descargar_imagen(tema="nature"):
    print("Paso 3: Descargando una imagen...")
    url = f"https://source.unsplash.com/1920x1080/?{tema}"
    archivo = "media/imagen.jpg"
    try:
        respuesta = requests.get(url, stream=True, timeout=10)
        print(f"Unsplash status code: {respuesta.status_code}")
        if respuesta.status_code == 200:
            with open(archivo, "wb") as f:
                f.write(respuesta.content)
            if not os.path.exists(archivo):
                raise Exception("Imagen no guardada")
            print(f"Imagen descargada: {archivo}, tamaño: {os.path.getsize(archivo)} bytes")
            return archivo
        else:
            raise Exception(f"Error al descargar, status: {respuesta.status_code}")
    except Exception as e:
        print(f"Error en imagen: {e}")
        # Fallback: Imagen negra
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=60", "-c:v", "libx264", archivo],
            capture_output=True, text=True
        )
        print(f"FFmpeg imagen fallback output: {result.stderr}")
        print(f"Imagen fallback generada: {archivo}, tamaño: {os.path.getsize(archivo)} bytes")
        return archivo

# Paso 4: Obtener música
def obtener_musica():
    print("Paso 4: Obteniendo música...")
    url = "https://cdn.pixabay.com/audio/2023/01/23/audio_0e3e4f7e65.mp3"
    archivo = "media/musica.mp3"
    try:
        respuesta = requests.get(url, stream=True, timeout=10)
        print(f"Pixabay status code: {respuesta.status_code}")
        if respuesta.status_code == 200:
            with open(archivo, "wb") as f:
                f.write(respuesta.content)
            if not os.path.exists(archivo):
                raise Exception("Música no guardada")
            print(f"Música descargada: {archivo}, tamaño: {os.path.getsize(archivo)} bytes")
            return archivo
        else:
            raise Exception(f"Error al descargar música, status: {respuesta.status_code}")
    except Exception as e:
        print(f"Error en música: {e}")
        # Fallback: Silencio
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "60", archivo],
            capture_output=True, text=True
        )
        print(f"FFmpeg música fallback output: {result.stderr}")
        print(f"Música fallback generada: {archivo}, tamaño: {os.path.getsize(archivo)} bytes")
        return archivo

# Paso 5: Generar subtítulos con Whisper
def generar_subtitulos(audio, salida="media/subtitulos.srt"):
    print("Paso 5: Generando subtítulos...")
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            texto = recognizer.recognize_whisper(audio_data, model="tiny")
        # Subtítulos simplificados
        palabras = texto.split()
        subtitulos = []
        for i in range(0, len(palabras), 5):
            start = i * 0.5
            end = min((i + 5) * 0.5, 60)
            subtitulos.append(pysrt.SubRipItem(
                index=len(subtitulos) + 1,
                start=pysrt.SubRipTime(seconds=start),
                end=pysrt.SubRipTime(seconds=end),
                text=" ".join(palabras[i:i+5])
            ))
        pysrt.SubRipFile(subtitulos).save(salida)
        if not os.path.exists(salida):
            raise Exception("Subtítulos no generados")
        print(f"Subtítulos generados: {salida}, tamaño: {os.path.getsize(salida)} bytes")
        return salida
    except Exception as e:
        print(f"Error en subtítulos: {e}")
        # Fallback: Subtítulos vacíos
        with open(salida, "w") as f:
            f.write("1\n00:00:00,000 --> 00:01:00,000\nSin subtítulos disponibles\n")
        print(f"Subtítulos fallback generados: {salida}, tamaño: {os.path.getsize(salida)} bytes")
        return salida

# Paso 6: Crear video
def crear_video(imagen, voz, musica, subtitulos, salida="media/video_final.mp4"):
    print("Paso 6: Creando video...")
    try:
        # Verificar que los archivos de entrada existan
        if not os.path.exists(imagen):
            raise Exception(f"Imagen no encontrada: {imagen}")
        if not os.path.exists(voz):
            raise Exception("Archivo de voz no encontrado")
        if not os.path.exists(musica):
            raise Exception("Archivo de música no encontrado")
        if not os.path.exists(subtitulos):
            raise Exception("Archivo de subtítulos no encontrado")

        # Crear video con una imagen estática, voz, música y subtítulos
        comando = [
            "ffmpeg", "-y", "-loop", "1", "-i", imagen, "-i", voz, "-i", musica,
            "-vf", f"subtitles={subtitulos},format=yuv420p",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", "-t", "60", salida
        ]
        result = subprocess.run(comando, check=True, capture_output=True, text=True)
        print(f"FFmpeg video output: {result.stderr}")
        if not os.path.exists(salida):
            raise Exception("Video final no generado")
        print(f"Video final generado: {salida}, tamaño: {os.path.getsize(salida)} bytes")
        return salida
    except Exception as e:
        print(f"Error en creación de video: {e}")
        # Fallback: Video mínimo
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=60", "-c:v", "libx264", salida],
            capture_output=True, text=True
        )
        print(f"FFmpeg video fallback output: {result.stderr}")
        print(f"Video fallback generado: {salida}, tamaño: {os.path.getsize(salida)} bytes")
        return salida

# Flujo principal
def main():
    try:
        tema = "nature"
        guion = generar_guion(tema)
        voz = texto_a_voz(guion)
        imagen = descargar_imagen(tema)
        musica = obtener_musica()
        subtitulos = generar_subtitulos(voz)
        video_final = crear_video(imagen, voz, musica, subtitulos)
        print(f"Proceso completado: {video_final}, tamaño: {os.path.getsize(video_final)} bytes")
    except Exception as e:
        print(f"Error en flujo principal: {e}")
        raise

if __name__ == "__main__":
    main()

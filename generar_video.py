import os
import subprocess
import requests
import json
from gtts import gTTS

# Crear directorio temporal
os.makedirs("media", exist_ok=True)

# Paso 1: Generar guión con Hugging Face Inference API
def generar_guion(tema="curiosidades naturaleza", hf_token=os.getenv("HF_TOKEN")):
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
            return guion
        else:
            raise Exception(f"API error: {response.text}")
    except Exception as e:
        print(f"Error en guión: {e}")
        return "Este es un video sobre la naturaleza. Los bosques son hogar de miles de especies. Los ríos fluyen con vida. Cada día, la naturaleza nos enseña algo nuevo."

# Paso 2: Crear voz en off con gTTS
def texto_a_voz(guion, archivo_salida="media/voz.wav"):
    print("Paso 2: Generando voz...")
    try:
        tts = gTTS(text=guion, lang='es')
        temp_mp3 = "media/temp_voz.mp3"
        tts.save(temp_mp3)
        if not os.path.exists(temp_mp3):
            raise Exception("No se generó el archivo MP3")
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", temp_mp3, archivo_salida],
            check=True, capture_output=True, text=True
        )
        print(f"FFmpeg voz output: {result.stderr}")
        if not os.path.exists(archivo_salida):
            raise Exception("No se generó el archivo WAV")
        print("Voz generada con éxito.")
        return archivo_salida
    except Exception as e:
        print(f"Error en voz: {e}")
        # Fallback: Silencio
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "60", archivo_salida],
            capture_output=True, text=True
        )
        return archivo_salida

# Paso 3: Descargar imágenes (Unsplash Source)
def descargar_imagenes(tema="nature", cantidad=3):
    print("Paso 3: Descargando imágenes...")
    imagenes = []
    for i in range(cantidad):
        url = f"https://source.unsplash.com/1920x1080/?{tema}&sig={i}"
        archivo = f"media/imagen_{i}.jpg"
        try:
            respuesta = requests.get(url, stream=True, timeout=10)
            if respuesta.status_code == 200:
                with open(archivo, "wb") as f:
                    f.write(respuesta.content)
                if not os.path.exists(archivo):
                    raise Exception(f"Imagen {i} no guardada")
                imagenes.append(archivo)
                print(f"Imagen {i} descargada.")
            else:
                raise Exception("Error al descargar")
        except Exception as e:
            print(f"Error en imagen {i}: {e}")
            # Fallback: Imagen negra
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=20", "-c:v", "libx264", archivo],
                capture_output=True, text=True
            )
            imagenes.append(archivo)
    return imagenes

# Paso 4: Obtener música
def obtener_musica():
    print("Paso 4: Obteniendo música...")
    url = "https://cdn.pixabay.com/audio/2023/01/23/audio_0e3e4f7e65.mp3"
    archivo = "media/musica.mp3"
    try:
        respuesta = requests.get(url, stream=True, timeout=10)
        if respuesta.status_code == 200:
            with open(archivo, "wb") as f:
                f.write(respuesta.content)
            if not os.path.exists(archivo):
                raise Exception("Música no guardada")
            print("Música descargada.")
            return archivo
        else:
            raise Exception("Error al descargar música")
    except Exception as e:
        print(f"Error en música: {e}")
        # Fallback: Silencio
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-t", "60", archivo],
            capture_output=True, text=True
        )
        return archivo

# Paso 5: Crear video
def crear_video(imagenes, voz, musica, salida="media/video_final.mp4"):
    print("Paso 5: Creando video...")
    try:
        # Verificar que los archivos de entrada existan
        for img in imagenes:
            if not os.path.exists(img):
                raise Exception(f"Imagen no encontrada: {img}")
        if not os.path.exists(voz):
            raise Exception("Archivo de voz no encontrado")
        if not os.path.exists(musica):
            raise Exception("Archivo de música no encontrado")

        # Crear archivo de entrada para imágenes
        with open("media/imagenes.txt", "w") as f:
            for img in imagenes:
                f.write(f"file '{img}'\n")
                f.write("duration 20\n")  # 20 segundos por imagen

        # Combinar imágenes, voz y música
        comando = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", "media/imagenes.txt",
            "-i", voz, "-i", musica,
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest", "-pix_fmt", "yuv420p",
            salida
        ]
        result = subprocess.run(comando, check=True, capture_output=True, text=True)
        print(f"FFmpeg video output: {result.stderr}")
        if not os.path.exists(salida):
            raise Exception("Video final no generado")
        print(f"Video final generado: {salida}")
        return salida
    except Exception as e:
        print(f"Error en creación de video: {e}")
        # Fallback: Video mínimo
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=1920x1080:d=60", "-c:v", "libx264", salida],
            capture_output=True, text=True
        )
        return salida

# Flujo principal
def main():
    try:
        tema = "nature"
        guion = generar_guion(tema)
        voz = texto_a_voz(guion)
        imagenes = descargar_imagenes(tema)
        musica = obtener_musica()
        video_final = crear_video(imagenes, voz, musica)
        print(f"Proceso completado: {video_final}")
    except Exception as e:
        print(f"Error en flujo principal: {e}")
        raise

if __name__ == "__main__":
    main()

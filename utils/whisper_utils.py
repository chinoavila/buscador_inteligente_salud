"""
Utilidades para transcripción de audio.
"""
import dotenv
import os
from openai import OpenAI
import io

# Cargar variables de entorno
dotenv.load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio_with_whisper(audio_bytes):
    """
    Convierte bytes de audio a archivo temporal y los transcribe con Whisper.

    :param audio_bytes: Bytes con los datos de audio a transcribir
    :return: Texto obtenido en la transcripción
    """
    audio_file = io.BytesIO(audio_bytes) # Crea un archivo temporal
    audio_file.name = "audio.wav" # Debe tener nombre y extensión
    
    try:
        # Llamar a la API para la transcripcion
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        # La API devuelve un objeto por lo que se debe devolver "text"
        return transcript.text
    except Exception as e:
        raise Exception(f"Error en transcripción con Whisper: {str(e)}")

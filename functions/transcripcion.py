import dotenv
import os
from openai import OpenAI
import io
from utils import with_status_message

# tomar API Key de OPENAI desde archivo .env
dotenv.load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribir_audio(audio_bytes):
    """
    Convierte los bytes a un archivo de audio 
    y lo transcribe a texto utilizando el modelo Whisper de OpenAI
    :param audio_bytes: bytes de los datos de audio
    :return: El texto obtenido en la transcripción
    """
    audio_file = io.BytesIO(audio_bytes) # Crea un archivo temporal
    audio_file.name = "audio.wav" # Debe tener nombre y extensión
    # Llamar a la API para la transcripcion
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    # La API devuelve un objeto por lo que se debe devolver "text"
    return transcript.text

@with_status_message("Transcribiendo audio...")
def transcribir_con_status(audio_bytes):
    return transcribir_audio(audio_bytes)
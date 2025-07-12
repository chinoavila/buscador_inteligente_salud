import dotenv
import os
import openai
import io

# tomar API Key de OPENAI desde archivo .env
dotenv.load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    # La API devuelve un objeto por lo que se debe devolver "text"
    return transcript["text"]
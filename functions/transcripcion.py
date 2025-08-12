from utils import transcribe_audio_with_whisper
from application.ui import with_status_message

def transcribir_audio(audio_bytes):
    """
    Convierte los bytes a un archivo de audio y los transcribe a texto con Whisper.

    :param audio_bytes: Bytes con los datos del audio a transcribir
    :return: Texto obtenido en la transcripción o mensaje de error
    """
    try:
        return transcribe_audio_with_whisper(audio_bytes)
    except Exception as e:
        print(f"[DEBUG TRANSCRIPCION] Error: {str(e)}")
        return f"Error en transcripción: {str(e)}"

@with_status_message("Transcribiendo audio...")
def transcribir_con_status(audio_bytes):
    """
    Transcribe audio mostrando un mensaje de estado durante el proceso.

    :param audio_bytes: Bytes con los datos del audio a transcribir
    :return: Texto obtenido en la transcripción o mensaje de error
    """
    return transcribir_audio(audio_bytes)
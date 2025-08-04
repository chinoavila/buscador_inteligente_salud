import os
import sys
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils import show_instructions
from functions import (
    transcribir_con_status,
    detectar_entidades_con_status,
    consultar_rag_con_status
)

# Configuración específica para Hugging Face Spaces
if "HF_TOKEN" in os.environ:
    os.environ["HUGGINGFACE_API_TOKEN"] = os.environ["HF_TOKEN"]

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Buscador Inteligente de Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    MAX_SEGUNDOS = 60

    if st.button("Ayuda"):
        show_instructions(MAX_SEGUNDOS)

    st.title("Buscador Inteligente de Profesionales de Salud")

    audio_bytes = audio_recorder(
            text="",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="5x",
            energy_threshold=(-1.0, 1.0),
            pause_threshold=float(MAX_SEGUNDOS),
        )
    
    if audio_bytes:
        # Transcripción de audio
        transcripcion = transcribir_con_status(audio_bytes)

        if transcripcion:
            st.header("Transcripción:")
            st.write(transcripcion)

            ## Extracción de entidades médicas
            entidades_medicas = detectar_entidades_con_status(transcripcion)

            if entidades_medicas:
                ## Consulta con RAG
                respuesta_rag = consultar_rag_con_status(entidades_medicas)
                if respuesta_rag:
                    st.header("Contactos de Profesionales Encontrados:")
                    st.markdown(respuesta_rag)
                else:
                    st.error("No se pudieron encontrar profesionales para las especialidades consultadas.")    
            else:
                st.error("No fue posible identificar entidades médicas en la transcripción.")

        else:
            st.error("No se pudo transcribir el audio.")

if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)
    main()
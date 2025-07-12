import os
import sys
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from utils import (
    transcribir_con_status,
    detectar_entidades_con_status,
    show_instructions
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

            ## Extracción de sintomas
            entidades_medicas = detectar_entidades_con_status(transcripcion)

            if entidades_medicas:
                st.header("Entidades médicas detectadas:")
                st.write(entidades_medicas)
            else:
                st.error("No fue posible identificar entidades médicas.")

        else:
            st.error("No se pudo transcribir el audio.")

if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)
    main()
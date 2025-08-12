import os
import sys
import streamlit as st
from application.orchestration import HealthOrchestrator
from application.config import APP_CONFIG, CUSTOM_CSS
from application.ui import (
    show_instructions,
    create_text_input,
    create_audio_input,
    create_styled_radio_input,
    display_results,
    create_search_button
)

# Configuración específica para Hugging Face Spaces
if "HF_TOKEN" in os.environ:
    os.environ["HUGGINGFACE_API_TOKEN"] = os.environ["HF_TOKEN"]

# Configuración de página de Streamlit
st.set_page_config(
    page_title=APP_CONFIG["titulo"],
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS de la aplicación
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def main():
    """
    Inicializa la aplicación Streamlit y gestiona el flujo principal de UI.

    :return: None
    """
    MAX_SEGUNDOS = APP_CONFIG["max_segundos_audio"]

    # Inicializar el orquestador
    orchestrator = HealthOrchestrator()

    # Título principal
    st.markdown(f'<h1 class="main-title">🏥 {APP_CONFIG["titulo"]}</h1>', unsafe_allow_html=True)
    
    # Botón de ayuda discreto
    if st.button("ℹ️ Ayuda", help="Cómo usar la aplicación"):
        show_instructions(MAX_SEGUNDOS)
    
    # Método de entrada simple
    input_method = create_styled_radio_input()

    if input_method == "✍️ Escribir":
        # Usar el componente de UI para entrada de texto
        sintomas_texto = create_text_input()
        
        if create_search_button(sintomas_texto):
            if sintomas_texto.strip():
                procesar_sintomas(sintomas_texto.strip(), orchestrator)
        
    else:  # Grabación de audio
        # Usar el componente de UI para entrada de audio
        audio_bytes = create_audio_input()
        
        if audio_bytes:
            procesar_audio(audio_bytes, orchestrator)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer minimalista
    st.markdown("""
    <div class="footer">
        <p>⚠️ Esta herramienta es informativa. No reemplaza la consulta médica profesional.</p>
    </div>
    """, unsafe_allow_html=True)

def procesar_sintomas(texto_sintomas, orchestrator):
    """
    Procesa síntomas escritos usando el orquestador y muestra los resultados.

    :param texto_sintomas: Texto con la descripción de los síntomas del usuario
    :param orchestrator: Instancia de HealthOrchestrator para ejecutar el flujo
    :return: None
    """
    with st.spinner("🔍 Analizando síntomas..."):
        result = orchestrator.process_text_symptoms(texto_sintomas)
        display_results(result)

def procesar_audio(audio_bytes, orchestrator):
    """
    Procesa una grabación de audio: transcribe, analiza y muestra recomendaciones.

    :param audio_bytes: Datos de audio en formato bytes
    :param orchestrator: Instancia de HealthOrchestrator para ejecutar el flujo
    :return: None
    """
    # 1) Transcribir y mostrar inmediatamente
    with st.spinner("🎧 Transcribiendo audio..."):
        transcription = orchestrator.transcribe_audio(audio_bytes)
    
    if transcription:
        st.markdown("**🗣️ Transcripción:**")
        st.markdown(f"*{transcription}*")
        st.divider()
    
    # 2) Continuar con el flujo completo para entidades y recomendaciones
    with st.spinner("🔍 Analizando y buscando prestadores..."):
        result = orchestrator.process_audio_symptoms(audio_bytes, pretranscription=transcription)
        # Ya mostramos la transcripción arriba; ocultarla en el bloque de resultados para no duplicar
        if transcription:
            result['transcription'] = None
        display_results(result)

if __name__ == "__main__":
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)
    main()
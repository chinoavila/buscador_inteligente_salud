import streamlit as st
from functools import wraps
from .config import APP_CONFIG, HELP_MESSAGES

def with_status_message(message):
    """
    Decorador para mostrar un mensaje de estado mientras se ejecuta una función.

    :param message: Mensaje a mostrar durante la ejecución
    :return: Función decorada que muestra el mensaje de estado
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            status_placeholder = st.empty()
            with status_placeholder.container():
                st.info(message)
                result = func(*args, **kwargs)
            status_placeholder.empty()
            return result
        return wrapper
    return decorator


@st.dialog("ℹ️ Cómo usar la aplicación")
def show_instructions(max_segundos):
    """
    Muestra un diálogo con instrucciones de uso de la aplicación.

    :param max_segundos: Tiempo máximo de grabación de audio permitido (segundos)
    :return: None
    """
    st.markdown("""
    ### 🎯 ¿Qué hace esta aplicación?
    Te ayuda a encontrar prestadores de salud especializados basándose en tus síntomas.
    
    ### ✍️ Escribir síntomas
    - Describe detalladamente lo que sientes
    - Incluye ubicación, intensidad y duración
    - Ejemplo: *"Dolor de cabeza intenso en el lado derecho con náuseas desde hace 2 días"*
    
    ### 🎤 Grabar audio
    - Presiona el micrófono para iniciar/detener
    - Habla claro y describe tus síntomas
    - Máximo **{} segundos** de grabación
    
    ### ⚠️ Importante
    Esta herramienta es solo informativa y no reemplaza la consulta médica profesional.
    Siempre consulta con un profesional de la salud para un diagnóstico adecuado.
    """.format(max_segundos))


def create_symptom_input_section():
    """
    Crea la sección de entrada de síntomas con validación.

    :return: Método de entrada seleccionado
    """
    st.markdown("### 📝 Describe tus síntomas")
    
    # Selector de método de entrada con estilos personalizados
    input_method = create_styled_radio_input()
    
    return input_method


def create_styled_radio_input():
    """
    Crea botones estilizados que funcionan como radio buttons con el tema de la aplicación.

    :return: Método de entrada seleccionado
    """
    st.markdown("**Seleccione cómo describir sus síntomas:**")
    
    # Inicializar el estado si no existe
    if 'input_method' not in st.session_state:
        st.session_state.input_method = "✍️ Escribir"
    
    # Crear dos columnas para los botones
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        escribir_selected = st.session_state.input_method == "✍️ Escribir"
        if st.button(
            "✍️ Escribir", 
            key="btn_escribir",
            use_container_width=True,
            type="primary" if escribir_selected else "secondary"
        ):
            st.session_state.input_method = "✍️ Escribir"
            st.rerun()
    
    with col2:
        audio_selected = st.session_state.input_method == "🎤 Grabar audio"
        if st.button(
            "🎤 Grabar audio", 
            key="btn_audio",
            use_container_width=True,
            type="primary" if audio_selected else "secondary"
        ):
            st.session_state.input_method = "🎤 Grabar audio"
            st.rerun()
    
    return st.session_state.input_method


def create_text_input():
    """
    Crea el área de texto para entrada de síntomas.

    :return: Texto de síntomas ingresado por el usuario
    """
    st.markdown("**Describe tus síntomas con detalle**")
    sintomas_texto = st.text_area(
        "Síntomas",
        placeholder=HELP_MESSAGES["sintomas_texto"]["placeholder"],
        height=120,
        max_chars=APP_CONFIG["max_caracteres_texto"],
        label_visibility="collapsed"
    )
    
    st.markdown(
        '<p class="help-text">💡 Tip: Incluye ubicación, intensidad y duración para mejores resultados</p>', 
        unsafe_allow_html=True
    )
    
    return sintomas_texto


def create_audio_input():
    """
    Crea la interfaz de grabación de audio.

    :return: Datos de audio grabados en bytes o None
    """
    from audio_recorder_streamlit import audio_recorder
    
    st.markdown("**Graba tus síntomas**")
    st.markdown(
        '<p class="help-text">🎤 Presiona el micrófono y describe claramente tus síntomas</p>', 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="audio-container">', unsafe_allow_html=True)
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e8b62c",
        neutral_color="#2E8B57",
        icon_name="microphone",
        icon_size="4x",
        energy_threshold=(-1.0, 1.0),
        pause_threshold=float(APP_CONFIG["max_segundos_audio"]),
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    return audio_bytes


def display_results(result_data):
    """
    Muestra los resultados del procesamiento de síntomas.

    :param result_data: Diccionario con los datos del resultado del procesamiento
    :return: None
    """
    if result_data.get('success'):
        # Mostrar transcripción si existe
        if result_data.get('transcription'):
            st.markdown("**🗣️ Transcripción:**")
            st.markdown(f"*{result_data['transcription']}*")
            st.divider()
        
        # Mostrar recomendaciones
        if result_data.get('recommendations'):
            st.markdown("### 🎯 Prestadores recomendados")
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result_data['recommendations'])
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Botón para nueva búsqueda
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Nueva búsqueda", type="secondary", use_container_width=True):
                st.rerun()
    else:
        # Mostrar error
        error_message = result_data.get('error_message', 'Error desconocido')
        st.error(f"❌ {error_message}")
        
        # Sugerencias basadas en el tipo de error
        if "específicos" in error_message.lower():
            st.info("💡 **Sugerencia:** Intenta ser más específico sobre:")
            st.markdown("""
            - Ubicación exacta del dolor o molestia
            - Intensidad (leve, moderado, intenso)
            - Duración (desde cuándo comenzó)
            - Síntomas acompañantes
            """)
        elif "transcribir" in error_message.lower():
            st.info("💡 **Sugerencia:** Para mejorar la transcripción:")
            st.markdown("""
            - Habla más claro y despacio
            - Acércate al micrófono
            - Evita ruidos de fondo
            - Verifica que el micrófono funcione
            """)


def create_search_button(text_symptoms=None, disabled=False):
    """
    Crea el botón de búsqueda con validación.

    :param text_symptoms: Texto de síntomas para validar (opcional)
    :param disabled: Indica si el botón debe estar deshabilitado
    :return: True si el botón fue presionado y la entrada es válida
    """
    if text_symptoms is not None:
        # Validar longitud mínima usando configuración
        min_length = APP_CONFIG["min_caracteres_texto"]
        is_valid = text_symptoms and len(text_symptoms.strip()) >= min_length
        disabled = disabled or not is_valid
        
        if not is_valid and text_symptoms:
            st.warning(f"⚠️ La descripción debe tener al menos {min_length} caracteres")
    
    return st.button(
        "🔍 Buscar prestadores", 
        type="primary", 
        disabled=disabled,
        use_container_width=True,
        help="Buscar prestadores especializados basándose en los síntomas descritos"
    )

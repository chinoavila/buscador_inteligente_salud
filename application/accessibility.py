import streamlit as st
import re

def create_accessible_button(label, key=None, 
                           type="secondary", disabled=False, 
                           help_text=None):
    """
    Crea un botón accesible con texto de ayuda opcional.

    :param label: Texto del botón
    :param key: Clave única para el botón (opcional)
    :param type: Tipo de botón ("primary", "secondary")
    :param disabled: Indica si el botón está deshabilitado
    :param help_text: Texto de ayuda para accesibilidad (opcional)
    :return: True si el botón fue presionado
    """
    if help_text:
        st.help(help_text)
    
    return st.button(
        label, 
        key=key, 
        type=type, 
        disabled=disabled,
        help=help_text
    )


def create_progress_indicator(step, total_steps, 
                            current_action=""):
    """
    Crea un indicador de progreso accesible.

    :param step: Paso actual
    :param total_steps: Total de pasos
    :param current_action: Descripción de la acción actual (opcional)
    :return: None
    """
    progress_percentage = step / total_steps
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress_percentage)
    with col2:
        st.write(f"{step}/{total_steps}")
    
    if current_action:
        st.write(f"**Paso actual:** {current_action}")


def create_status_message(message_type, title, content, 
                         show_icon=True):
    """
    Crea mensajes de estado accesibles con iconos.

    :param message_type: Tipo de mensaje ("success", "error", "warning", "info", "processing")
    :param title: Título del mensaje
    :param content: Contenido del mensaje
    :param show_icon: Indica si se muestra el icono correspondiente
    :return: None
    """
    icons = {
        "success": "✅",
        "error": "❌", 
        "warning": "⚠️",
        "info": "ℹ️",
        "processing": "⏳"
    }
    
    icon = icons.get(message_type, "ℹ️") if show_icon else ""
    formatted_message = f"{icon} **{title}**\n\n{content}"
    
    if message_type == "success":
        st.success(formatted_message)
    elif message_type == "error":
        st.error(formatted_message)
    elif message_type == "warning":
        st.warning(formatted_message)
    elif message_type == "processing":
        st.info(formatted_message)
    else:
        st.info(formatted_message)


def create_expandable_section(title, content, 
                            expanded=False):
    """
    Crea una sección expandible accesible.

    :param title: Título de la sección
    :param content: Contenido de la sección
    :param expanded: Indica si la sección debe estar expandida por defecto
    :return: None
    """
    with st.expander(title, expanded=expanded):
        st.markdown(content)


def create_input_validation_feedback(input_value, 
                                   validation_rules):
    """
    Proporciona retroalimentación de validación para entradas de usuario.

    :param input_value: Valor de entrada a validar
    :param validation_rules: Lista de reglas de validación. Cada regla debe tener
                             {"type": str, "value": Any, "message": str}
    :return: True si la entrada es válida
    """
    feedback = []
    is_valid = True
    
    for rule in validation_rules:
        rule_type = rule.get("type")
        rule_value = rule.get("value")
        rule_message = rule.get("message")
        
        if rule_type == "min_length" and len(input_value) < rule_value:
            feedback.append(f"❌ {rule_message}")
            is_valid = False
        elif rule_type == "max_length" and len(input_value) > rule_value:
            feedback.append(f"❌ {rule_message}")
            is_valid = False
        elif rule_type == "required" and not input_value.strip():
            feedback.append(f"❌ {rule_message}")
            is_valid = False
        elif rule_type == "pattern" and not re.search(rule_value, input_value):
            feedback.append(f"❌ {rule_message}")
            is_valid = False
    
    # Mostrar feedback
    if feedback:
        for msg in feedback:
            st.write(msg)
    elif input_value.strip():
        st.write("✅ Entrada válida")
    
    return is_valid


def create_keyboard_shortcuts_help():
    """
    Muestra atajos de teclado disponibles para mejorar la navegación.

    :return: None
    """
    with st.expander("⌨️ Atajos de teclado"):
        st.markdown("""
        ### Navegación básica
        - **Tab**: Navegar hacia adelante entre elementos
        - **Shift + Tab**: Navegar hacia atrás entre elementos
        - **Enter**: Activar botones seleccionados
        - **Espacio**: Seleccionar opciones de radio/checkbox
        
        ### Controles de página
        - **Escape**: Cerrar diálogos y ventanas modales
        - **Ctrl + R** (Windows) / **Cmd + R** (Mac): Recargar página
        - **F5**: Actualizar página
        
        ### Accesibilidad
        - **Ctrl + (+/-)**: Aumentar/disminuir zoom
        - **Ctrl + 0**: Restablecer zoom
        """)


def create_accessibility_settings():
    """
    Crea un panel de configuración de accesibilidad en la barra lateral.

    :return: Diccionario con configuraciones de accesibilidad seleccionadas
    """
    with st.sidebar:
        st.markdown("### ♿ Configuración de Accesibilidad")
        
        # Configuración de tamaño de texto
        font_size = st.selectbox(
            "Tamaño de texto:",
            ["Normal", "Grande", "Muy grande"],
            help="Ajusta el tamaño del texto para mejor legibilidad"
        )
        
        # Configuración de contraste
        high_contrast = st.checkbox(
            "Alto contraste",
            help="Mejora la visibilidad para usuarios con problemas de visión"
        )
        
        # Configuración de animaciones
        reduce_motion = st.checkbox(
            "Reducir animaciones",
            help="Reduce las animaciones para usuarios sensibles al movimiento"
        )
        
        # Configuración de sonidos
        enable_sound_feedback = st.checkbox(
            "Retroalimentación de sonido",
            help="Habilita sonidos para acciones importantes"
        )
        
        # Configuración de modo de lectura
        reading_mode = st.checkbox(
            "Modo de lectura",
            help="Optimiza la interfaz para lectores de pantalla"
        )
        
        return {
            "font_size": font_size,
            "high_contrast": high_contrast,
            "reduce_motion": reduce_motion,
            "enable_sound_feedback": enable_sound_feedback,
            "reading_mode": reading_mode
        }


def apply_accessibility_styles(settings):
    """
    Aplica estilos CSS basados en las configuraciones de accesibilidad.

    :param settings: Configuraciones de accesibilidad
    :return: None
    """
    styles = []
    
    # Tamaño de texto
    if settings.get("font_size") == "Grande":
        styles.append("html { font-size: 18px; }")
    elif settings.get("font_size") == "Muy grande":
        styles.append("html { font-size: 22px; }")
    
    # Alto contraste
    if settings.get("high_contrast"):
        styles.append("""
        .stApp {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        .stButton > button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }
        """)
    
    # Reducir animaciones
    if settings.get("reduce_motion"):
        styles.append("""
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        """)
    
    # Aplicar estilos
    if styles:
        st.markdown(f"<style>{''.join(styles)}</style>", unsafe_allow_html=True)


def create_screen_reader_announcement(message):
    """
    Crea un anuncio para lectores de pantalla.

    :param message: Mensaje a anunciar
    :return: None
    """
    st.markdown(
        f'<div aria-live="polite" aria-atomic="true" class="sr-only">{message}</div>',
        unsafe_allow_html=True
    )


def create_skip_navigation_link():
    """
    Crea un enlace de salto de navegación para accesibilidad.

    :return: None
    """
    st.markdown("""
    <style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000000;
        color: #FFFFFF;
        padding: 8px;
        text-decoration: none;
        z-index: 1000;
    }
    .skip-link:focus {
        top: 6px;
    }
    </style>
    <a href="#main-content" class="skip-link">Saltar al contenido principal</a>
    """, unsafe_allow_html=True)

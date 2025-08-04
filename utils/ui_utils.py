import streamlit as st
from functools import wraps

def with_status_message(message):
    """
    Decorador para mostrar un mensaje de estado mientras se ejecuta una función.
    :param message: Mensaje a mostrar durante la ejecución
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

@st.dialog("Instrucciones")
def show_instructions(max_segundos):
    texto_instrucciones = f"""
        Presione el ícono del micrófono para iniciar la grabación.\n
        Cuando el micrófono esté de color amarillo, indique sus sintomas.\n
        Puede detener la grabación presionando nuevamente el ícono del micrófono.\n
        Pasados {str(max_segundos)} segundos, la grabación se detendrá automáticamente.
        """
    st.write(texto_instrucciones)
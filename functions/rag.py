from utils import query_contacts_with_langchain
from application.ui import with_status_message
from utils.rag_utils import get_health_service

# Inicialización de RAG al cargar el módulo (solo una vez al inicio de la app)
get_health_service()

def consultar_rag(text):
    """
    Realiza una consulta al sistema RAG para obtener prestadores de salud.

    :param text: Texto o JSON con la(s) especialidad(es) a buscar
    :return: Respuesta formateada con la lista de contactos o mensaje de error
    """
    try:
        print(f"[DEBUG RAG] Input recibido: {text}")
        result = query_contacts_with_langchain(text)
        print(f"[DEBUG RAG] Resultado: {result[:200]}...")
        return result
    except Exception as e:
        print(f"[DEBUG RAG] Error: {str(e)}")
        return f"Error en consulta RAG: {str(e)}"
    
@with_status_message("Buscando contactos de prestadores...")
def consultar_rag_con_status(entidades_medicas):
    """
    Consulta el sistema RAG mostrando un mensaje de estado durante el proceso.

    :param entidades_medicas: Texto o JSON con especialidades médicas a buscar
    :return: Respuesta formateada con la lista de contactos o mensaje de error
    """
    return consultar_rag(entidades_medicas)
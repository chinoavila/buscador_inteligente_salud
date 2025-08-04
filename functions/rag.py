from utils.rag_utils import query_contacts_with_langchain, with_status_message

def consultar_rag(text):
    """
    Realizar consulta al sistema RAG
    :param text: Texto/JSON con especialidades a buscar
    :return: Respuesta con lista de contactos
    """
    try:
        return query_contacts_with_langchain(text)  
    except Exception as e:
        return f"Error en consulta RAG: {str(e)}"
    
@with_status_message("Consultando contactos de profesionales...")
def consultar_rag_con_status(entidades_medicas):
    return consultar_rag(entidades_medicas)
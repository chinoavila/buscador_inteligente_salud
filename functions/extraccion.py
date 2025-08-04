
from utils import generate_with_hugging_face, extract_entities_with_spacy, with_status_message
    
def detectar_entidades_medicas(texto):
    """
    Extrae las entidades detectadas en el texto de la transcripción
    y las clasifica segun tipo de especialidad medica
    :param text: El texto obtenido en la transcripción
    :return: Especialidad asociada a los sintomas detectados
    """
    # Buscar casos de estos sintomas con modelo de Hugging Face
    busqueda_resultados = generate_with_hugging_face(texto, "es", "en")
    # Extraer entidades con NER de spaCy
    entidades = extract_entities_with_spacy(busqueda_resultados)
    # Clasificar entidades con modelo de Hugging Face
    clasificacion_resultados = generate_with_hugging_face(entidades, "en", "es")
    return clasificacion_resultados

@with_status_message("Detectando entidades médicas...")
def detectar_entidades_con_status(transcripcion):
    return detectar_entidades_medicas(transcripcion)
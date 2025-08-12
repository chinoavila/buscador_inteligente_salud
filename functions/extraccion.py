
from utils import generate_with_hugging_face, extract_entities_with_spacy
from application.ui import with_status_message
    
def detectar_entidades_medicas(texto):
    """
    Extrae las entidades detectadas en el texto de la transcripción y
    las clasifica según la(s) especialidad(es) médica(s) asociada(s).

    :param texto: Texto obtenido de la transcripción o ingresado por el usuario
    :return: Descripción en español de la(s) especialidad(es) médica(s) detectada(s)
    """
    print(f"[DEBUG EXTRACCION] Input texto: {texto}")
    
    # Buscar casos de estos sintomas con modelo de Hugging Face
    busqueda_resultados = generate_with_hugging_face(texto, "es", "en")
    print(f"[DEBUG EXTRACCION] Resultado HF (es->en): {busqueda_resultados}")
    
    # Extraer entidades con NER de spaCy
    entidades = extract_entities_with_spacy(busqueda_resultados)
    print(f"[DEBUG EXTRACCION] Entidades spaCy: {entidades}")
    
    # Clasificar entidades con modelo de Hugging Face
    clasificacion_resultados = generate_with_hugging_face(entidades, "en", "es")
    print(f"[DEBUG EXTRACCION] Resultado final (en->es): {clasificacion_resultados}")
    
    return clasificacion_resultados

@with_status_message("Detectando entidades médicas...")
def detectar_entidades_con_status(transcripcion):
    """
    Detecta entidades médicas mostrando un mensaje de estado durante el proceso.

    :param transcripcion: Texto de entrada sobre el cual se identificarán entidades médicas
    :return: Descripción en español de la(s) especialidad(es) médica(s) detectada(s)
    """
    return detectar_entidades_medicas(transcripcion)
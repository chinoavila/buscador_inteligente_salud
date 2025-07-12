
from utils import generate_with_hugging_face, extract_entities_with_spacy
    
def detectar_entidades_medicas(texto):
    """
    Extrae las entidades detectadas en el texto de la transcripción
    y las clasifica segun tipo de especialidad medica
    :param text: El texto obtenido en la transcripción
    :return: Especialidad asociada a los sintomas detectados
    """
    # Formateo del texto de entrada
    prompt = f"Los sintomas \"{texto}\" ¿a que especialidad médica corresponden?"

    # Fine-tunning
    input_text = f'''<bos>
    <start_of_turn>system
    You are a helpful AI assistant.
    Eres un agente experto en medicina.
    Responde de la forma más acotada posible.
    No respondas con un diagnóstico.
    Tu respuesta siempre debe tener este formato:
    Sintomatología: <sintomas>.
    Especialidad sugerida: <especialidad>.
    <end_of_turn>
    <start_of_turn>user {prompt}<end_of_turn>
    <start_of_turn>model
    '''

    # Clasificar sintomas con modelo de Hugging Face
    clasificacion = generate_with_hugging_face(input_text)

    # Extraer entidades con NER de spaCy
    entidades = extract_entities_with_spacy(clasificacion)

    return entidades

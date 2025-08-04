import spacy
from .cache_utils import (
    save_model_to_cache, 
    load_model_from_cache, 
    is_model_cached
)

def load_model():
    """Cargar modelo NER de scispacy con caché optimizado"""
    model_id = "en_core_sci_sm"
    
    # Intentar cargar desde caché primero
    if is_model_cached(model_id):
        print(f"Cargando modelo spaCy {model_id} desde caché...")
        cached_data = load_model_from_cache(model_id)
        if cached_data and 'model' in cached_data:
            print(f"Modelo spaCy {model_id} cargado exitosamente desde caché")
            return cached_data['model']
    else:
        # Si no está en caché, cargar desde spaCy
        print(f"📥 Cargando modelo spaCy {model_id}...")
        model = spacy.load(model_id)
    
    # Guardar en caché para futuras cargas
    try:
        model_data = {'model': model}
        save_model_to_cache(model_id, model_data)
        print(f"Modelo spaCy {model_id} guardado en caché")
    except Exception as e:
        print(f"No se pudo guardar el modelo spaCy en caché: {e}")
    
    return model

ner_nlp = load_model()

def extract_entities_with_spacy(input_text):
    """Extrae entidades con información detallada"""
    doc = ner_nlp(input_text)
    entidades = ""
    for entity in doc.ents:
        entidades += entity.text + ", "
    if entidades == "":
        respuesta = "No se detectaron síntomas claros."
    else:
        respuesta = entidades[:-2]
    return respuesta
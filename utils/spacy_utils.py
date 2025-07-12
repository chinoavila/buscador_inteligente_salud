import spacy

# Cargar modelo NER de spaCy en español
ner_nlp = spacy.load("es_core_news_sm")

def extract_entities_with_spacy(input_text):
    doc = ner_nlp(input_text)
    entidades = [(entity.text, entity.label_) for entity in doc.ents]
    if entidades:
        if len(entidades):
            respuesta = " ".join(entidades)
    else: 
        respuesta = "No se detectaron síntomas claros."
    return respuesta
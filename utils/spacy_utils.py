import spacy
import streamlit as st

@st.cache_resource
def load_model():
    """Cargar modelo NER de scispacy"""
    model = spacy.load("en_core_sci_sm")
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
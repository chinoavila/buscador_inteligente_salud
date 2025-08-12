import spacy
import streamlit as st
import warnings

# Silenciar FutureWarning específico de spaCy
warnings.filterwarnings(
    "ignore",
    message=".*Possible set union.*",
    category=FutureWarning,
    module="spacy"
)

@st.cache_resource
def load_model():
    """
    Carga el modelo NER de SciSpaCy utilizado para extracción de entidades.

    :return: Modelo spaCy listo para procesar texto
    """
    model = spacy.load("en_core_sci_sm")
    return model

ner_nlp = load_model()

def extract_entities_with_spacy(input_text):
    """
    Extrae entidades nombradas del texto usando el modelo NER cargado.

    :param input_text: Texto de entrada del cual extraer entidades
    :return: Cadena con las entidades detectadas separadas por coma o mensaje si no hay
    """
    doc = ner_nlp(input_text)
    entidades = ""
    for entity in doc.ents:
        entidades += entity.text + ", "
    if entidades == "":
        respuesta = "No se detectaron síntomas claros."
    else:
        respuesta = entidades[:-2]
    return respuesta
"""
Módulo de utilidades varias
"""
from .hf_utils import generate_with_hugging_face
from .spacy_utils import extract_entities_with_spacy
from .ui_utils import (
    transcribir_con_status,
    detectar_entidades_con_status,
    show_instructions
)
__all__ = [
    'transcribir_con_status',
    'detectar_entidades_con_status',
    'show_instructions',
    'generate_with_hugging_face',
    'extract_entities_with_spacy'
]
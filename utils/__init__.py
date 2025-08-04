"""
Módulo de utilidades varias
"""
from .hf_utils import generate_with_hugging_face
from .spacy_utils import extract_entities_with_spacy
from .rag_utils import query_contacts_with_langchain
from .ui_utils import with_status_message, show_instructions
from .cache_utils import (
    save_model_to_cache, 
    load_model_from_cache, 
    is_model_cached, 
    clear_model_cache
)

__all__ = [
    'with_status_message',
    'show_instructions',
    'generate_with_hugging_face',
    'extract_entities_with_spacy',
    'query_contacts_with_langchain',
    'save_model_to_cache',
    'load_model_from_cache',
    'is_model_cached',
    'clear_model_cache'
]
"""
Módulo de utilidades varias
"""
from .hf_utils import generate_with_hugging_face
from .spacy_utils import extract_entities_with_spacy
from .rag_utils import query_contacts_with_langchain
from .whisper_utils import transcribe_audio_with_whisper

__all__ = [
    'generate_with_hugging_face',
    'extract_entities_with_spacy',
    'query_contacts_with_langchain',
    'transcribe_audio_with_whisper'
]
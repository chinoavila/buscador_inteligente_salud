"""
Módulo de funciones para el procesamiento de audio sintomatologico
"""
from .transcripcion import transcribir_audio
from .extraccion import detectar_entidades_medicas

__all__ = [
    'transcribir_audio',
    'detectar_entidades_medicas'
]
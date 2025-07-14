#!/bin/bash
# Pre-setup script for Hugging Face Spaces

# Descargar modelo de spaCy si no existe
python -m spacy download es_core_news_sm

# Verificar que todas las dependencias estén instaladas
pip install --upgrade pip
pip install -r requirements.txt

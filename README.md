# 🏥 Buscador Inteligente de Prestadores de Salud

## 📋 Descripción del Proyecto

### El Problema
En Argentina, existe una gran fragmentación en el sistema de salud que dificulta a los ciudadanos encontrar la atención médica apropiada. Los pacientes a menudo no saben qué especialidad médica necesitan según sus síntomas, y la búsqueda de prestadores adecuados puede ser compleja y consume tiempo valioso, ya sea por recorridos presenciales visitando cada establecimiento, o una búsqueda en internet. Estas últimas, pueden realizarse mediante buscadores básicos y populares como Google o mediante los sitios oficiales de instituciones de salud, lo cual obliga al usuario a tener que comprender sus interfaces antes de poder utilizarlos de manera fluida.

### La Solución Propuesta
Se desarrolló una aplicación web que utiliza **Inteligencia Artificial Avanzada** para:
- **Entrada dual**: Voz (transcripción automática) o texto directo
- **Análisis inteligente**: Extracción de entidades médicas con modelos especializados
- **Búsqueda semántica**: Sistema RAG con LangChain y ChromaDB
- **Recomendaciones personalizadas**: Prestadores basados en análisis de síntomas
- **Fuentes de datos adaptables**: La base de datos permite integrar prestadores de cualquier origen para adaptar el alcance de las recomendaciones.

## 🛠️ Stack Tecnológico Completo

| Categoría | Tecnología | Versión | Propósito |
|-----------|------------|---------|-----------|
| **Backend** | Python | 3.10+ | Lenguaje principal |
| **Frontend** | Streamlit | 1.28+ | Interfaz web responsiva |
| **Audio** | audio-recorder-streamlit | 0.0.10 | Captura de audio |
| **Transcripción** | OpenAI Whisper API | 1.0+ | Conversión voz-texto |
| **NLP Básico** | spaCy | 3.7+ | Procesamiento de lenguaje |
| **NLP Biomédico** | SciSpaCy | 0.5.4 | Análisis médico especializado |
| **ML Models** | Hugging Face Transformers | 4.30+ | Modelos biomédicos |
| **RAG Framework** | LangChain | 0.3.27 | IA conversacional |
| **Vector DB** | ChromaDB | 0.5+ | Búsqueda semántica |
| **Deploy** | Docker Compose | 2.0+ | Orquestación de servicios |

## 🚀 Inicio Rápido

```bash
# Instalación con Docker (Recomendado)
git clone https://github.com/chinoavila/buscador_inteligente_salud
cd buscador_inteligente_salud
cp .env.example .env
# Editar .env con tus API keys
docker-compose up --build -d
```

**🌐 Aplicación disponible en:** `http://localhost:8501`

### API Keys Requeridas
- **OpenAI API**: Para transcripción con Whisper ([obtener aquí](https://platform.openai.com))
- **Hugging Face**: Opcional para modelos avanzados ([obtener aquí](https://huggingface.co))

## 📚 Documentación Completa

Para información detallada sobre instalación, configuración y uso, consulta nuestra documentación especializada:

- **[📖 Guía de Instalación Detallada](docs/instalacion-detallada.md)** - Instrucciones paso a paso para todos los entornos
- **[🎮 Guía de Uso Completa](docs/guia-de-uso.md)** - Cómo utilizar todas las funcionalidades
- **[⚙️ Documentación Técnica](docs/documentacion-tecnica.md)** - Arquitectura, APIs y desarrollo
- **[🚨 Solución de Problemas](docs/solucion-problemas.md)** - Resolución de errores comunes

## ⚠️ Importante - Uso Académico

>Proyecto desarrollado para la **Maestría en Tecnologías de la Información (UNNE/UNaM)** - Asignatura "Inteligencia Artificial". 
Este sistema **NO proporciona diagnósticos médicos**, solo sugerencias orientativas. 
Las inferencias son generadas por modelos de IA y **no sustituyen el consejo médico profesional**. 
Siempre consulte con un profesional de la salud calificado.

# Buscador Inteligente de Profesionales de Salud

Una aplicación web desarrollada en Streamlit que utiliza inteligencia artificial para transcribir consultas médicas por voz, extraer entidades médicas y sugerir especialidades apropiadas.

## 🎯 Características Principales

- **Grabación de Audio**: Interfaz minimalista para grabar consultas médicas por voz (hasta 60 segundos)
- **Transcripción Automática**: Utiliza el modelo Whisper de OpenAI para convertir audio a texto
- **Extracción de Entidades Médicas**: Detecta síntomas y entidades médicas usando:
  - spaCy con modelo en español (`es_core_news_sm`)
  - Modelos de Hugging Face para análisis especializado
- **Sugerencia de Especialidades**: Recomienda especialidades médicas basadas en los síntomas detectados
- **Base de Datos de Establecimientos**: Incluye datasets de centros de salud públicos y privados

## 🗂️ Estructura del Proyecto

```
ENTREGA/
├── app.py                    # Aplicación principal de Streamlit
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Documentación del proyecto
├── comandos_instalacion.txt  # Comandos de instalación rápida
├── env/                     # Entorno virtual de Python
├── functions/               # Módulos de funcionalidades
│   ├── transcripcion.py     # Transcripción de audio con OpenAI Whisper
│   ├── extraccion.py        # Extracción de entidades médicas
│   └── rag.py              # Lógica de RAG (Retrieval-Augmented Generation)
├── utils/                   # Utilidades del proyecto
│   ├── hf_utils.py         # Integración con Hugging Face
│   ├── spacy_utils.py      # Procesamiento NLP con spaCy
│   └── ui_utils.py         # Utilidades de interfaz de usuario
└── datasets/               # Datasets de establecimientos de salud
    ├── dataset_ejemplo_1752219625571.xlsx
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de OpenAI con API Key activa
- Micrófono funcional en el sistema

### Instalación Paso a Paso

1. **Clona el repositorio** (o descarga los archivos):
   ```bash
   git clone <repository-url>
   cd ENTREGA
   ```

2. **Crea un entorno virtual**:
   ```bash
   python -m venv env
   ```

3. **Activa el entorno virtual**:
   ```bash
   # Windows
   env\Scripts\activate
   
   # Linux/Mac
   source env/bin/activate
   ```

4. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configura las variables de entorno**:
   Crea un archivo `.env` en el directorio raíz con las credenciales de OpenAI y Hugging Face:
   ```
   OPENAI_API_KEY=tu_api_key_aqui
   HF_TOKEN=tu_access_token_aqui
   ```

6. **Ejecuta la aplicación**:
   ```bash
   streamlit run app.py
   ```

## 🎮 Uso de la Aplicación

1. **Inicia la aplicación** y accede a `http://localhost:8501`
2. **Presiona el botón de ayuda** para ver las instrucciones detalladas
3. **Graba tu consulta médica** usando el botón del micrófono (máximo 60 segundos)
4. **Revisa la transcripción** generada automáticamente
5. **Analiza las entidades médicas** detectadas en tu consulta
6. **Obtén sugerencias** de especialidades médicas relevantes

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Transcripción**: OpenAI Whisper API
- **ML**: Hugging Face Transformers, PyTorch
- **NLP**: spaCy (`es_core_news_sm`)
- **Audio**: audio-recorder-streamlit
- **Datos**: Pandas, Excel

## 📦 Dependencias Principales

- `streamlit>=1.28.0` - Framework web para la interfaz
- `audio-recorder-streamlit==0.0.10` - Componente de grabación de audio
- `openai==0.28` - API de OpenAI para transcripción
- `transformers==4.46.3` - Modelos de Hugging Face
- `torch==2.7.1` - Framework de machine learning
- `spacy==3.8.7` - Procesamiento de lenguaje natural

## ⚙️ Configuración Avanzada

### Parámetros Modificables

- **Duración máxima de grabación**: Modificar `MAX_SEGUNDOS` en `app.py` (por defecto 60 segundos)
- **Modelos de ML**: Cambiar modelos en `utils/hf_utils.py`
- **Configuración de spaCy**: Ajustar en `utils/spacy_utils.py`

### Variables de Entorno

Crea un archivo `.env` con las siguientes variables:
```
OPENAI_API_KEY=tu_api_key_de_openai
HF_TOKEN=tu_token_de_hugging_face (opcional)
```

## 🚨 Resolución de Problemas

### Errores Comunes

1. **Error de credenciales**: Verifica que tu archivo `.env` contenga credenciales válidas
2. **Error de modelo spaCy**: Ejecuta `python -m spacy download es_core_news_sm`
3. **Error de micrófono**: Verifica que tu navegador tenga permisos de micrófono
4. **Error de dependencias**: Reinstala con `pip install -r requirements.txt --upgrade`

## 📄 Licencia

**MIT License**

Copyright (c) 2025 - Proyecto Académico de Maestría en TI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**Aviso Importante**: Este proyecto fue desarrollado con fines académicos como parte de la Maestría en Tecnologías de la Información con enfoque en Inteligencia Artificial. No debe utilizarse como sustituto del consejo médico profesional. No proporciona diagnósticos médicos, solo sugerencias de especialidades y todas las inferencias son obtenidas a través de los modelos de Hugging Face y spaCy.

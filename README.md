---
title: Buscador Inteligente de Profesionales de Salud
emoji: 🏥
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
python_version: 3.10.12
---

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
buscador_inteligente_salud/
├── app.py                    # Aplicación principal de Streamlit
├── requirements.txt          # Dependencias del proyecto
├── README.md                # Documentación del proyecto
├── Dockerfile               # Configuración para contenedor Docker
├── docker-compose.yml       # Orquestación de servicios Docker
├── .dockerignore           # Archivos excluidos del contexto Docker
├── .env.example            # Template de variables de entorno
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
- Cuenta de Hugging Face con Access Token activo
- Micrófono funcional en el sistema
- Docker y Docker Compose (para despliegue con contenedores)

### Opción 1: Instalación Local (Desarrollo)

1. **Clona el repositorio** (o descarga los archivos):
   ```bash
   git clone https://github.com/chinoavila/buscador_inteligente_salud
   cd buscador_inteligente_salud
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
   STREAMLIT_PORT=8501
   ```

6. **Ejecuta la aplicación**:
   ```bash
   streamlit run app.py
   ```

### Opción 2: Despliegue con Docker (Recomendado para Producción)

#### Configuración

1. **Variables de entorno (opcional):**
   ```bash
   cp .env.example .env
   ```
   Edita el archivo `.env` y configura las variables necesarias.

#### Usando Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

#### Usando Docker directamente

```bash
# Construir la imagen
docker build -t buscador_inteligente_salud .

# Ejecutar el contenedor
docker run -p 8501:8501 \
  -v $(pwd)/datasets:/app/datasets \
  -e OPENAI_API_KEY=tu_api_key \
  -e HF_TOKEN=tu_token_de_hugging_face \
  buscador_inteligente_salud
```

#### Comandos útiles para Docker

```bash
# Ver contenedores ejecutándose
docker ps

# Acceder al shell del contenedor
docker exec -it buscador_inteligente_salud bash

# Ver logs en tiempo real
docker-compose logs -f buscador_inteligente_salud

# Reconstruir después de cambios
docker-compose up --build

# Limpiar todo (contenedores, imágenes, volúmenes)
docker-compose down -v
docker system prune -a
```

### Opción 3: Despliegue en Hugging Face Spaces 🤗

#### 📋 Pasos Detallados para Desplegar

##### 1. Preparar el Repositorio
1. Sube todos los archivos del proyecto a tu repositorio de GitHub
2. Asegúrate de que el archivo `README.md` contenga el encabezado YAML con la configuración de Hugging Face

##### 2. Crear el Space en Hugging Face
1. Ve a [Hugging Face Spaces](https://huggingface.co/spaces)
2. Haz clic en "Create new Space"
3. Completa la información:
   - **Space name**: `buscador-inteligente-salud`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU basic (gratuito)

##### 3. Configurar Variables de Entorno (Secrets)
En la configuración del Space, agrega las siguientes variables secretas:

```
OPENAI_API_KEY = "tu_openai_api_key_aqui"
HF_TOKEN = "tu_huggingface_token_aqui"
```

##### 4. Subir Archivos o Conectar GitHub
Puedes elegir entre:
- **Opción A**: Subir archivos directamente al repositorio del Space
- **Opción B**: Conectar tu repositorio de GitHub existente

##### 5. Verificar Archivos Necesarios
Asegúrate de que estos archivos estén presentes:

```
├── app.py                    # ✅ Archivo principal
├── requirements.txt          # ✅ Dependencias
├── README.md                # ✅ Con encabezado YAML
├── packages.txt             # ✅ Paquetes del sistema
├── setup.sh                # ✅ Script de configuración
├── .streamlit/
│   ├── config.toml          # ✅ Configuración de Streamlit
│   └── secrets.toml.example # ✅ Template para secretos
├── functions/               # ✅ Funciones del proyecto
├── utils/                   # ✅ Utilidades
└── datasets/               # ✅ Datos (opcional)
```

#### ⚙️ Configuración Automática

El proyecto incluye configuración automática para:
- **Puerto**: 7860 (estándar de Hugging Face)
- **Modelo spaCy**: Descarga automática de `es_core_news_sm`
- **Variables de entorno**: Manejo automático de tokens
- **Dependencias**: Instalación automática desde `requirements.txt`

#### 🔧 Resolución de Problemas Específicos de HF

##### Error de Modelo spaCy
Si hay problemas con el modelo de spaCy:
```bash
python -m spacy download es_core_news_sm
```

##### Error de Variables de Entorno
Verifica que las variables secretas estén configuradas correctamente en:
`Settings > Variables and secrets`

##### Error de Memoria
Si el espacio se queda sin memoria:
- Considera usar hardware con más RAM
- Optimiza el código para usar menos memoria

#### 🎯 URL del Space
Una vez desplegado, tu aplicación estará disponible en:
```
https://huggingface.co/spaces/tu-usuario/buscador-inteligente-salud
```

#### � Notas Importantes para Hugging Face
- El primer despliegue puede tardar varios minutos
- Hugging Face Spaces reinicia automáticamente si hay cambios
- Los logs están disponibles en la pestaña "Logs" del Space
- La aplicación se suspende después de inactividad y se reactiva automáticamente

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
- `openai>=1.0.0` - API de OpenAI para transcripción
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
HF_TOKEN=tu_token_de_hugging_face
STREAMLIT_PORT=8501
```

## 🚨 Resolución de Problemas

### Errores Comunes

1. **Error de credenciales**: Verifica que tu archivo `.env` contenga credenciales válidas
2. **Error de modelo spaCy**: Ejecuta `python -m spacy download es_core_news_sm`
3. **Error de micrófono**: Verifica que tu navegador tenga permisos de micrófono
4. **Error de dependencias**: Reinstala con `pip install -r requirements.txt --upgrade`

### Problemas específicos de Docker

#### Error de permisos (Linux/Mac)
```bash
# Asegurar permisos correctos
sudo chown -R $USER:$USER datasets/
```

#### Reconstruir imagen completamente
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Ver logs detallados
```bash
docker-compose logs --tail=100 buscador_inteligente_salud
```

### Archivos Docker incluidos

- `Dockerfile`: Define la imagen del contenedor
- `docker-compose.yml`: Orquesta los servicios
- `.dockerignore`: Archivos a excluir del contexto de build
- `.env.example`: Template de variables de entorno

### Volúmenes persistentes

El archivo `docker-compose.yml` está configurado para persistir:
- `/datasets`: Archivos de datos
- `/logs`: Archivos de log (si se crean)

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

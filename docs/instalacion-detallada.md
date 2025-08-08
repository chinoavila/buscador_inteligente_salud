# Guía de Instalación Detallada

Esta guía proporciona instrucciones paso a paso para instalar y configurar el Buscador Inteligente de Profesionales de Salud en diferentes entornos.

## 🔧 Prerrequisitos

### Requisitos del Sistema
- **Python**: 3.8 o superior (recomendado: 3.10)
- **RAM**: Mínimo 4GB (recomendado: 8GB para modelos de ML)
- **Espacio en disco**: Al menos 2GB libres
- **Micrófono**: Funcional en el sistema
- **Navegador**: Chrome, Firefox, Safari o Edge (con soporte de Web Audio API)

### Cuentas y API Keys Necesarias
1. **OpenAI**: Para transcripción con Whisper
   - Crear cuenta en [OpenAI](https://platform.openai.com)
   - Generar API Key en la sección "API Keys"
   - Asegurar créditos suficientes en la cuenta

2. **Hugging Face**: Para modelos de ML
   - Crear cuenta en [Hugging Face](https://huggingface.co)
   - Generar Access Token en "Settings > Access Tokens"
   - Token tipo "Read" es suficiente ("Write" para desplegar en HuggingFace Spaces)

## 🖥️ Instalación Local (Desarrollo)

### Paso 1: Clonar o Descargar el Proyecto
```bash
git clone https://github.com/chinoavila/buscador_inteligente_salud
cd buscador_inteligente_salud
```

### Paso 2: Crear Entorno Virtual
```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# Windows (PowerShell)
env\Scripts\Activate.ps1

# Windows (Command Prompt)
env\Scripts\activate.bat

# Linux/macOS
source env/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalaciones críticas
python -m spacy download es_core_news_sm
python -c "import langchain; print('LangChain instalado correctamente')"
python -c "import chromadb; print('ChromaDB instalado correctamente')"
```

#### Dependencias Principales Instaladas
- **Streamlit**: Framework de interfaz web
- **OpenAI**: API para transcripción con Whisper
- **LangChain**: Framework para aplicaciones de IA (v0.3.27)
- **ChromaDB**: Base de datos vectorial para RAG
- **spaCy**: Procesamiento de lenguaje natural
- **Transformers**: Modelos de Hugging Face

### Paso 4: Configurar Variables de Entorno
Crear archivo `.env` en el directorio raíz:
```bash
# Copiar template
cp .env.example .env

# Editar con tus credenciales
# Windows
notepad .env

# Linux/macOS
nano .env
```

Contenido del archivo `.env`:
```
OPENAI_API_KEY=sk-tu_api_key_de_openai_aqui
HF_TOKEN=hf_tu_token_de_hugging_face_aqui
STREAMLIT_PORT=8501
```

### Paso 5: Ejecutar la Aplicación
```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 🐳 Instalación con Docker

### Prerrequisitos Docker
- Docker Engine 20.0+ instalado
- Docker Compose 2.0+ instalado
- Al menos 4GB de RAM disponible para contenedores

### Opción A: Docker Compose (Recomendado)

#### 1. Configurar Variables de Entorno
```bash
# Copiar y editar archivo de entorno
cp .env.example .env
```

#### 2. Construir y Ejecutar
```bash
# Construir y ejecutar en primer plano
docker-compose up --build

# Ejecutar en segundo plano (modo daemon)
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f buscador-salud
```

#### 3. Comandos Útiles
```bash
# Detener servicios
docker-compose down

# Reconstruir después de cambios
docker-compose up --build

# Limpiar todo (contenedores, imágenes, volúmenes)
docker-compose down -v
docker system prune -a

# Acceder al shell del contenedor
docker exec -it buscador_inteligente_salud bash
```

### Opción B: Docker Directamente
```bash
# Construir imagen
docker build -t buscador_inteligente_salud .

# Ejecutar contenedor
docker run -p 8501:8501 \
  -v $(pwd)/datasets:/app/datasets \
  -e OPENAI_API_KEY=tu_api_key \
  -e HF_TOKEN=tu_token_de_hugging_face \
  --name buscador_salud \
  buscador_inteligente_salud
```

## ☁️ Despliegue en Hugging Face Spaces

### Preparación del Proyecto

#### 1. Verificar Archivos Necesarios
Asegurar que estos archivos estén presentes:
- `app.py` - Aplicación principal
- `requirements.txt` - Dependencias Python
- `packages.txt` - Paquetes del sistema
- `README.md` - Con encabezado YAML para HF
- `functions/` y `utils/` - Código del proyecto

#### 2. Configurar README.md para HF
El archivo debe comenzar con:
```yaml
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
```

### Creación del Space

#### 1. Crear Nuevo Space
1. Ir a [Hugging Face Spaces](https://huggingface.co/spaces)
2. Clic en "Create new Space"
3. Configurar:
   - **Space name**: `buscador-inteligente-salud`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU basic (gratuito)

#### 2. Configurar Variables Secretas
En Settings > Variables and secrets, agregar:
```
OPENAI_API_KEY = sk-tu_openai_api_key_aqui
HF_TOKEN = hf_tu_huggingface_token_aqui
```

#### 3. Subir Código
**Opción A**: Conectar repositorio GitHub existente
**Opción B**: Subir archivos directamente al repositorio del Space

### Configuración Específica para HF

#### Archivo packages.txt
Crear si no existe:
```
espeak
espeak-data
libespeak1
libespeak-dev
ffmpeg
```

#### Optimizaciones
- El modelo spaCy se descarga automáticamente
- Puerto 7860 se configura automáticamente
- Streamlit se optimiza para el entorno de HF

## 🚨 Resolución de Problemas

### Errores Comunes de Instalación

#### Error: "No module named 'xxx'"
```bash
# Reinstalar dependencias
pip install -r requirements.txt --upgrade --force-reinstall
```

#### Error de permisos en Docker (Linux/macOS)
```bash
sudo chown -R $USER:$USER datasets/
chmod -R 755 datasets/
```

#### Error de memoria insuficiente
- Cerrar otras aplicaciones
- Usar Docker con límites de memoria:
```bash
docker run --memory=4g --memory-swap=6g ...
```

### Problemas de Configuración

#### Variables de entorno no detectadas
1. Verificar que el archivo `.env` esté en el directorio raíz
2. Comprobar que no hay espacios extra en las variables
3. Reiniciar la aplicación después de cambios

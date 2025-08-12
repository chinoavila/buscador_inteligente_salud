# Guía de Instalación Detallada

Esta guía proporciona instrucciones paso a paso para instalar y configurar el Buscador Inteligente de Profesionales de Salud en diferentes entornos.

## 🔧 Prerrequisitos

### Requisitos del Sistema
- **Python**: 3.8 o superior (recomendado: 3.10+)
- **RAM**: Mínimo 4GB (recomendado: 8GB para modelos de ML y ChromaDB)
- **Espacio en disco**: Al menos 3GB libres (2GB para modelos + 1GB para datos)
- **CPU**: Procesador moderno con soporte para AVX (para PyTorch)
- **Micrófono**: Funcional en el sistema (para grabación de audio)
- **Navegador**: Chrome, Firefox, Safari o Edge (con soporte de Web Audio API)
- **Conectividad**: Internet estable para APIs de OpenAI y Hugging Face

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
# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# Descargar modelo spaCy español
python -m spacy download es_core_news_sm

# Verificar instalación
python -c "import streamlit, langchain, chromadb; print('✅ Instalación exitosa')"
```

### Paso 4: Configurar Variables de Entorno
Crear archivo `.env` en el directorio raíz:
```bash
# Copiar template y editar
cp .env.example .env
```

**Contenido del archivo `.env`:**
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

### Prerrequisitos
- Docker Engine 20.0+ y Docker Compose 2.0+
- 6GB RAM y 5GB espacio libre en disco

### Opción A: Docker Compose (Recomendado)
```bash
# 1. Configurar variables de entorno
cp .env.example .env

# 2. Construir y ejecutar
docker-compose up -d --build

# 3. Verificar estado
docker-compose logs -f buscador-salud
```

**Comandos útiles:**
```bash
# Detener servicios
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f buscador-salud

# Acceder al contenedor
docker exec -it buscador_inteligente_salud bash

# Backup de ChromaDB
docker cp buscador_inteligente_salud:/app/chroma_db ./backup_chroma_db
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

### 1. Preparar Proyecto
Verificar archivos necesarios: `app.py`, `requirements.txt`, `packages.txt`, `README.md`

**Configurar README.md para HF:**
```yaml
---
title: Buscador Inteligente de Profesionales de Salud
emoji: 🏥
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
---
```

### 2. Crear Space
1. Ir a [Hugging Face Spaces](https://huggingface.co/spaces) → "Create new Space"
2. Configurar: Space name: `buscador-inteligente-salud`, SDK: Streamlit
3. En Settings > Variables and secrets:
   ```
   OPENAI_API_KEY = sk-tu_openai_api_key_aqui
   HF_TOKEN = hf_tu_huggingface_token_aqui
   ```

### 3. Subir Código
- **Opción A**: Conectar repositorio GitHub existente
- **Opción B**: Subir archivos directamente al Space

## 🚨 Resolución de Problemas

### Errores de Instalación
**"No module named 'xxx'":**
```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

**Error de permisos (Linux/macOS):**
```bash
sudo chown -R $USER:$USER datasets/
chmod -R 755 datasets/
```

**Memoria insuficiente:**
- Cerrar otras aplicaciones
- Usar Docker con límites: `docker run --memory=4g ...`

### Problemas de Configuración
**Variables de entorno no detectadas:**
1. Verificar archivo `.env` en directorio raíz
2. Comprobar que no hay espacios extra
3. Reiniciar aplicación después de cambios

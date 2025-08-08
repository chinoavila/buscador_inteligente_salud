# Solución de Problemas

Esta guía proporciona soluciones a los problemas más comunes que pueden encontrarse al usar el Buscador Inteligente de Profesionales de Salud.

## 🚨 Problemas de Instalación

### Error: "Python no encontrado"
**Mensaje de error**: `'python' is not recognized as an internal or external command`

**Soluciones**:
1. **Verificar instalación de Python**:
   ```bash
   python --version
   # o
   python3 --version
   ```

2. **Agregar Python al PATH** (Windows):
   - Buscar "Variables de entorno" en Windows
   - Agregar ruta de Python a PATH
   - Reiniciar terminal

3. **Reinstalar Python**:
   - Descargar desde [python.org](https://python.org)
   - Marcar "Add to PATH" durante instalación

### Error: "pip no encontrado"
**Mensaje de error**: `'pip' is not recognized as an internal or external command`

**Soluciones**:
```bash
# Windows
python -m pip --version

# Instalar pip si no existe
python -m ensurepip --upgrade

# Linux/macOS
python3 -m pip --version
```

### Error de permisos en instalación
**Mensaje de error**: `Permission denied` o `Access denied`

**Soluciones**:
```bash
# Usar --user flag
pip install --user -r requirements.txt

# En Linux/macOS con sudo (no recomendado)
sudo pip install -r requirements.txt

# Mejor: usar entorno virtual
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### Error: "Microsoft Visual C++ required"
**Mensaje de error**: Error al instalar dependencias en Windows

**Soluciones**:
1. **Instalar Visual Studio Build Tools**:
   - Descargar desde Microsoft
   - Instalar componentes C++

2. **Usar binarios precompilados**:
   ```bash
   pip install --only-binary=all -r requirements.txt
   ```

## 🤖 Problemas de LangChain y RAG

### Error: "No module named 'langchain'"
**Síntomas**: ImportError al intentar ejecutar la aplicación

**Soluciones**:
```bash
# Reinstalar LangChain y dependencias
pip install langchain==0.3.27
pip install langchain-openai
pip install langchain-community
pip install chromadb

# Verificar instalación
python -c "import langchain; print(langchain.__version__)"
```

### Error: "ChromaDB initialization failed"
**Síntomas**: Error al crear la base de datos vectorial

**Causas comunes**:
- Permisos insuficientes en directorio de trabajo
- Conflictos de versiones de ChromaDB
- Espacio en disco insuficiente

**Soluciones**:
```bash
# Limpiar directorio ChromaDB existente
rm -rf ./chroma_db  # Linux/macOS
rmdir /s chroma_db  # Windows

# Verificar permisos
mkdir chroma_db
chmod 755 chroma_db  # Linux/macOS

# Reinstalar ChromaDB
pip uninstall chromadb -y
pip install chromadb>=0.4.0
```

### Error: "OpenAI embeddings rate limit"
**Síntomas**: Errores de límite de tasa al procesar documentos

**Soluciones**:
```bash
# Verificar límites de API OpenAI
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/usage

# Implementar delays en procesamiento
# (configurado automáticamente en el código)
```

### Error: "LangChain vector store empty"
**Síntomas**: No se encuentran documentos en búsquedas RAG

**Verificaciones**:
1. **Comprobar archivos de datos**:
   ```bash
   ls -la datasets/  # Verificar que existen archivos Excel
   ```

2. **Verificar inicialización**:
   ```python
   python -c "
   from utils.rag_utils import RAGProcessor
   rag = RAGProcessor()
   print('RAG inicializado correctamente')
   "
   ```

**Soluciones**:
- Ejecutar re-indexación de documentos
- Verificar formato de archivos Excel
- Comprobar variables de entorno de OpenAI

### Error: "Document loading failed"
**Síntomas**: Errores al cargar archivos Excel para RAG

**Soluciones**:
```bash
# Verificar integridad de archivos Excel
python -c "
import pandas as pd
df = pd.read_excel('datasets/INSTITUCIONES_ACLISA_JULIO.xlsx')
print(f'Archivo cargado: {len(df)} filas')
"

# Reinstalar openpyxl
pip install --upgrade openpyxl
```

## 🔧 Problemas de Configuración

### Variables de entorno no detectadas
**Mensaje de error**: `API key not found` o errores de autenticación

**Verificaciones**:
1. **Comprobar archivo .env**:
   ```bash
   # El archivo debe estar en el directorio raíz
   ls -la .env  # Linux/macOS
   dir .env     # Windows
   ```

2. **Verificar contenido**:
   ```bash
   cat .env     # Linux/macOS
   type .env    # Windows
   ```

3. **Formato correcto**:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxx
   STREAMLIT_PORT=8501
   ```

**Soluciones**:
- **Sin espacios** alrededor del `=`
- **Sin comillas** a menos que sean parte del valor
- **Reiniciar aplicación** después de cambios

### Error: "Model not found" (spaCy)
**Mensaje de error**: `OSError: [E050] Can't find model 'es_core_news_sm'`

**Soluciones**:
```bash
# Instalar modelo manualmente
python -m spacy download es_core_news_sm

# Verificar instalación
python -c "import spacy; spacy.load('es_core_news_sm')"

# Si persiste el error
pip install https://github.com/explosion/spacy-models/releases/download/es_core_news_sm-3.7.0/es_core_news_sm-3.7.0-py3-none-any.whl
```

### Error de puerto ocupado
**Mensaje de error**: `Port 8501 is already in use`

**Soluciones**:
```bash
# Verificar qué usa el puerto
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Linux/macOS

# Usar puerto diferente
streamlit run app.py --server.port 8502

# Cambiar en .env
STREAMLIT_PORT=8502
```

## 🎙️ Problemas de Audio

### Micrófono no detectado
**Mensaje de error**: Botón de grabación no aparece o no funciona

**Verificaciones**:
1. **Permisos del navegador**:
   - Verificar que se permitió acceso al micrófono
   - Revisar configuración de sitio en navegador

2. **Hardware**:
   - Comprobar que el micrófono esté conectado
   - Verificar en configuración del sistema

**Soluciones**:
- **Recargar página** y volver a permitir acceso
- **Cambiar navegador** (Chrome recomendado)
- **Verificar configuración** de audio del sistema
- **Probar con audífonos** con micrófono

### Audio sin sonido o muy bajo
**Mensaje de error**: Grabación sin contenido o muy silenciosa

**Soluciones**:
1. **Ajustar volumen**:
   - Aumentar ganancia del micrófono
   - Verificar niveles en sistema operativo

2. **Distancia del micrófono**:
   - Hablar a 15-30 cm del micrófono
   - Evitar hablar demasiado lejos

3. **Configuración del navegador**:
   - Verificar permisos específicos del sitio
   - Comprobar configuración de privacidad

### Error: "Audio file too large"
**Mensaje de error**: Error al procesar grabación larga

**Soluciones**:
- **Evitar modificar el máximo de grabación por defecto (60 segundos)**

## 🌐 Problemas de Conectividad

### Error de conexión a OpenAI
**Mensaje de error**: `OpenAI API error` o timeouts

**Verificaciones**:
1. **API Key válida**:
   ```bash
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
        https://api.openai.com/v1/models
   ```

2. **Créditos disponibles**:
   - Verificar balance en cuenta OpenAI
   - Comprobar límites de uso

**Soluciones**:
- **Verificar conectividad** a internet
- **Comprobar firewall** o proxy
- **Regenerar API key** si es necesario
- **Contactar soporte** OpenAI si persiste

### Error de conexión a Hugging Face
**Mensaje de error**: `HuggingFace connection error`

**Soluciones**:
```bash
# Verificar token
huggingface-cli whoami

# Login manual
huggingface-cli login

# Verificar conectividad
curl -H "Authorization: Bearer $HF_TOKEN" \
     https://huggingface.co/api/whoami
```

### Timeout en descarga de modelos
**Mensaje de error**: Demora excesiva cargando modelos

**Soluciones**:
- **Verificar velocidad** de internet
- **Usar cache local** si está disponible
- **Reintentar** la operación
- **Configurar proxy** si es necesario

## 🐳 Problemas de Docker

### Docker no instalado
**Mensaje de error**: `docker: command not found`

**Soluciones**:
1. **Instalar Docker**:
   - [Docker Desktop para Windows/Mac](https://docker.com/products/docker-desktop)
   - [Docker Engine para Linux](https://docs.docker.com/engine/install/)

2. **Verificar instalación**:
   ```bash
   docker --version
   docker-compose --version
   ```

### Error de permisos Docker (Linux)
**Mensaje de error**: `Permission denied` al ejecutar docker

**Soluciones**:
```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar sesión o aplicar cambios
newgrp docker

# Verificar
docker run hello-world
```

### Error: "Port already in use" en Docker
**Mensaje de error**: `Port 8501 is already in use`

**Soluciones**:
```bash
# Detener contenedores existentes
docker-compose down

# Ver qué usa el puerto
docker ps
netstat -tulpn | grep :8501

# Cambiar puerto en docker-compose.yml
ports:
  - "8502:8501"
```

### Error de memoria insuficiente
**Mensaje de error**: Container se cierra inesperadamente

**Soluciones**:
```bash
# Verificar recursos Docker
docker system df
docker stats

# Limpiar sistema
docker system prune -a

# Aumentar memoria para Docker Desktop
# Settings > Resources > Memory
```

### Error de build de imagen
**Mensaje de error**: `Build failed` o errores durante construcción

**Soluciones**:
```bash
# Build sin cache
docker-compose build --no-cache

# Ver logs detallados
docker-compose build --progress=plain

# Verificar Dockerfile
# Comprobar sintaxis y dependencias
```

## 🔍 Problemas de Funcionalidad

### Transcripción incorrecta o vacía
**Mensaje de error**: Texto transcrito no coincide con audio

**Causas comunes**:
- Audio de mala calidad
- Ruido de fondo excesivo
- Volumen muy bajo

**Soluciones**:
- **Mejorar calidad** de grabación
- **Reducir ruido** ambiente
- **Hablar más claro** y despacio
- **Verificar configuración** de idioma

### Entidades médicas no detectadas
**Mensaje de error**: No aparecen síntomas o entidades

**Soluciones**:
- **Usar terminología médica** específica
- **Mencionar síntomas claramente**
- **Evitar jerga** o términos coloquiales
- **Repetir información** importante

### Especialidades incorrectas sugeridas
**Mensaje de error**: Recomendaciones no relevantes

**Causas**:
- Entidades mal detectadas
- Síntomas ambiguos

**Soluciones**:
- **Ser más específico** en descripción
- **Incluir duración** y características

## 📱 Problemas de Interfaz

### Aplicación no carga completamente
**Mensaje de error**: Página en blanco o elementos faltantes

**Soluciones**:
```bash
# Verificar logs
streamlit run app.py --logger.level=debug

# Limpiar cache del navegador
# Ctrl+Shift+R (Windows/Linux)
# Cmd+Shift+R (Mac)

# Probar navegador diferente
```

### Botones no responden
**Mensaje de error**: Clics no registrados

**Soluciones**:
- **Esperar carga completa** de la página
- **Recargar aplicación**
- **Verificar JavaScript** habilitado
- **Comprobar consola** del navegador (F12)

### Elementos desalineados
**Mensaje de error**: Layout roto o elementos superpuestos

**Soluciones**:
- **Ajustar zoom** del navegador (100%)
- **Cambiar tamaño** de ventana
- **Actualizar Streamlit**

## 📊 Problemas de Performance

### Aplicación muy lenta
**Mensaje de error**: Respuestas demoradas

**Diagnóstico**:
```bash
# Monitorear recursos
top          # Linux/macOS
taskmgr      # Windows

# Ver logs de Streamlit
streamlit run app.py --logger.level=info
```

**Optimizaciones**:
- **Cerrar aplicaciones** innecesarias
- **Aumentar RAM** disponible
- **Verificar conexión** a internet
- **Limpiar cache** de modelos

### Memoria insuficiente
**Mensaje de error**: `MemoryError` o aplicación se cierra

**Soluciones**:
- **Cerrar otros programas**
- **Reiniciar aplicación** regularmente
- **Usar versión Docker** con límites
- **Optimizar modelos** utilizados

## 🆘 Obtener Ayuda Adicional

### Logs y Debugging
```bash
# Ejecutar con logs detallados
streamlit run app.py --logger.level=debug

# Verificar logs del sistema
# Windows: Event Viewer
# Linux: /var/log/
# macOS: Console.app
```

### Información del Sistema
```bash
# Información de Python
python --version
pip list

# Información del sistema
# Windows
systeminfo

# Linux
uname -a
lsb_release -a

# macOS
system_profiler SPSoftwareDataType
```

### Reportar Problemas
Si el problema persiste:
1. **Recopilar información**:
   - Versión del sistema operativo
   - Versión de Python
   - Logs de error completos
   - Pasos para reproducir
2. **Crear issue** en GitHub
3. **Incluir contexto** relevante
4. **Adjuntar logs** si es necesario

### Contacto y Soporte
- **GitHub Issues**: Para reportar bugs
- **Documentación**: Revisar guías detalladas
- **Community**: Foros de Streamlit y Python

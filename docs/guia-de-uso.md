# Guía de Uso Detallada

Esta guía explica cómo utilizar todas las funcionalidades del Buscador Inteligente de Profesionales de Salud.

## 🎯 Descripción General

El Buscador Inteligente de Profesionales de Salud es una aplicación web que permite:
1. **Grabar consultas médicas por voz** (hasta 60 segundos)
2. **Transcribir automáticamente** el audio a texto
3. **Extraer entidades médicas** (síntomas, condiciones, etc.)
4. **Buscar profesionales con RAG** usando inteligencia artificial avanzada
5. **Obtener recomendaciones personalizadas** de establecimientos de salud

## 🚀 Acceso a la Aplicación

### URL Local
Si ejecutas la aplicación localmente:
```
http://localhost:8501
```

### URL en Hugging Face Spaces
Si está desplegada en HF Spaces:
```
https://huggingface.co/spaces/tu-usuario/buscador-inteligente-salud
```

## 📱 Interfaz de Usuario

### Pantalla Principal
La aplicación presenta una interfaz limpia y minimalista con:
- **Título**: "Buscador Inteligente de Profesionales de Salud"
- **Botón de Ayuda**: Muestra instrucciones detalladas
- **Grabador de Audio**: Componente principal para capturar voz
- **Área de Resultados**: Muestra transcripción y análisis

### Elementos de la Interfaz
1. **Icono de ayuda (❓)**: Despliega panel de instrucciones
2. **Botón de grabación**: Inicia/detiene captura de audio
3. **Indicador de tiempo**: Muestra duración de grabación
4. **Panel de transcripción**: Texto convertido del audio
5. **Panel de entidades**: Elementos médicos detectados
6. **Panel de resultados**: Recomendaciones de profesionales y establecimientos

## 🎙️ Grabación de Audio

### Iniciar Grabación
1. **Permitir acceso al micrófono** cuando el navegador lo solicite
2. **Hacer clic en el botón de grabación** (ícono de micrófono)
3. **Hablar claramente** hacia el micrófono
4. **Hacer clic nuevamente** para detener la grabación

### Consejos para Mejor Grabación
- **Ambiente silencioso**: Minimizar ruido de fondo
- **Distancia adecuada**: 15-30 cm del micrófono
- **Volumen apropiado**: Hablar con claridad, sin susurrar ni gritar
- **Velocidad moderada**: No hablar demasiado rápido
- **Pausas naturales**: Permite mejor segmentación del audio

### Limitaciones Técnicas
- **Duración máxima**: 60 segundos por grabación
- **Formato soportado**: WAV, calidad CD (44.1kHz, 16-bit)
- **Tamaño máximo**: Aproximadamente 5MB por archivo
- **Navegadores compatibles**: Chrome, Firefox, Safari, Edge

## 📝 Proceso de Transcripción

### Funcionamiento Automático
1. **Al finalizar la grabación**, el audio se envía automáticamente
2. **Whisper de OpenAI** procesa el archivo de audio
3. **La transcripción aparece** en la sección correspondiente
4. **El proceso toma** entre 5-15 segundos típicamente

### Calidad de Transcripción
- **Idioma optimizado**: Español (modelo multiidioma)
- **Precisión típica**: 85-95% en condiciones ideales
- **Manejo de ruido**: Filtrado automático de sonidos ambientales
- **Puntuación automática**: Comas, puntos y mayúsculas

### Formato de Salida
La transcripción se presenta como texto plano con:
- Puntuación automática
- Capitalización apropiada
- Separación en oraciones
- Eliminación de muletillas obvias

## 🔍 Extracción de Entidades Médicas

### Tipos de Entidades Detectadas
1. **Síntomas**: Dolor, fiebre, mareos, náuseas, etc.
2. **Partes del cuerpo**: Cabeza, estómago, corazón, etc.
3. **Condiciones**: Diabetes, hipertensión, asma, etc.
4. **Medicamentos**: Nombres de fármacos mencionados
5. **Especialidades**: Referencias a tipos de médicos

### Tecnologías Utilizadas
- **spaCy**: Modelo `es_core_news_sm` para español
- **Hugging Face**: Modelos especializados en entidades médicas
- **Procesamiento combinado**: Múltiples modelos para mayor precisión

### Formato de Resultados
Las entidades se muestran como:
```
🏥 Entidades Médicas Detectadas:
- Síntomas: dolor de cabeza, mareos
- Partes del cuerpo: cabeza
- Condiciones: migraña (inferida)
```

## � Sistema RAG (Retrieval-Augmented Generation)

### Funcionamiento del RAG
El sistema utiliza tecnología avanzada de IA para encontrar profesionales apropiados:
1. **Análisis de entidades detectadas** en la transcripción
2. **Búsqueda semántica** en base de datos vectorial (ChromaDB)
3. **Procesamiento con LangChain** para contextualizar resultados
4. **Generación de recomendaciones** usando modelos de OpenAI
5. **Presentación personalizada** de profesionales y establecimientos

### Tecnologías RAG Implementadas
- **ChromaDB**: Base de datos vectorial para búsqueda semántica
- **LangChain**: Framework para aplicaciones de IA conversacional
- **OpenAI Embeddings**: Vectorización de documentos médicos
- **ChatGPT**: Generación de respuestas contextualizadas
- **Retrieval QA**: Cadena de pregunta-respuesta con contexto

### Proceso de Búsqueda Inteligente
1. **Vectorización**: Las entidades médicas se convierten en vectores
2. **Similarity Search**: ChromaDB encuentra documentos similares
3. **Context Retrieval**: Se recupera información relevante de establecimientos
4. **LLM Processing**: ChatGPT genera recomendaciones personalizadas
5. **Ranking**: Los resultados se ordenan por relevancia y proximidad

### Ventajas del Sistema RAG
- **Búsqueda semántica**: Encuentra profesionales por contexto, no solo palabras clave
- **Actualizaciones dinámicas**: Incorpora nuevos establecimientos automáticamente  
- **Respuestas contextualizadas**: Explica por qué recomienda cada profesional
- **Precisión mejorada**: Combina múltiples fuentes de información
- **Escalabilidad**: Maneja grandes volúmenes de datos médicos

### Formato de Recomendaciones RAG
```
🏥 Profesionales Recomendados:

📍 Dr. Juan Pérez - Neurologo
   Centro Médico Central
   📞 Tel: (011) 4555-1234
   📍 Av. Corrientes 1234, CABA
   ⭐ Relevancia: 95% - Especialista en migraña y cefaleas

📍 Dra. María González - Medicina General  
   Hospital Público San Juan
   📞 Tel: (011) 4555-5678
   📍 San Martín 567, CABA
   ⭐ Relevancia: 85% - Evaluación inicial de síntomas neurológicos
```

## 📊 Base de Datos de Establecimientos

### Fuentes de Datos
La aplicación incluye datasets de:
- **Centros de salud públicos**: REFES Argentina
- **Establecimientos privados**: Instituciones registradas
- **Prestadores ACLISA**: Red de laboratorios
- **Centros de atención primaria**: Ubicaciones geográficas

### Información Disponible
- **Nombre del establecimiento**
- **Dirección completa**
- **Teléfonos de contacto**
- **Tipo de institución** (pública/privada)
- **Especialidades disponibles**
- **Horarios de atención** (cuando disponible)

### Búsqueda y Filtros
- **Por especialidad**: Filtrar según recomendación
- **Por ubicación**: Buscar por provincia/ciudad
- **Por tipo**: Público vs. privado
- **Por servicios**: Emergencias, internación, ambulatorio

## 🎛️ Configuración y Personalización

### Parámetros Ajustables
En el código fuente (`app.py`):
```python
MAX_SEGUNDOS = 60  # Duración máxima de grabación
UMBRAL_CONFIANZA = 0.7  # Umbral para entidades detectadas
FORMATO_AUDIO = "wav"  # Formato de audio para transcripción
```

### Variables de Entorno
Archivo `.env`:
```
OPENAI_API_KEY=tu_key_aqui  # Para transcripción
HF_TOKEN=tu_token_aqui      # Para modelos de ML
STREAMLIT_PORT=8501         # Puerto de la aplicación
LOG_LEVEL=INFO              # Nivel de logging
```

### Modelos Personalizables
En `utils/hf_utils.py`:
- Cambiar modelos de Hugging Face
- Ajustar parámetros de inferencia
- Modificar umbrales de confianza

## 🔧 Solución de Problemas de Uso

### Problemas de Audio
**Problema**: No se puede grabar audio
- **Verificar permisos** del navegador para micrófono
- **Comprobar que el micrófono** esté funcionando
- **Recargar la página** y volver a intentar

**Problema**: Audio se corta o no se escucha bien
- **Verificar configuración** de audio del sistema
- **Ajustar volumen** del micrófono
- **Cambiar dispositivo** de entrada si hay múltiples

### Problemas de Transcripción
**Problema**: Transcripción incorrecta o vacía
- **Hablar más claro** y despacio
- **Reducir ruido ambiente**
- **Verificar conexión** a internet
- **Comprobar créditos** de OpenAI API

**Problema**: Transcripción en idioma incorrecto
- **Hablar únicamente en español**
- **Evitar mezclar idiomas** en una misma grabación

### Problemas de Entidades
**Problema**: No se detectan entidades médicas
- **Usar terminología médica** más específica
- **Mencionar síntomas claramente**
- **Evitar jerga o términos coloquiales**

**Problema**: Entidades incorrectas detectadas
- **Ser más específico** en la descripción
- **Usar nombres médicos** cuando sea posible
- **Repetir información importante**

## 📈 Mejores Prácticas de Uso

### Para Mejores Resultados
1. **Preparar la consulta** antes de grabar
2. **Hablar de forma estructurada**: síntomas, duración, intensidad
3. **Mencionar antecedentes** relevantes
4. **Especificar ubicación** del problema
5. **Indicar urgencia** si aplica

### Ejemplo de Consulta Óptima
```
"Tengo dolor de cabeza intenso desde hace tres días, 
localizado en la sien derecha, acompañado de náuseas 
y sensibilidad a la luz. El dolor empeora por las mañanas 
y mejora ligeramente con paracetamol."
```

### Información a Evitar
- **Datos personales identificables**: nombres, apellidos, DNI
- **Información médica sensible**: diagnósticos previos específicos
- **Medicación actual**: solo mencionar si es relevante al síntoma actual

## 🚨 Disclaimers Importantes

### Uso Académico
- Este proyecto es **solo para fines académicos**
- **No reemplaza** consulta médica profesional
- **No proporciona diagnósticos** médicos

### Limitaciones
- Las sugerencias son **orientativas únicamente**
- La precisión depende de la **calidad del audio**
- Los modelos pueden tener **sesgos o errores**

### Privacidad
- **No se almacenan** grabaciones de audio
- **No se guardan** transcripciones permanentemente
- **No se recopilan** datos personales del usuario

# 📚 Documentación - Buscador Inteligente de Profesionales de Salud

Bienvenido a la documentación completa del proyecto. Esta documentación está organizada para proporcionar información detallada según tus necesidades específicas.

## 🗂️ Estructura de la Documentación

### 📖 Para Usuarios
- **[Guía de Uso Completa](guia-de-uso.md)** - Cómo utilizar todas las funcionalidades de la aplicación
- **[Solución de Problemas](solucion-problemas.md)** - Resolución de errores comunes y FAQ

### 🛠️ Para Desarrolladores e Instaladores
- **[Guía de Instalación Detallada](instalacion-detallada.md)** - Instrucciones paso a paso para todos los entornos
- **[Documentación Técnica](documentacion-tecnica.md)** - Arquitectura, APIs y detalles de desarrollo

## 🚀 Inicio Rápido por Perfil

### 👤 Soy un Usuario Final
1. **Empezar**: Lee la [Guía de Uso](guia-de-uso.md)
2. **Problemas**: Consulta [Solución de Problemas](solucion-problemas.md)
3. **Feedback**: Revisa el README principal para información de contacto

### 💻 Soy un Desarrollador/Administrador
1. **Instalación**: Sigue la [Guía de Instalación Detallada](instalacion-detallada.md)
2. **Arquitectura**: Revisa la [Documentación Técnica](documentacion-tecnica.md)
3. **Troubleshooting**: Consulta [Solución de Problemas](solucion-problemas.md)

### 🎓 Soy un Académico/Investigador
1. **Contexto del Proyecto**: Lee el README principal
2. **Implementación Técnica**: Revisa [Documentación Técnica](documentacion-tecnica.md)
3. **Casos de Uso**: Consulta [Guía de Uso](guia-de-uso.md)

## 📋 Contenido por Documento

### [📖 Guía de Uso Completa](guia-de-uso.md)
- Descripción general de funcionalidades
- Proceso paso a paso de uso
- Grabación de audio y mejores prácticas
- Interpretación de resultados
- Configuración de parámetros
- Mejores prácticas y consejos

### [🔧 Guía de Instalación Detallada](instalacion-detallada.md)
- Prerrequisitos detallados
- Instalación local paso a paso
- Configuración con Docker
- Despliegue en Hugging Face Spaces
- Configuración de variables de entorno
- Resolución de problemas de instalación

### [⚙️ Documentación Técnica](documentacion-tecnica.md)
- Arquitectura del sistema
- Descripción de componentes
- APIs y integraciones
- Flujo de datos
- Modelos de machine learning utilizados
- Consideraciones de rendimiento y escalabilidad
- Extensibilidad y personalización

### [🚨 Solución de Problemas](solucion-problemas.md)
- Problemas comunes de instalación
- Errores de configuración
- Problemas de audio y micrófono
- Errores de conectividad
- Problemas específicos de Docker
- Issues de funcionalidad
- Cómo obtener ayuda adicional

## 🎯 Guías Rápidas por Escenario

### Instalación Express
```bash
git clone https://github.com/chinoavila/buscador_inteligente_salud
cd buscador_inteligente_salud
cp .env.example .env
# Editar .env con tus API keys
docker-compose up --build
```
📚 **Detalle completo**: [Instalación Detallada](instalacion-detallada.md)

### Primer Uso
1. Acceder a `http://localhost:8501`
2. Permitir acceso al micrófono
3. Grabar consulta médica (máx. 60s)
4. Revisar transcripción y recomendaciones

📚 **Detalle completo**: [Guía de Uso](guia-de-uso.md)

### Desarrollo Local
1. Crear entorno virtual Python
2. Instalar dependencias
3. Configurar variables de entorno
4. Ejecutar con `streamlit run app.py`

📚 **Detalle completo**: [Documentación Técnica](documentacion-tecnica.md)

## 🔍 Búsqueda Rápida de Información

### Errores Comunes
- **"Python no encontrado"** → [Problemas de Instalación](solucion-problemas.md#problemas-de-instalación)
- **"API key not found"** → [Problemas de Configuración](solucion-problemas.md#problemas-de-configuración)
- **"Micrófono no detectado"** → [Problemas de Audio](solucion-problemas.md#problemas-de-audio)
- **"Port already in use"** → [Problemas de Docker](solucion-problemas.md#problemas-de-docker)

### Configuración Específica
- **Variables de entorno** → [Instalación: Configurar Variables](instalacion-detallada.md#paso-4-configurar-variables-de-entorno)
- **Modelos de ML** → [Técnica: Modelos Utilizados](documentacion-tecnica.md#modelos-utilizados)
- **Docker Compose** → [Instalación: Docker](instalacion-detallada.md#instalación-con-docker)
- **Hugging Face Spaces** → [Instalación: HF Spaces](instalacion-detallada.md#despliegue-en-hugging-face-spaces)

## 📞 Soporte y Contacto

### Para Reportar Problemas
1. **Revisar primero**: [Solución de Problemas](solucion-problemas.md)
2. **GitHub Issues**: Para bugs y mejoras
3. **Incluir información**: SO, versión Python, logs de error

### Para Sugerencias Académicas
- Crear issue en GitHub con etiqueta "enhancement"
- Incluir contexto académico y referencias
- Proponer implementación si es posible

### Recursos Externos
- **[Streamlit Docs](https://docs.streamlit.io/)** - Framework web utilizado
- **[OpenAI API](https://platform.openai.com/docs)** - Documentación Whisper
- **[Hugging Face](https://huggingface.co/docs)** - Modelos de ML
- **[spaCy](https://spacy.io/)** - Procesamiento de lenguaje natural

---

## 🎓 Nota Académica

Esta documentación es parte de un proyecto académico de la **Maestría en Tecnologías de la Información con enfoque en Inteligencia Artificial**. El objetivo es demostrar la aplicación práctica de conceptos de ML/AI en el dominio de la salud digital.

**⚠️ Importante**: Este proyecto es solo para fines académicos y de investigación. No debe utilizarse como sustituto del consejo médico profesional.

---

*Última actualización: Agosto 2025*

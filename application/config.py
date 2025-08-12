# Configuraciones de la aplicación
APP_CONFIG = {
    "titulo": "Buscador Inteligente de Prestadores de Salud",
    "descripcion": "Encuentre prestadores de salud especializados basándose en sus síntomas",
    "version": "2.0.0",
    "autor": "Equipo de Desarrollo",
    "max_segundos_audio": 60,
    "max_caracteres_texto": 1000,
    "min_caracteres_texto": 10
}

# Mensajes de ayuda y sugerencias
HELP_MESSAGES = {
    "sintomas_texto": {
        "placeholder": "Ejemplo: Tengo dolor de cabeza intenso, náuseas y sensibilidad a la luz desde hace dos días...",
        "ayuda": "Escriba de manera clara y detallada todos los síntomas que está experimentando",
        "sugerencias": [
            "Sea específico sobre la ubicación del dolor o molestia",
            "Mencione la intensidad (leve, moderado, severo)",
            "Indique la duración de los síntomas",
            "Incluya síntomas relacionados o asociados"
        ]
    },
    "audio_grabacion": {
        "instrucciones": [
            "Presione el micrófono para iniciar/detener",
            "Hable claramente y a velocidad normal",
            "Describa sus síntomas de manera organizada",
            "Evite ruidos de fondo durante la grabación"
        ]
    }
}

# Validaciones de entrada
VALIDATION_RULES = {
    "texto_sintomas": [
        {
            "type": "required",
            "message": "La descripción de síntomas es obligatoria"
        },
        {
            "type": "min_length",
            "value": APP_CONFIG["min_caracteres_texto"],
            "message": f"La descripción debe tener al menos {APP_CONFIG['min_caracteres_texto']} caracteres"
        },
        {
            "type": "max_length", 
            "value": APP_CONFIG["max_caracteres_texto"],
            "message": f"La descripción no debe exceder {APP_CONFIG['max_caracteres_texto']} caracteres"
        }
    ]
}

# Mensajes de estado y errores
STATUS_MESSAGES = {
    "procesando_texto": "🔍 Analizando síntomas y extrayendo entidades médicas...",
    "procesando_audio": "🎧 Transcribiendo audio...",
    "buscando_prestadores": "🔍 Buscando prestadores especializados...",
    "completado": "✅ Búsqueda completada exitosamente",
    "error_transcripcion": {
        "titulo": "Error de transcripción",
        "mensaje": "No se pudo transcribir el audio.",
        "sugerencias": [
            "Verifique que su micrófono funcione correctamente",
            "Grabe en un ambiente silencioso",
            "Hable más claro y a volumen adecuado",
            "Intente grabar nuevamente"
        ]
    },
    "error_entidades": {
        "titulo": "Error en el análisis",
        "mensaje": "No fue posible identificar entidades médicas.",
        "sugerencias": [
            "Sea más específico en la descripción",
            "Use terminología médica común",
            "Incluya ubicación, intensidad y duración de los síntomas"
        ]
    },
    "sin_resultados": {
        "titulo": "Sin resultados",
        "mensaje": "No se pudieron encontrar prestadores para las especialidades consultadas.",
        "sugerencias": [
            "Intente con una descripción más específica",
            "Agregue más detalles sobre los síntomas",
            "Consulte directamente con un médico general"
        ]
    }
}

# Estilos CSS mejorados
CUSTOM_CSS = """
<style>
    /* Estilos principales */
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #4682B4;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E6F3FF;
        font-weight: 600;
    }
    
    /* Contenedores de entrada */
    .input-method-card {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #E9ECEF;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .input-method-selected {
        border-color: #2E8B57;
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%);
        box-shadow: 0 6px 12px rgba(46,139,87,0.15);
    }
    
    /* Contenedores de instrucciones */
    .instructions-box {
        background: linear-gradient(135deg, #E6F3FF 0%, #F0F8FF 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #4682B4;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Contenedores de resultados */
    .result-container {
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #90EE90;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(144,238,144,0.2);
    }
    
    /* Contenedores de error */
    .error-container {
        background: linear-gradient(135deg, #FFE6E6 0%, #FFF5F5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FF6B6B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(255,107,107,0.2);
    }
    
    /* Mejoras de accesibilidad */
    .stTextArea > label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2E8B57;
    }
    
    .audio-recorder-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 2rem;
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%);
        border-radius: 15px;
        border: 2px dashed #2E8B57;
    }
    
    /* Botones mejorados */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Botones personalizados estilo radio */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%) !important;
        border: 2px solid #2E8B57 !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 12px rgba(46,139,87,0.3) !important;
        transition: all 0.3s ease !important;
        color: white !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #228B22 0%, #2E8B57 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(46,139,87,0.4) !important;
    }
    
    div.stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        border: 2px solid #E9ECEF !important;
        border-radius: 12px !important;
        padding: 1rem 2rem !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
        color: #333 !important;
    }
    
    div.stButton > button[kind="secondary"]:hover {
        border-color: #2E8B57 !important;
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%) !important;
        box-shadow: 0 4px 8px rgba(46,139,87,0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Indicador de método seleccionado */
    .method-indicator {
        background: linear-gradient(135deg, #E6F3FF 0%, #F0F8FF 100%);
        border-left: 4px solid #2E8B57;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
        color: #2E8B57;
        text-align: center;
    }
    
    /* Radio buttons mejorados - Streamlit específico */
    div[data-testid="stRadio"] {
        background: transparent;
    }
    
    div[data-testid="stRadio"] > div {
        gap: 1.5rem !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    div[data-testid="stRadio"] label {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        padding: 1.2rem 2rem !important;
        border-radius: 12px !important;
        border: 2px solid #E9ECEF !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        min-width: 180px !important;
        text-align: center !important;
        margin: 0.5rem !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div[data-testid="stRadio"] label:hover {
        border-color: #2E8B57 !important;
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%) !important;
        box-shadow: 0 4px 8px rgba(46,139,87,0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    div[data-testid="stRadio"] input[type="radio"]:checked + label,
    div[data-testid="stRadio"] label:has(input[type="radio"]:checked) {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%) !important;
        border-color: #2E8B57 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(46,139,87,0.3) !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="stRadio"] input[type="radio"]:checked + label:hover,
    div[data-testid="stRadio"] label:has(input[type="radio"]:checked):hover {
        background: linear-gradient(135deg, #228B22 0%, #2E8B57 100%) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Ocultar el radio button circular por defecto */
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    
    /* Asegurar que el texto del label sea visible */
    div[data-testid="stRadio"] label > div {
        color: inherit !important;
        font-weight: inherit !important;
    }
    
    /* Alternativa usando clases de Streamlit */
    .stRadio > div {
        gap: 1.5rem !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    .stRadio label {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        padding: 1.2rem 2rem !important;
        border-radius: 12px !important;
        border: 2px solid #E9ECEF !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        min-width: 180px !important;
        text-align: center !important;
        margin: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stRadio label:hover {
        border-color: #2E8B57 !important;
        background: linear-gradient(135deg, #F0FFF0 0%, #FFFFFF 100%) !important;
        box-shadow: 0 4px 8px rgba(46,139,87,0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Barra de progreso mejorada */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2E8B57 0%, #90EE90 100%);
    }
    
    /* Responsividad mejorada */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .input-method-card {
            padding: 1rem;
        }
        
        div[data-testid="stRadio"] > div,
        .stRadio > div {
            flex-direction: column !important;
            gap: 1rem !important;
            align-items: stretch !important;
        }
        
        div[data-testid="stRadio"] label,
        .stRadio label {
            min-width: auto !important;
            width: 100% !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
        }
        
        div.stButton > button[kind="primary"],
        div.stButton > button[kind="secondary"] {
            padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important;
        }
    }
    
    @media (max-width: 480px) {
        div[data-testid="stRadio"] label,
        .stRadio label {
            padding: 0.8rem 1rem !important;
            font-size: 0.9rem !important;
        }
        
        div.stButton > button[kind="primary"],
        div.stButton > button[kind="secondary"] {
            padding: 0.7rem 1rem !important;
            font-size: 0.9rem !important;
        }
    }
    
    /* Modo de alto contraste */
    .high-contrast .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    .high-contrast .input-method-card {
        background-color: #1a1a1a !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    .high-contrast div[data-testid="stRadio"] label,
    .high-contrast .stRadio label {
        background: #1a1a1a !important;
        border-color: #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    .high-contrast div[data-testid="stRadio"] label:hover,
    .high-contrast .stRadio label:hover {
        background: #333333 !important;
        border-color: #90EE90 !important;
    }
    
    .high-contrast div[data-testid="stRadio"] input[type="radio"]:checked + label,
    .high-contrast div[data-testid="stRadio"] label:has(input[type="radio"]:checked),
    .high-contrast .stRadio input[type="radio"]:checked + label {
        background: #90EE90 !important;
        border-color: #90EE90 !important;
        color: #000000 !important;
    }
    
    /* Estilos adicionales para radio buttons - versiones alternativas */
    [data-testid="stRadio"] [role="radiogroup"] {
        gap: 1.5rem !important;
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    [data-testid="stRadio"] [role="radiogroup"] label {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%) !important;
        padding: 1.2rem 2rem !important;
        border-radius: 12px !important;
        border: 2px solid #E9ECEF !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        min-width: 180px !important;
        text-align: center !important;
        margin: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Radio button personalizado con marcador visual */
    [data-testid="stRadio"] input[type="radio"]:checked + div::before {
        content: "✓" !important;
        position: absolute !important;
        top: 0.5rem !important;
        right: 0.5rem !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    
    /* Reducción de movimiento */
    .reduce-motion * {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
</style>
"""

# Configuraciones de accesibilidad
ACCESSIBILITY_CONFIG = {
    "font_sizes": {
        "Normal": "1rem",
        "Grande": "1.2rem",
        "Muy grande": "1.5rem"
    },
    "contrast_themes": {
        "normal": {},
        "high": {
            "background": "#000000",
            "text": "#FFFFFF",
            "card_bg": "#1a1a1a"
        }
    }
}

import logging
from functions.transcripcion import transcribir_con_status
from functions.extraccion import detectar_entidades_con_status
from functions.rag import consultar_rag_con_status
from .config import APP_CONFIG

class HealthOrchestrator:
    """
    Orquestador principal que coordina el flujo de procesamiento de síntomas
    para la búsqueda de prestadores de salud.
    """
    
    def __init__(self):
        """
        Inicializa el orquestador con configuración básica.

        :return: None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
    def transcribe_audio(self, audio_bytes):
        """
        Transcribe audio a texto utilizando el flujo existente con estado.

        :param audio_bytes: Datos de audio en bytes
        :return: Texto transcrito o None en caso de fallo
        """
        try:
            self.logger.info("Transcribiendo audio (método rápido)")
            transcription = transcribir_con_status(audio_bytes)
            return transcription if transcription else None
        except Exception as e:
            self.logger.error(f"Fallo transcripción rápida: {e}")
            return None
        
    def process_text_symptoms(self, text_symptoms):
        """
        Procesa síntomas escritos en texto y busca prestadores recomendados.

        :param text_symptoms: Descripción textual de los síntomas
        :return: Diccionario con claves: success, symptoms_text, entities, recommendations, error_message
        """
        self.logger.info("Iniciando procesamiento de síntomas en texto")
        
        result = {
            'success': False,
            'symptoms_text': text_symptoms,
            'entities': None,
            'recommendations': None,
            'error_message': None
        }
        
        try:
            # Paso 1: Extraer entidades médicas del texto
            self.logger.info("Extrayendo entidades médicas")
            entities = detectar_entidades_con_status(text_symptoms)
            
            if not entities:
                result['error_message'] = "No se pudieron identificar síntomas específicos. Intenta ser más descriptivo."
                self.logger.warning("No se encontraron entidades médicas en el texto")
                return result
                
            result['entities'] = entities
            
            # Paso 2: Consultar prestadores usando RAG
            self.logger.info("Consultando prestadores con RAG")
            recommendations = consultar_rag_con_status(entities)
            
            if not recommendations:
                result['error_message'] = "No se encontraron prestadores para estos síntomas."
                self.logger.warning("No se encontraron recomendaciones de prestadores")
                return result
                
            result['recommendations'] = recommendations
            result['success'] = True
            
            self.logger.info("Procesamiento de síntomas completado exitosamente")
            return result
            
        except Exception as e:
            error_msg = f"Error durante el procesamiento de síntomas: {str(e)}"
            result['error_message'] = error_msg
            self.logger.error(error_msg, exc_info=True)
            return result
    
    def process_audio_symptoms(self, audio_bytes, pretranscription=None):
        """
        Procesa síntomas grabados en audio y busca prestadores recomendados.

        :param audio_bytes: Datos de audio en formato bytes
        :param pretranscription: Transcripción previa para reutilizar (opcional)
        :return: Diccionario con claves: success, transcription, entities, recommendations, error_message
        """
        self.logger.info("Iniciando procesamiento de síntomas en audio")
        
        result = {
            'success': False,
            'transcription': None,
            'entities': None,
            'recommendations': None,
            'error_message': None
        }
        
        try:
            # Paso 1: Transcribir el audio
            self.logger.info("Transcribiendo audio")
            transcription = pretranscription if pretranscription else transcribir_con_status(audio_bytes)
            
            if not transcription:
                result['error_message'] = "No se pudo transcribir el audio. Verifica tu micrófono."
                self.logger.warning("Fallo en la transcripción del audio")
                return result
                
            result['transcription'] = transcription
            
            # Paso 2: Extraer entidades médicas de la transcripción
            self.logger.info("Extrayendo entidades médicas de la transcripción")
            entities = detectar_entidades_con_status(transcription)
            
            if not entities:
                result['error_message'] = "No se pudieron identificar síntomas en la grabación. Intenta grabar nuevamente."
                self.logger.warning("No se encontraron entidades médicas en la transcripción")
                return result
                
            result['entities'] = entities
            
            # Paso 3: Consultar prestadores usando RAG
            self.logger.info("Consultando prestadores con RAG")
            recommendations = consultar_rag_con_status(entities)
            
            if not recommendations:
                result['error_message'] = "No se encontraron prestadores para estos síntomas."
                self.logger.warning("No se encontraron recomendaciones de prestadores")
                return result
                
            result['recommendations'] = recommendations
            result['success'] = True
            
            self.logger.info("Procesamiento de audio completado exitosamente")
            return result
            
        except Exception as e:
            error_msg = f"Error durante el procesamiento de audio: {str(e)}"
            result['error_message'] = error_msg
            self.logger.error(error_msg, exc_info=True)
            return result
    
    def validate_input(self, input_data, min_length=None):
        """
        Valida la entrada de síntomas.

        :param input_data: Datos de entrada a validar
        :param min_length: Longitud mínima requerida (usa config si no se especifica)
        :return: Tupla (es_válido, mensaje_error)
        """
        if min_length is None:
            min_length = APP_CONFIG["min_caracteres_texto"]
            
        if not input_data or not isinstance(input_data, str):
            return False, "Los datos de entrada no pueden estar vacíos"
            
        cleaned_input = input_data.strip()
        
        if len(cleaned_input) < min_length:
            return False, f"La descripción debe tener al menos {min_length} caracteres"
            
        return True, None

import os
import dotenv
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from chromadb import PersistentClient

# Cargar variables de entorno
dotenv.load_dotenv()

# Configuración
class Config:
    EXCEL_PATH = "datasets/dataset_ejemplo.xlsx"
    EMBEDDING_MODEL = "text-embedding-3-large"
    CHROMA_DB_PATH = "./chroma_db"
    COLLECTION_NAME = "rag_collection"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    DEFAULT_SEARCH_K = 10
    DEFAULT_TEMPERATURE = 0.3
    LLM_MODEL = "gpt-3.5-turbo"

class DocumentLoader:
    """
    Maneja la carga de documentos desde diferentes fuentes.

    :return: Lista de objetos Document de LangChain al usar los métodos de carga
    """
    @staticmethod
    def load_excel_documents(excel_path):
        """
        Carga documentos desde un archivo Excel.

        :param excel_path: Ruta del archivo .xlsx con los datos de prestadores
        :return: Lista de Document con el contenido y metadatos de cada fila
        """
        try:
            df = pd.read_excel(excel_path)
            documents = []
            for idx, row in df.iterrows():
                text_content = " | ".join([
                    f"{col}: {str(val)}" 
                    for col, val in row.items() 
                    if pd.notna(val)
                ])  
                doc = Document(
                    page_content=text_content,
                    metadata={
                        "source": excel_path,
                        "row_index": idx,
                        "file_type": "excel"
                    }
                )
                documents.append(doc)   
            return documents
        except Exception as e:
            raise Exception(f"Error cargando archivo Excel {excel_path}: {str(e)}")

class VectorStoreManager:
    """
    Maneja la creación y carga de vectorstores.

    :param persist_directory: Directorio de persistencia para ChromaDB
    :param collection_name: Nombre de la colección (opcional)
    """
    def __init__(self, persist_directory, collection_name = None):
        self.persist_directory = persist_directory
        self.collection_name = collection_name or Config.COLLECTION_NAME
        self.embeddings = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
    
    def create_vectorstore(self, chunks):
        """
        Crea un vectorstore con ChromaDB a partir de chunks de documentos.

        :param chunks: Lista de Document ya segmentados
        :return: Instancia de Chroma inicializada con embeddings
        """
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            client = PersistentClient(path=self.persist_directory)
            return Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                client=client,
                collection_name=self.collection_name,
            )
        except Exception as e:
            raise Exception(f"Error creando vectorstore: {str(e)}")
    
    def load_existing_vectorstore(self):
        """
        Carga un vectorstore existente desde disco.

        :return: Instancia de Chroma conectada a la colección persistida
        """
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            client = PersistentClient(path=self.persist_directory)
            return Chroma(
                client=client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
        except Exception as e:
            raise Exception(f"Error cargando vectorstore existente: {str(e)}")

class PromptBuilder:
    """
    Construye prompts para diferentes tipos de consultas.
    """
    @staticmethod
    def get_search_prompt():
        """
        Construye un prompt optimizado para búsqueda de prestadores de salud.

        :return: Instancia de PromptTemplate configurada
        """
        template = """
        Eres un sistema de búsqueda de prestadores de salud.

        CONTEXTO DE PRESTADORES DISPONIBLES:
        {context}

        CONSULTA JSON: {question}

        INSTRUCCIONES:
        1. Extrae la especialidad médica del campo "medical_specialty" en el JSON de entrada
        2. Si hay múltiples especialidades, busca prestadores de TODAS ellas
        3. Busca en el CONTEXTO todos los prestadores que coincidan con la(s) especialidad(es)
        4. Muestra TODOS los prestadores encontrados
        5. Si no encuentras prestadores, responde: "No se encontraron resultados para esta búsqueda."

        FORMATO DE RESPUESTA:

        Para cada prestador encontrado, usa el siguiente formato con bullet points:

        • **Nombre:** [NOMBRE]  \n
        • **Especialidad:** [ESPECIALIDAD]  \n
        • **Teléfono:** [TELÉFONO]  \n
        • **Dirección:** [DIRECCIÓN]  \n
        • **Email:** [EMAIL]  \n
        • **Localidad:** [LOCALIDAD]  \n

        IMPORTANTE: 
        - Para múltiples prestadores, separa cada uno con una línea en blanco.

        RESPUESTA:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

class RAGProcessor:
    def __init__(self, persist_directory,
                 chunk_size = None, 
                 chunk_overlap = None,
                 search_k = None):
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        self.search_k = search_k or Config.DEFAULT_SEARCH_K
        self.vectorstore_manager = VectorStoreManager(persist_directory)
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
    
    def split_documents(self, documents):
        """
        Divide documentos en chunks para indexación.

        :param documents: Lista de Document con el contenido a dividir
        :return: Lista de Document segmentados
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(documents)
    
    def setup_vectorstore(self, documents = None, force_reload = False):
        """
        Configura el vectorstore (crear o cargar existente).

        :param documents: Lista de Document para crear el índice (si es necesario)
        :param force_reload: Forzar recreación del índice desde documentos
        :return: None
        """
        if not force_reload and os.path.exists(self.persist_directory):
            try:
                self.vectorstore = self.vectorstore_manager.load_existing_vectorstore()
                return
            except Exception as e:
                print(f"Error cargando vectorstore existente: {e}")
                print("Creando nuevo vectorstore...")
        if documents is None:
            raise ValueError("Se requieren documentos para crear un nuevo vectorstore")
        chunks = self.split_documents(documents)
        self.vectorstore = self.vectorstore_manager.create_vectorstore(chunks)
        print(f"Vectorstore creado con {len(chunks)} chunks")
    
    def setup_retriever(self, search_type = "similarity"):
        """
        Configura el retriever del vectorstore.

        :param search_type: Estrategia de búsqueda (por ejemplo, "similarity")
        :return: None
        """
        if self.vectorstore is None:
            raise Exception("Vectorstore no inicializado")
        self.retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": self.search_k}
        )
    
    def setup_qa_chain(self, temperature = None):
        """
        Configura la cadena de QA (LLM + retriever + prompt).

        :param temperature: Temperatura a usar en el LLM (opcional)
        :return: None
        """
        if self.retriever is None:
            raise Exception("Retriever no inicializado")
        llm = ChatOpenAI(
            model=Config.LLM_MODEL, 
            temperature=temperature or Config.DEFAULT_TEMPERATURE
        )
        prompt = PromptBuilder.get_search_prompt()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
    
    def query(self, question):
        """
        Realiza una consulta al sistema RAG y devuelve la respuesta.

        :param question: Consulta en formato texto o JSON
        :return: Diccionario con 'answer' y 'source_documents'
        """
        if self.qa_chain is None:
            raise Exception("Sistema RAG no configurado completamente")
        try:
            # Verificar si hay documentos relevantes
            relevant_docs = self._get_relevant_documents(question)
            if not relevant_docs:
                return {
                    "answer": "No se encontraron resultados para esta búsqueda.",
                    "source_documents": []
                }
            result = self.qa_chain.invoke({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result.get("source_documents", [])
            }
        except Exception as e:
            print(f"Error en consulta RAG: {e}")
            raise Exception(f"Error en consulta RAG: {str(e)}")
    
    def query_with_specific_docs(self, question, specific_docs=None):
        """
        Realiza una consulta usando únicamente los documentos especificados.

        :param question: Consulta en formato texto o JSON
        :param specific_docs: Lista de Document relevantes (opcional)
        :return: Diccionario con 'answer' y 'source_documents'
        """
        if specific_docs:
            # Usar documentos específicos con el prompt existente
            context = "\n\n".join([doc.page_content for doc in specific_docs])
            prompt = PromptBuilder.get_search_prompt()
            formatted_prompt = prompt.format(context=context, question=question)
            
            # Usar solo el LLM sin retriever
            llm = ChatOpenAI(model=Config.LLM_MODEL, temperature=Config.DEFAULT_TEMPERATURE)
            response = llm.invoke(formatted_prompt)
            return {
                "answer": response.content,
                "source_documents": specific_docs
            }
        else:
            # Usar flujo normal con retriever
            return self.query(question)
    
    def _get_relevant_documents(self, question):
        """
        Obtiene documentos relevantes usando el retriever configurado.

        :param question: Consulta a evaluar
        :return: Lista de Document relevantes o vacía si falla
        """
        try:
            return self.retriever.invoke(question)
        except Exception:
            try:
                return self.retriever.get_relevant_documents(question)
            except Exception:
                return []

def setup_rag_from_excel(excel_path, persist_directory,force_reload= False):
    """
    Configura el sistema RAG a partir de un archivo Excel y un directorio de persistencia.

    :param excel_path: Ruta al archivo .xlsx base
    :param persist_directory: Directorio para persistir ChromaDB
    :param force_reload: Si True, vuelve a crear el índice desde el Excel
    :return: Instancia de RAGProcessor inicializada
    """
    processor = RAGProcessor(persist_directory=persist_directory)
    # Cargar documentos solo si es necesario
    documents = None
    if force_reload or not os.path.exists(persist_directory):
        documents = DocumentLoader.load_excel_documents(excel_path)
    # Configurar componentes
    processor.setup_vectorstore(documents, force_reload)
    processor.setup_retriever()
    processor.setup_qa_chain()
    return processor

class SearchService:
    """
    Servicio principal para búsquedas.
    
    :param excel_path: Ruta al .xlsx de datos (opcional)
    :param persist_directory: Directorio de persistencia de ChromaDB (opcional)
    """
    def __init__(self, excel_path = None, persist_directory = None):
        self.excel_path = excel_path or Config.EXCEL_PATH
        self.persist_directory = persist_directory or Config.CHROMA_DB_PATH
        self.processor = None
        self._initialize()
    
    def _initialize(self):
        """
        Inicializa el procesador RAG.

        :return: None
        """
        self.processor = setup_rag_from_excel(
            excel_path=self.excel_path,
            persist_directory=self.persist_directory,
            force_reload=True
        )
    
    def search(self, query):
        """
        Busca prestadores de salud basado en JSON con el campo medical_specialty.

        :param query: String o dict con la consulta (incluye medical_specialty)
        :return: Texto con la respuesta formateada o mensaje de error
        """
        try:
            print(f"Consulta recibida: {query}")
            
            # Extraer especialidad del JSON para hacer búsquedas más específicas
            specialty_queries = self._extract_specialty_queries(query)
            print(f"Consultas por especialidad: {specialty_queries}")
            
            # Recopilar documentos basados en especialidades
            all_docs = self._collect_documents_by_specialty(specialty_queries)
            print(f"Documentos encontrados: {len(all_docs)}")
            
            # Si no se encontraron documentos específicos, usar búsqueda general
            if not all_docs:
                print("No se encontraron documentos específicos, usando búsqueda general...")
                all_docs = self._general_search()
            
            if not all_docs:
                return "No se encontraron resultados para esta búsqueda."
            
            # Usar el processor con documentos específicos
            result = self.processor.query_with_specific_docs(query, all_docs)
            return result["answer"]
        except Exception as e:
            print(f"Error en búsqueda: {e}")
            return f"Error en búsqueda: {str(e)}"
    
    def _extract_specialty_queries(self, query):
        """
        Extrae especialidades del JSON de entrada y crea consultas específicas.

        :param query: Cadena o dict con la consulta original
        :return: Lista de términos de búsqueda por especialidad
        """
        import json
        import re
        
        specialty_queries = []
        
        try:
            # Intentar parsear como JSON
            if isinstance(query, str):
                # Limpiar el string para que sea JSON válido
                cleaned_query = re.sub(r'[\n\r\t]', '', query.strip())
                if cleaned_query.startswith('{') and cleaned_query.endswith('}'):
                    json_data = json.loads(cleaned_query)
                else:
                    # Si no es JSON, buscar el patrón medical_specialty
                    specialty_match = re.search(r'"medical_specialty":\s*"([^"]+)"', cleaned_query)
                    if specialty_match:
                        json_data = {"medical_specialty": specialty_match.group(1)}
                    else:
                        json_data = {}
            else:
                json_data = query if isinstance(query, dict) else {}
            
            # Extraer especialidades
            if "medical_specialty" in json_data:
                specialty = json_data["medical_specialty"]
                if isinstance(specialty, str):
                    specialties = [s.strip().upper() for s in specialty.split(',')]
                elif isinstance(specialty, list):
                    specialties = [s.strip().upper() for s in specialty]
                else:
                    specialties = [str(specialty).strip().upper()]
                
                # Crear consultas específicas por especialidad
                for spec in specialties:
                    if spec:
                        specialty_queries.append(spec)
                        specialty_queries.append(f"especialidad {spec}")
                        specialty_queries.append(f"prestadores {spec}")
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error procesando JSON: {e}")
            # Si falla el parsing, usar la consulta original
            specialty_queries.append(str(query))
        
        # Si no se encontraron especialidades, usar consulta original
        if not specialty_queries:
            specialty_queries.append(str(query))
        
        return specialty_queries
    
    def _collect_documents_by_specialty(self, specialty_queries):
        """
        Recopila documentos basados en las especialidades extraídas.

        :param specialty_queries: Lista de términos de búsqueda por especialidad
        :return: Lista de Document relevantes (máx. 15)
        """
        all_docs = []
        seen_docs = set()
        
        for query in specialty_queries:
            try:
                docs = self.processor.retriever.invoke(query)
                print(f"Especialidad '{query}': {len(docs)} documentos")
                
                for doc in docs:
                    doc_id = f"{doc.metadata.get('row_index', '')}-{doc.page_content[:100]}"
                    if doc_id not in seen_docs:
                        all_docs.append(doc)
                        seen_docs.add(doc_id)
                        
            except Exception as e:
                print(f"Error buscando especialidad '{query}': {e}")
        
        return all_docs[:15]  # Limitar a 15 documentos
    
    def _general_search(self):
        """
        Ejecuta una búsqueda general cuando no hay especialidades específicas.

        :return: Lista de Document relevantes (máx. 15)
        """
        general_queries = [
            "prestadores de salud",
            "médicos",
            "especialistas",
            "doctores"
        ]
        
        all_docs = []
        seen_docs = set()
        
        for query in general_queries:
            try:
                docs = self.processor.retriever.invoke(query)
                print(f"Búsqueda general '{query}': {len(docs)} documentos")
                
                for doc in docs:
                    doc_id = f"{doc.metadata.get('row_index', '')}-{doc.page_content[:100]}"
                    if doc_id not in seen_docs:
                        all_docs.append(doc)
                        seen_docs.add(doc_id)
                
                # Si encontramos documentos, salir del bucle
                if all_docs:
                    break
                    
            except Exception as e:
                print(f"Error en búsqueda general '{query}': {e}")
        
        return all_docs[:15]

# Instancia global del servicio
_health_service = None

def get_health_service():
    """
    Obtiene la instancia singleton del servicio de salud.

    :return: Instancia de SearchService
    """
    global _health_service
    if _health_service is None:
        _health_service = SearchService()
    return _health_service

def query_contacts_with_langchain(input_text):
    """
    Función de compatibilidad para consultar prestadores.

    :param input_text: Consulta en formato texto o JSON
    :return: Respuesta formateada con la lista de prestadores
    """
    service = get_health_service()
    return service.search(input_text)

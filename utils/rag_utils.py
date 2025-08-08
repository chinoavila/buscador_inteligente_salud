import os
import importlib
import dotenv
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# Importación dinámica: usar langchain-chroma si está disponible; si no, caer a community
_USING_LC_CHROMA = importlib.util.find_spec("langchain_chroma") is not None
if _USING_LC_CHROMA:
    Chroma = importlib.import_module("langchain_chroma").Chroma
else:
    from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from chromadb import PersistentClient
from chromadb.config import Settings

# Cargar variables de entorno
dotenv.load_dotenv()

# Configuración global
EXCEL_PATH = "datasets/dataset_ejemplo.xlsx"
EMBEDDING_MODEL = "text-embedding-3-large"
CHROMA_DB_PATH = "./chroma_db"

class RAGProcessor:
    """ Clase para manejar el procesamiento RAG con ChromaDB """
    def __init__(self, persist_directory, chunk_size=1000, chunk_overlap=100,
                 search_k: int | None = None, score_threshold: float | None = None):
        """Inicializar el procesador RAG"""
        self.persist_directory = persist_directory
        self.collection_name = "rag_collection"
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = EMBEDDING_MODEL
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        # Parametrización del recuperador
        try:
            env_k = int(os.getenv("RAG_TOP_K", "8"))
        except Exception:
            env_k = 8
        try:
            env_thr = float(os.getenv("RAG_SCORE_THRESHOLD", "0.5"))
        except Exception:
            env_thr = 0.5
        self.search_k = search_k if search_k is not None else env_k
        self.score_threshold = score_threshold if score_threshold is not None else env_thr
    # Asegurar desactivación de telemetría por entorno
    os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
    os.environ.setdefault("CHROMA_TELEMETRY_ANONYMIZED", "False")
    os.environ.setdefault("CHROMA_TELEMETRY_ENABLED", "False")
    os.environ.setdefault("CHROMA_TELEMETRY_IMPLEMENTATION", "noop")
    os.environ.setdefault("CHROMA_DISABLE_TELEMETRY", "true")
    os.environ.setdefault("POSTHOG_DISABLED", "true")
    os.environ.setdefault("DO_NOT_TRACK", "1")
        
    def load_excel_documents(self, excel_path):
        """ Cargar documentos desde un archivo Excel """
        try:
            df = pd.read_excel(excel_path)
            documents = []
            for idx, row in df.iterrows():
                # Crear texto combinando todas las columnas
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
    
    def split_documents(self, documents):
        """ Dividir documentos en chunks más pequeños """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return text_splitter.split_documents(documents)
    
    def create_vectorstore(self, chunks):
        """ Crear vectorstore con ChromaDB """
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
            # Desactivar telemetría para evitar logs de errores en entornos sin PostHog
            client = PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            if _USING_LC_CHROMA:
                self.vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    client=client,
                    collection_name=self.collection_name,
                )
            else:
                # Firma de la versión legacy usa 'embedding'
                self.vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=self.embeddings,
                    client=client,
                    collection_name=self.collection_name,
                )
            return self.vectorstore 
        except Exception as e:
            raise Exception(f"Error creando vectorstore: {str(e)}")
    
    def load_existing_vectorstore(self):
        """ Cargar un vectorstore existente desde disco """
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
            # Desactivar telemetría para evitar logs de errores en entornos sin PostHog
            client = PersistentClient(
                path=self.persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            self.vectorstore = Chroma(
                client=client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
            return self.vectorstore    
        except Exception as e:
            raise Exception(f"Error cargando vectorstore existente: {str(e)}")
    
    def create_retriever(self, search_type: str | None = None, search_kwargs=None):
        """ Crear retriever a partir del vectorstore """
        if self.vectorstore is None:
            raise Exception("Vectorstore no inicializado.")
        # Por defecto usamos umbral de similitud para evitar ruido y alucinaciones
        if search_type is None:
            search_type = "similarity_score_threshold"
        if search_kwargs is None:
            if search_type == "similarity_score_threshold":
                search_kwargs = {"k": self.search_k, "score_threshold": self.score_threshold}
            else:
                search_kwargs = {"k": self.search_k}
        self.retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        return self.retriever
    
    def create_qa_chain(self, temperature: float | None = None):
        """ Crear cadena de QA con recuperación """
        if self.retriever is None:
            raise Exception("Retriever no inicializado.") 
        try:
            # Temperatura 0 por defecto para respuestas deterministas
            if temperature is None:
                try:
                    temperature = float(os.getenv("RAG_TEMPERATURE", "0"))
                except Exception:
                    temperature = 0
            llm_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)
            
            # Prompt personalizado para búsqueda de prestadores de salud
            custom_prompt = PromptTemplate(
                template="""
                Eres un asistente especializado en búsqueda de contactos de prestadores de salud.
                SOLO puedes responder usando citas textuales del CONTEXTO. 
                Si la información solicitada no está en el contexto o no hay coincidencias relevantes, responde exactamente: "No se encontraron resultados para esta búsqueda."
                CONTEXTO:
                {context}
                PREGUNTA: {question}
                Reglas estrictas:
                - No alucines ni completes datos faltantes.
                - Usa únicamente los campos presentes (nombre, especialidad, teléfono, dirección, etc.).
                - Si los datos del contexto están en inglés, traducelos al español antes de hacer la búsqueda.
                Responde de forma clara, en español, y solo con información respaldada por el contexto.
                """,
                input_variables=["context", "question"]
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm_model,
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": custom_prompt}
            )
            return self.qa_chain
        except Exception as e:
            raise Exception(f"Error creando cadena QA: {str(e)}")
    
    def query(self, question):
        """ Realizar consulta al sistema RAG """
        if self.qa_chain is None:
            raise Exception("Cadena QA no inicializada.")
        try:
            # Pre-chequeo: si no hay documentos relevantes por umbral, no preguntar al LLM
            relevant_docs = []
            try:
                # En LangChain modernos el retriever es Runnable
                relevant_docs = self.retriever.invoke(question)
            except Exception:
                try:
                    relevant_docs = self.retriever.get_relevant_documents(question)
                except Exception:
                    relevant_docs = []
            if not relevant_docs:
                return {
                    "answer": "No se encontraron resultados para esta búsqueda.",
                    "source_documents": []
                }

            # LangChain >= 0.1: usar invoke en lugar de __call__
            result = self.qa_chain.invoke({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result.get("source_documents", [])
            }
        except Exception as e:
            raise Exception(f"Error en consulta RAG: {str(e)}")


def setup_rag_from_excel(excel_path, persist_directory, force_reload=False):
    """ Función utilitaria para configurar RAG desde archivo Excel """
    # Permitir forzar recarga vía variable de entorno (útil tras actualizar Chroma/índices)
    if os.getenv("RAG_FORCE_RELOAD") in {"1", "true", "True", "yes"}:
        force_reload = True
    processor = RAGProcessor(persist_directory=persist_directory)
    # Verificar si ya existe un vectorstore y no se fuerza la recarga
    if os.path.exists(persist_directory) and not force_reload:
        try:
            processor.load_existing_vectorstore()
            processor.create_retriever()
            processor.create_qa_chain()
            return processor
        except Exception:
            # Si falla cargar el existente, crear uno nuevo
            pass
    # Crear nuevo vectorstore desde Excel
    documents = processor.load_excel_documents(excel_path)
    chunks = processor.split_documents(documents)
    processor.create_vectorstore(chunks)
    processor.create_retriever()
    processor.create_qa_chain()
    return processor

# Inicializar el procesador RAG global
rag_processor = setup_rag_from_excel(
            excel_path=EXCEL_PATH,
            persist_directory=CHROMA_DB_PATH,
            force_reload=False
        )

def query_contacts_with_langchain(input_text):
    """ Función específica para consultar prestadores por especialidades """
    try:
        print(input_text)
        # Mejorar la consulta para ser más específica
        query = f"""
        Busca prestadores de salud con las siguientes especialidades: {input_text}
        Proporciona una lista estructurada de contactos que incluya:
        - Nombre del profesional o institución
        - Especialidad médica
        - Número de teléfono
        - Dirección o ubicación
        - Cualquier información adicional de contacto disponible 
        Organiza la información de manera clara y legible.
        """
        print(query)
        result = rag_processor.query(query)
        return result["answer"]
    except Exception as e:
        return f"Error en consulta: {str(e)}"

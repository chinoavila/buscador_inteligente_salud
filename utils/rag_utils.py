import dotenv
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
import os

# Cargar variables de entorno
dotenv.load_dotenv()

# Configuración global
EXCEL_PATH = "datasets/INSTITUCIONES_ACLISA_JULIO.xlsx"
CHROMA_DB_PATH = "./chroma_db"

class RAGProcessor:
    """ Clase para manejar el procesamiento RAG con ChromaDB """
    def __init__(self, persist_directory="./chroma_db", chunk_size=1000, chunk_overlap=100):
        """ Inicializar el procesador RAG """
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        
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
    
    def create_vectorstore(self, chunks, embedding_model="text-embedding-3-large"):
        """ Crear vectorstore con ChromaDB """
        try:
            self.embeddings = OpenAIEmbeddings(model=embedding_model)
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            return self.vectorstore 
        except Exception as e:
            raise Exception(f"Error creando vectorstore: {str(e)}")
    
    def load_existing_vectorstore(self, embedding_model="text-embedding-3-large"):
        """ Cargar un vectorstore existente desde disco """
        try:
            if not os.path.exists(self.persist_directory):
                raise Exception(f"No existe el directorio {self.persist_directory}")  
            self.embeddings = OpenAIEmbeddings(model=embedding_model)
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            return self.vectorstore    
        except Exception as e:
            raise Exception(f"Error cargando vectorstore existente: {str(e)}")
    
    def create_retriever(self, search_kwargs=None):
        """ Crear retriever a partir del vectorstore """
        if self.vectorstore is None:
            raise Exception("Vectorstore no inicializado. Llame a create_vectorstore() primero.")
        if search_kwargs is None:
            search_kwargs = {"k": 4}  # Retorna los 4 documentos más relevantes   
        self.retriever = self.vectorstore.as_retriever(search_kwargs=search_kwargs)
        return self.retriever
    
    def create_qa_chain(self, llm_model_name="gpt-3.5-turbo", temperature=0):
        """ Crear cadena de QA con recuperación """
        if self.retriever is None:
            raise Exception("Retriever no inicializado. Llame a create_retriever() primero.") 
        try:
            llm_model = ChatOpenAI(model=llm_model_name, temperature=temperature)
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm_model,
                retriever=self.retriever,
                return_source_documents=True
            )
            return self.qa_chain
        except Exception as e:
            raise Exception(f"Error creando cadena QA: {str(e)}")
    
    def query(self, question):
        """ Realizar consulta al sistema RAG """
        if self.qa_chain is None:
            raise Exception("Cadena QA no inicializada. Llame a create_qa_chain() primero.")
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result.get("source_documents", [])
            }
        except Exception as e:
            raise Exception(f"Error en consulta RAG: {str(e)}")


def setup_rag_from_excel(excel_path, persist_directory="./chroma_db", force_reload=False):
    """ Función utilitaria para configurar RAG desde archivo Excel """
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
            force_reload=None
        )

def query_contacts_with_langchain(input_text, excel_path="datasets/INSTITUCIONES_ACLISA_JULIO.xlsx"):
    """ Función específica para consultar profesionales por especialidades """
    try:
        query = f'''Dame una lista de contactos de todos los profesionales
                    cuyas especialidades se encuentren en este JSON: {input_text}.
                    Por favor incluye nombre, especialidad, teléfono y dirección cuando esté disponible.'''
        result = rag_processor.query(query)
        return result["answer"]
    except Exception as e:
        return f"Error en consulta: {str(e)}"

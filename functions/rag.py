# %pip install --quiet --upgrade langchain-text-splitters langchain-community langgraph
# pip install -qU "langchain[openai]"
# pip install -qU langchain-chroma  o  pip install chromadb

import dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import init_chat_model
from langchain.chains import RetrievalQA

# tomar API Key de OPENAI desde archivo .env
dotenv.load_dotenv()

# https://python.langchain.com/docs/tutorials/rag/
# https://medium.com/@callumjmac/implementing-rag-in-langchain-with-chroma-a-step-by-step-guide-16fc21815339

# 1. Cargar documentos
# https://www.apsfsa.com.ar/prestadores
# https://www.saludintegralweb.com/prestadores
# https://www.hacfsa.gob.ar/servicios/
# https://sisa.msal.gov.ar/sisa/#sisa
loader = TextLoader("tus_documentos.txt")
documents = loader.load()

# 2. Chunking para dividir texto en fragmentos pequeños
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# 3. Crear embeddings y almacenar en FAISS
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Crear el retriever
retriever = vectorstore.as_retriever()

# 5. Crear el modelo de QA con recuperación
llm_model = init_chat_model("gpt-4o-mini", model_provider="openai")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm_model,
    retriever=retriever,
    return_source_documents=True
)

def rag_query(text):
    query = f"¿Qué profesionales puedo consultar si presento los siguientes sintomas: {text}?"
    result = qa_chain({"query": text})
    return result["result"]


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

def ingest_documents(path):

    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()

    vector_db = FAISS.from_documents(chunks, embeddings)

    vector_db.save_local("rag/vectorstore")

    print("Vector DB created successfully")

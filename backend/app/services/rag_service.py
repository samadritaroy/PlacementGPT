from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_service import create_vector_store
from app.services.vector_service import search_chunks

documents = []

def create_chunks(text, filename):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    global documents
    documents = chunks

    create_vector_store(
        chunks,
        filename
    )

    return len(chunks)

def get_relevant_chunks(question):

    return search_chunks(question)
    
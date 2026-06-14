from app.services.rag_service import create_chunks
from app.services.rag_service import get_relevant_chunks
from app.services.llm_service import ask_llama
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from app.services.document_service import (
    extract_text_from_pdf,
    extract_text_from_docx
)
import os
class QuestionRequest(BaseModel):
    question: str
app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "PlacementGPT Backend Running Successfully!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/upload-document")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if file.filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.lower().endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return {
            "error": "Only PDF and DOCX files are supported"
        }

    chunks = create_chunks(
        text,
        file.filename
    )

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks_created": chunks
    }
@app.get("/test-llm")
def test_llm():

    answer = ask_llama(
        "Explain database in one sentence."
    )

    return {
        "response": answer
    }
@app.post("/ask")
def ask_question(data: QuestionRequest):

    result = get_relevant_chunks(
        data.question
    )
    context = result["context"]
    sources = result["sources"]

    prompt = f"""
    Context:
    {context}

    Question:
    {data.question}

    Answer based only on the context.
    """

    answer = ask_llama(prompt)

    return {
        "answer": answer,
        "sources": sources
    }
    try:
        text = extract_text_from_pdf(file_path)
    except Exception as e:
        return {
        "error": str(e),
        "file": file.filename
        }

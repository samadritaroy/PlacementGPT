from app.services.rag_service import create_chunks
from app.services.rag_service import get_relevant_chunks
from app.services.llm_service import ask_llama
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from app.services.resume_service import extract_skills
from app.services.resume_analysis_service import analyze_resume
from app.services.mock_interview_service import (
    start_mock_interview,
    continue_interview,
    end_interview_with_feedback
)
from app.services.roadmap_service import (
    generate_dsa_roadmap
)
from app.services.interview_service import (
    get_questions
)
from app.services.ats_service import (
    generate_skill_gap_report
)
from app.services.ats_service import (
    save_resume_skills,
    get_resume_skills,
    calculate_ats_score
)
from app.services.document_service import (
    extract_text_from_pdf,
    extract_text_from_docx
)
from app.services.interview_service import (
    generate_interview_questions
)
import os
class StartInterviewRequest(BaseModel):
    session_type: str = "technical"
    company: str | None = None
    role: str | None = None
    difficulty: str = "medium"


class ContinueInterviewRequest(BaseModel):
    session_id: str
    answer: str


class EndInterviewRequest(BaseModel):
    session_id: str
class RoadmapRequest(
    BaseModel
):

    target_role: str
class InterviewRequest(
    BaseModel
):

    difficulty: str = "mixed"
class QuestionRequest(BaseModel):
    question: str
app = FastAPI()

class ATSRequest(
    BaseModel
):

    job_description: str
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
@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if file.filename.lower().endswith(".pdf"):

        text = extract_text_from_pdf(
            file_path
        )

    elif file.filename.lower().endswith(".docx"):

        text = extract_text_from_docx(
            file_path
        )

    else:

        return {
            "error": "Only PDF and DOCX supported"
        }

    skills = extract_skills(text)
    print("Extracted Skills:", skills)
    analysis = analyze_resume(
        text,
        skills
    )
    save_resume_skills(
        skills
    )
    return {
    "filename": file.filename,
    "skills": skills,
    "skills_found": len(skills),
    "analysis": analysis
    }
@app.post("/ats-score")
def ats_score(
    data: ATSRequest
):

    resume_skills = get_resume_skills()

    jd_skills = extract_skills(
        data.job_description
    )

    result = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    return result
@app.post("/skill-gap")
def skill_gap(
    data: ATSRequest
):

    resume_skills = get_resume_skills()

    jd_skills = extract_skills(
        data.job_description
    )

    ats_result = calculate_ats_score(
        resume_skills,
        jd_skills
    )

    result = generate_skill_gap_report(
        ats_result
    )

    return result
@app.post(
    "/interview-questions"
)
def interview_questions(
    data: InterviewRequest
):
    print("Resume Skills:", get_resume_skills())
    skills = get_resume_skills()

    questions = (
        generate_interview_questions(
            skills,
            data.difficulty
        )
    )

    return {
        "skills": skills,
        "difficulty": data.difficulty,
        "questions": questions
    }
@app.get("/saved-questions")
def saved_questions():

    return {
        "questions": get_questions()
    }
@app.get("/dsa-roadmap")
def dsa_roadmap():

    roadmap = generate_dsa_roadmap()

    return {
        "roadmap": roadmap
    }
@app.post("/mock-interview/start")
def start_interview(
    data: StartInterviewRequest
):

    result = start_mock_interview(
        session_type=data.session_type,
        company=data.company,
        role=data.role,
        difficulty=data.difficulty
    )

    return result
@app.post("/mock-interview/continue")
def continue_interview_route(
    data: ContinueInterviewRequest
):

    result = continue_interview(
        session_id=data.session_id,
        user_message=data.answer
    )

    return result
@app.post("/mock-interview/end")
def end_interview(
    data: EndInterviewRequest
):

    result = end_interview_with_feedback(
        data.session_id
    )

    return result
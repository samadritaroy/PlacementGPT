from fastapi.middleware.cors import CORSMiddleware
from app.services.rag_service import create_chunks
from app.services.rag_service import get_relevant_chunks
from app.services.llm_service import ask_llama
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from app.services.resume_service import extract_skills
from app.services.resume_analysis_service import analyze_resume
from app.services.company_prep_service import (
    get_company_list,
    get_company_profile,
    generate_prep_guide,
    get_common_questions,
    generate_mock_question
)
from app.services.dsa_service import (
    generate_dsa_question,
    get_dsa_hint,
    get_dsa_solution,
    evaluate_dsa_answer
)
from app.services.answer_evaluator_service import (
    evaluate_answer
)
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
from app.services.auth_service import (
    signup_user,
    login_user
)
import os
class AuthRequest(BaseModel):
    email: str
    password: str
class CompanyPrepRequest(BaseModel):
    company: str
    role: str = "Software Engineer"
    experience: str = "fresher"
    weeks_available: int = 8
class CompanyMockQuestionRequest(BaseModel):
    company: str
    question_type: str
    role: str = "Software Engineer"
class DSAQuestionRequest(BaseModel):
    topic: str
    difficulty: str = "easy"
class DSAHintRequest(BaseModel):
    topic: str
    difficulty: str
    question_id: str
class DSAEvaluationRequest(BaseModel):
    question: str
    answer: str
class AnswerEvaluationRequest(
    BaseModel
):
    question: str
    answer: str
    question_type: str = "technical"
    company: str | None = None
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
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.post("/evaluate-answer")
def evaluate_candidate_answer(
    data: AnswerEvaluationRequest
):

    result = evaluate_answer(
        question=data.question,
        answer=data.answer,
        question_type=data.question_type,
        company=data.company
    )

    return result
@app.post("/dsa/generate")
def generate_question(
    data: DSAQuestionRequest
):
    return generate_dsa_question(
        topic=data.topic,
        difficulty=data.difficulty
    )
@app.post("/dsa/hint")
def get_hint(
    data: DSAHintRequest
):
    return get_dsa_hint(
        topic=data.topic,
        difficulty=data.difficulty,
        question_id=data.question_id
    )
@app.post("/dsa/solution")
def get_solution(
    data: DSAHintRequest
):
    return get_dsa_solution(
        topic=data.topic,
        difficulty=data.difficulty,
        question_id=data.question_id
    )
@app.post("/dsa/evaluate")
def evaluate_solution(
    data: DSAEvaluationRequest
):
    return evaluate_dsa_answer(
        question=data.question,
        answer=data.answer
    )
@app.get("/company-prep/companies")
def list_companies():
    return get_company_list()
@app.post("/company-prep")
def company_prep(
    data: CompanyPrepRequest
):
    return {
        "company_profile": get_company_profile(
            data.company
        ),

        "preparation_guide": generate_prep_guide(
            company=data.company,
            role=data.role,
            experience=data.experience,
            weeks_available=data.weeks_available
        ),

        "common_questions": get_common_questions(
            data.company
        )
    }
@app.post("/company-prep/mock-question")
def company_mock_question(
    data: CompanyMockQuestionRequest
):
    return generate_mock_question(
        company=data.company,
        question_type=data.question_type,
        role=data.role
    )
@app.post("/auth/signup")
def signup(
    data: AuthRequest
):
    result = signup_user(
        data.email,
        data.password
    )

    return {
        "message": "Signup successful",
        "user": result.user.email if result.user else None
    }
@app.post("/auth/login")
def login(
    data: AuthRequest
):
    result = login_user(
        data.email,
        data.password
    )

    return {
        "message": "Login successful",
        "access_token": (
            result.session.access_token
            if result.session
            else None
        )
    }
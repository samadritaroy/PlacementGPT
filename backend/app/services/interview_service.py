from app.services.llm_service import ask_llama
import time
stored_questions = ""
def save_questions(questions):

    global stored_questions

    stored_questions = questions


def get_questions():

    return stored_questions
def generate_interview_questions(
    skills,
    difficulty="mixed"
):

    skill_text = ", ".join(skills[:5])

    prompt = f"""
    You are a technical interviewer.

    Candidate Skills:
    {skill_text}

    Generate interview questions.

    Difficulty:
    {difficulty}

    Rules:
    - Focus on the candidate's skills.
    - Include theory and practical questions.
    - Include coding questions where applicable.
    - Return only numbered questions.
    - Number each question.

    Return only the questions.
    """

    start = time.time()
    print("Skills sent:", skills)
    response = ask_llama(
    prompt)
    
    save_questions(response)
    print(
        "Interview Generation Time:",
        round(time.time() - start, 2),
        "seconds"
    )

    return response
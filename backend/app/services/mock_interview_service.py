"""
Mock Interview Service
Multi-turn AI interview with Llama3.
Supports: Technical, HR, DSA, System Design rounds.
Company-specific prompts for Amazon, Google, TCS, Infosys, Wipro.
"""

from app.services.llm_service import ask_llm_with_history
from app.services.chat_history_service import (
    create_session, add_message, get_history
)
from typing import Optional

# ── Company-Specific Instructions ─────────────────────────────────────────────
COMPANY_CONTEXT = {
    "Amazon": """You are interviewing for Amazon. Focus on LEADERSHIP PRINCIPLES in every answer.
Weave these into your questions: Customer Obsession, Ownership, Invent and Simplify,
Bias for Action, Frugality, Earn Trust, Dive Deep, Deliver Results.
After behavioral answers, ask "Tell me more about what YOU specifically did." (Amazon probes deeply.)""",

    "Google": """You are interviewing for Google. Focus on:
- Problem-solving PROCESS (think aloud), not just the answer
- Optimal algorithmic solutions (always ask: can you do better?)
- One system design question for SDE roles
- Googliness: collaboration, communication, intellectual humility""",

    "Microsoft": """You are interviewing for Microsoft. Focus on:
- OOP design patterns and SOLID principles
- Growth mindset questions ("Tell me about a time you failed and what you learned")
- Azure/cloud awareness for tech roles
- Collaboration and empathy""",

    "TCS": """You are interviewing for TCS (Tata Consultancy Services). This is a campus placement.
Keep questions at BE/BTech freshers level. Focus on:
- Java/Python basics, OOPS concepts
- SQL queries (JOINs, GROUP BY, subqueries)
- OS basics (process vs thread, scheduling)
- One easy coding problem (array, string, number pattern)
- HR: willingness to relocate, 2-year bond acceptance""",

    "Infosys": """You are interviewing for Infosys campus placement. Keep at freshers level:
- OOPS: inheritance, polymorphism, encapsulation with real examples
- SQL: second highest salary, department-wise aggregations
- Pseudo-code/logic questions (not actual compilation)
- HR: adaptability, teamwork, learning attitude""",

    "Wipro": """You are interviewing for Wipro campus placement. Freshers level:
- Core CS fundamentals (OS, DBMS, Networks, OOP)
- One simple coding problem
- HR round with standard questions
- Friendly tone, less pressure than product companies""",

    "Flipkart": """You are interviewing for Flipkart. Focus on:
- Strong DSA (similar to Amazon/Google difficulty)
- System design for e-commerce at scale
- Problem-solving and optimization mindset""",
}

# ── Session Type Configs ──────────────────────────────────────────────────────
SESSION_CONFIGS = {
    "technical": {
        "num_questions": 5,
        "focus": "Data structures, algorithms, OOP, DBMS, OS, Computer Networks",
        "tone": "Professional and challenging"
    },
    "hr": {
        "num_questions": 6,
        "focus": "Behavioral questions using STAR method, motivation, goals, cultural fit",
        "tone": "Warm and conversational but professional"
    },
    "dsa": {
        "num_questions": 3,
        "focus": "Coding problems — ask for approach first, then code, then optimize",
        "tone": "Technical and precise"
    },
    "system_design": {
        "num_questions": 2,
        "focus": "High-level system design — scalability, databases, APIs, caching",
        "tone": "Senior/collaborative, explore trade-offs"
    }
}


def _build_system_prompt(
    session_type: str,
    company: Optional[str],
    role: Optional[str],
    difficulty: str
) -> str:
    config = SESSION_CONFIGS.get(session_type, SESSION_CONFIGS["technical"])
    company_ctx = COMPANY_CONTEXT.get(company, "") if company else ""
    
    base = f"""You are a senior interviewer conducting a REALISTIC mock interview.

INTERVIEW DETAILS:
- Type: {session_type.upper()} Round
- Company: {company or "Top Tech Company"}
- Role: {role or "Software Engineer"}
- Difficulty: {difficulty}
- Questions to ask: {config["num_questions"]}
- Focus areas: {config["focus"]}
- Your tone: {config["tone"]}

{company_ctx}

YOUR RULES:
1. Ask exactly ONE question at a time. Never ask two questions together.
2. After each answer:
   a. Briefly acknowledge what was good (1 sentence)
   b. Ask a pointed follow-up OR move to the next question
3. For coding questions: ask for APPROACH first (time/space complexity), then code
4. If they're stuck: give ONE small hint, not the full answer
5. After all questions: give a brief overall feedback (3-4 lines)
6. DO NOT break character. Stay as the interviewer throughout.

Start by introducing yourself in ONE sentence and asking the FIRST question ONLY."""

    return base


def start_mock_interview(
    session_type: str = "technical",
    company: Optional[str] = None,
    role: Optional[str] = None,
    difficulty: str = "medium"
) -> dict:
    """
    Start a new mock interview session.
    Returns session_id + opening message from the interviewer.
    """
    session_id = create_session(session_type=session_type, company=company)
    system_prompt = _build_system_prompt(session_type, company, role, difficulty)
    
    # Store system prompt in session (as first "system" message)
    add_message(session_id, "system", system_prompt)
    
    # Get opening from AI
    messages = [{"role": "system", "content": system_prompt}]
    opening = ask_llm_with_history(messages, temperature=0.5, max_tokens=400)
    
    add_message(session_id, "assistant", opening)
    
    return {
        "session_id": session_id,
        "opening_message": opening,
        "company": company,
        "role": role,
        "session_type": session_type,
        "difficulty": difficulty,
    }


def continue_interview(session_id: str, user_message: str) -> dict:
    """
    Send user's answer and get next interviewer response.
    Maintains full conversation context.
    """
    # Save user message
    add_message(session_id, "user", user_message)
    
    # Get full history (includes system prompt)
    history = get_history(session_id)
    
    # Get AI response
    ai_response = ask_llm_with_history(history, temperature=0.5, max_tokens=600)
    
    # Save AI response
    add_message(session_id, "assistant", ai_response)
    
    return {
        "session_id": session_id,
        "response": ai_response,
        "message_count": len([m for m in history if m["role"] == "user"]),
    }


def end_interview_with_feedback(session_id: str) -> dict:
    """
    End the interview and get comprehensive feedback.
    """
    history = get_history(session_id)
    
    # Count Q&A pairs
    user_messages  = [m for m in history if m["role"] == "user"]
    ai_messages    = [m for m in history if m["role"] == "assistant"]
    
    # Build feedback prompt
    conversation_text = ""
    for msg in history[1:]:  # skip system prompt
        prefix = "CANDIDATE" if msg["role"] == "user" else "INTERVIEWER"
        conversation_text += f"\n{prefix}: {msg['content']}\n"
    
    feedback_prompt = f"""You just completed a mock interview. Here is the full conversation:

{conversation_text}

Now provide DETAILED feedback on the candidate's performance. Structure it as:

OVERALL SCORE: X/10

STRENGTHS (what they did well):
- [point 1]
- [point 2]

WEAKNESSES (what needs improvement):
- [point 1]
- [point 2]

QUESTION-BY-QUESTION BREAKDOWN:
[For each question, 1-2 sentence assessment]

TOP 3 THINGS TO IMPROVE:
1. [specific action]
2. [specific action]
3. [specific action]

Be honest, specific, and constructive."""

    feedback = ask_llm_with_history(
        [{"role": "user", "content": feedback_prompt}],
        temperature=0.2,
        max_tokens=1200
    )
    
    return {
        "session_id": session_id,
        "feedback": feedback,
        "questions_answered": len(user_messages),
        "session_summary": f"Completed {len(user_messages)} questions"
    }
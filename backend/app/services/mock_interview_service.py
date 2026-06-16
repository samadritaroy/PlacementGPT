"""
Mock Interview Service
Multi-turn AI interview with Llama3.
Supports: Technical, HR, DSA, System Design rounds.
Company-specific prompts for Amazon, Google, TCS, Infosys, Wipro.
"""
import logging
from typing import Optional
from app.services.chat_history_service import (
    create_session,
    add_message,
    get_history,
    clear_session
)
from app.services.answer_evaluator_service import (
    evaluate_answer
)
from app.services.llm_service import (
    ask_llm_with_history,
    ask_llm
)
logger = logging.getLogger(__name__)
# ─────────────────────────────────────────────────────────────
# In-memory score tracker  { session_id: [...] }
# Each entry: { question, answer, scores, question_num }
# ─────────────────────────────────────────────────────────────
_session_scores: dict = {}
_session_config: dict = {}   # stores session type, company, etc.
 
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


def _build_system_prompt(session_type: str, company: Optional[str],
                          role: Optional[str], difficulty: str) -> str:
    config = SESSION_CONFIGS.get(session_type, SESSION_CONFIGS["technical"])
    company_block = COMPANY_CONTEXT.get(company, "") if company else ""
    
    base = f"""You are a senior interviewer conducting a REALISTIC mock interview.

INTERVIEW DETAILS:
- Type: {session_type.upper()} Round
- Company: {company or "Top Tech Company"}
- Role: {role or "Software Engineer"}
- Difficulty: {difficulty}
- Questions to ask: {config["num_questions"]}
- Focus areas: {config["focus"]}
- Your tone: {config["tone"]}

{company_block}

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


# ═══════════════════════════════════════════════════════════════
# start_mock_interview()
# ═══════════════════════════════════════════════════════════════
def start_mock_interview(
    session_type: str = "technical",
    company: Optional[str] = None,
    role: Optional[str] = None,
    difficulty: str = "medium"
) -> dict:
    """
    Start a new mock interview session.
    Returns session_id + first question from AI interviewer.
    SAME SIGNATURE as your existing code — drop-in replacement.
    """
    session_id = create_session(session_type=session_type, company=company)
    system_prompt = _build_system_prompt(session_type, company, role, difficulty)
 
    # Store session config for use in evaluation later
    _session_scores[session_id] = []
    _session_config[session_id] = {
        "session_type": session_type,
        "company": company,
        "role": role,
        "difficulty": difficulty,
    }
 
    # Store system prompt in session
    add_message(session_id, "system", system_prompt)
 
    # Get opening message from AI
    messages = [{"role": "system", "content": system_prompt}]
    opening = ask_llm_with_history(messages, temperature=0.5, max_tokens=400)
 
    add_message(session_id, "assistant", opening)
 
    return {
        "session_id":      session_id,
        "opening_message": opening,
        "company":         company,
        "role":            role,
        "session_type":    session_type,
        "difficulty":      difficulty,
        "question_number": 1,
        # Tells frontend: evaluation will come with each /continue call
        "evaluation_enabled": True,
    }
 
 
# ═══════════════════════════════════════════════════════════════
# continue_interview()  ← KEY CHANGE: now includes evaluation
# ═══════════════════════════════════════════════════════════════
def continue_interview(session_id: str, user_message: str) -> dict:
    """
    Process user's answer → evaluate it → get next question.
    Returns both the next question AND evaluation scores.
    SAME SIGNATURE as your existing code — drop-in replacement.
 
    Return shape (new fields added):
    {
        "response":       "...",          ← next question from AI interviewer
        "evaluation": {                   ← NEW: scores for THIS answer
            "clarity":      8,
            "correctness":  7,
            "depth":        6,
            "structure":    8,
            "overall":      7.25,
            "grade":        "B+",
            "feedback":     "...",
            "what_was_good":"...",
            "ideal_points": [...]
        },
        "session_progress": {             ← NEW: running averages across session
            "questions_answered": 2,
            "avg_score_so_far":   7.1,
            "all_scores":         [...]
        },
        "question_number": 2              ← which question this was
    }
    """
    history = get_history(session_id)
 
    # ── Step 1: Find the last question the AI asked ──────────
    # We evaluate user_message AGAINST this question
    last_question = _extract_last_ai_question(history)
 
    # ── Step 2: Add user answer to history ───────────────────
    add_message(session_id, "user", user_message)
 
    # ── Step 3: Evaluate the answer ──────────────────────────
    config = _session_config.get(session_id, {})
    scores = evaluate_answer(
        question=last_question,
        answer=user_message,
        question_type=config.get("session_type", "technical"),
        company=config.get("company")
    )
 
    # ── Step 4: Store scores for this Q&A pair ───────────────
    question_num = len(_session_scores[session_id]) + 1
    _session_scores[session_id].append({
        "question_number": question_num,
        "question":        last_question[:300],   # truncate for storage
        "answer":          user_message[:500],
        "scores":          scores,
    })
 
    # ── Step 5: Get next question from AI interviewer ────────
    updated_history = get_history(session_id)
    ai_response = ask_llm_with_history(
        updated_history, temperature=0.5, max_tokens=500
    )
    add_message(session_id, "assistant", ai_response)
 
    # ── Step 6: Compute running averages ─────────────────────
    all_scores = _session_scores[session_id]
    avg_so_far = round(
        sum(s["scores"].get("overall", 5) for s in all_scores) / len(all_scores), 2
    ) if all_scores else 0
 
    return {
        # What your existing frontend already uses:
        "response":       ai_response,
        "message_count":  question_num,
 
        # NEW — evaluation of this specific answer:
        "evaluation":     scores,
 
        # NEW — session-level running stats:
        "session_progress": {
            "questions_answered": question_num,
            "avg_score_so_far":   avg_so_far,
            "all_scores": [
                {
                    "q": s["question_number"],
                    "overall": s["scores"].get("overall", 0),
                    "grade":   s["scores"].get("grade", "?"),
                }
                for s in all_scores
            ],
        },
 
        "question_number": question_num,
    }
 
 
# ═══════════════════════════════════════════════════════════════
# end_interview_with_feedback()  ← Enhanced with full metrics
# ═══════════════════════════════════════════════════════════════
def end_interview_with_feedback(session_id: str) -> dict:
    """
    End interview → compute full metrics → get AI written feedback.
    Returns comprehensive results.
    SAME SIGNATURE as your existing code — drop-in replacement.
 
    Return shape:
    {
        "feedback":        "...",         ← AI written overall feedback
        "aggregate": {                    ← Average across all questions
            "overall":     7.4,
            "clarity":     7.8,
            "correctness": 7.2,
            "depth":       6.9,
            "structure":   7.6,
            "grade":       "B+",
            "percentile":  "Top 30%"
        },
        "question_breakdown": [...],      ← Per-question scores
        "total_questions": 4,
        "session_summary": "..."
    }
    """
    all_qa = _session_scores.get(session_id, [])
    config  = _session_config.get(session_id, {})
 
    # ── Compute aggregate scores ──────────────────────────────
    if all_qa:
        def avg(key):
            vals = [q["scores"].get(key, 5) for q in all_qa if q["scores"].get(key)]
            return round(sum(vals) / len(vals), 2) if vals else 0
 
        aggregate = {
            "overall":     avg("overall"),
            "clarity":     avg("clarity"),
            "correctness": avg("correctness"),
            "depth":       avg("depth"),
            "structure":   avg("structure"),
            "grade":       _grade(avg("overall")),
            "percentile":  _percentile(avg("overall")),
            "total_questions": len(all_qa),
        }
    else:
        aggregate = {
            "overall": 0, "clarity": 0, "correctness": 0,
            "depth": 0, "structure": 0, "grade": "N/A",
            "percentile": "N/A", "total_questions": 0
        }
 
    # ── Build conversation summary for AI feedback ────────────
    conversation_summary = ""
    for i, qa in enumerate(all_qa, 1):
        score = qa["scores"].get("overall", "?")
        conversation_summary += (
            f"\nQ{i} (Score: {score}/10): {qa['question'][:150]}\n"
            f"Answer: {qa['answer'][:200]}\n"
            f"Feedback: {qa['scores'].get('feedback', '')[:100]}\n"
        )
 
    # ── Get AI written feedback ───────────────────────────────
    company = config.get("company", "the company")
    role    = config.get("role", "the role")
    stype   = config.get("session_type", "technical")
 
    feedback_prompt = f"""You conducted a {stype} mock interview for {company} — {role} role.
 
Here is a summary of the candidate's performance:
{conversation_summary}
 
Overall score: {aggregate['overall']}/10 — {aggregate['grade']}
 
Write honest, constructive feedback in this format:
 
OVERALL PERFORMANCE:
[2-3 sentences on how the candidate did overall]
 
STRENGTHS:
• [specific strength 1 with example from interview]
• [specific strength 2]
 
AREAS TO IMPROVE:
• [specific weakness 1 with what to do about it]
• [specific weakness 2]
 
TOP 3 ACTION ITEMS BEFORE NEXT INTERVIEW:
1. [specific, actionable step]
2. [specific, actionable step]
3. [specific, actionable step]
 
READINESS FOR {company.upper() if company else 'PLACEMENT'}:
[1-2 sentences on how ready they are and what's left to work on]"""
 
    ai_feedback = ask_llm(feedback_prompt, temperature=0.3, max_tokens=700)
 
    # ── Build question-by-question breakdown ──────────────────
    question_breakdown = [
        {
            "question_number": qa["question_number"],
            "question_preview": qa["question"][:100] + "..." if len(qa["question"]) > 100 else qa["question"],
            "scores": {
                "clarity":     qa["scores"].get("clarity", 0),
                "correctness": qa["scores"].get("correctness", 0),
                "depth":       qa["scores"].get("depth", 0),
                "structure":   qa["scores"].get("structure", 0),
                "overall":     qa["scores"].get("overall", 0),
            },
            "grade":    qa["scores"].get("grade", "?"),
            "feedback": qa["scores"].get("feedback", ""),
        }
        for qa in all_qa
    ]
 
    # ── Cleanup memory ────────────────────────────────────────
    clear_session(session_id)
    _session_scores.pop(session_id, None)
    _session_config.pop(session_id, None)
 
    return {
        "feedback":          ai_feedback,
        "aggregate":         aggregate,
        "question_breakdown":question_breakdown,
        "total_questions":   len(all_qa),
        "session_summary": (
            f"Completed {len(all_qa)} questions. "
            f"Overall: {aggregate['overall']}/10 ({aggregate['grade']}) — {aggregate['percentile']}"
        ),
    }
 
 
# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
 
def _extract_last_ai_question(history: list) -> str:
    """
    Find the most recent assistant message — that's the question being answered.
    Skips system messages.
    """
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            return msg["content"]
    return "General interview question"
 
 
def _grade(score: float) -> str:
    if score >= 9.0: return "A+"
    if score >= 8.0: return "A"
    if score >= 7.0: return "B+"
    if score >= 6.0: return "B"
    if score >= 5.0: return "C"
    if score >= 3.0: return "D"
    return "F"
 
 
def _percentile(score: float) -> str:
    if score >= 8.5: return "Top 10%"
    if score >= 7.5: return "Top 25%"
    if score >= 6.5: return "Top 40%"
    if score >= 5.0: return "Top 60%"
    return "Bottom 40%"
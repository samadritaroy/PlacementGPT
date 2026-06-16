"""
Company-Specific Preparation Service
=====================================
File: backend/app/services/company_service.py
CREATE this as a new file in your services/ folder.

What this does:
- Stores structured data for each company (rounds, focus areas, tips)
- Generates personalized prep guides using Groq/LLM
- Returns common questions per company
- Gives study plan + resources
"""

from app.services.llm_service import ask_llm
from typing import Optional
import logging

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# COMPANY DATABASE — Structured info for each company
# Add more companies by following the same format
# ═══════════════════════════════════════════════════════════════

COMPANY_DATA = {
    "Amazon": {
        "emoji": "📦",
        "type": "Product",
        "difficulty": "Hard",
        "rounds": [
            {"name": "Online Assessment (OA)", "duration": "90 min",
             "description": "2 DSA problems + work simulation questions. Usually LeetCode medium difficulty."},
            {"name": "Technical Phone Screen", "duration": "45 min",
             "description": "1 DSA problem + basic behavioral. Interviewer from engineering team."},
            {"name": "Onsite / Virtual Onsite (Loop)", "duration": "4–5 hours",
             "description": "4–5 rounds: 2 coding, 1 system design, 2 behavioral (all LP-based)."},
        ],
        "focus_areas": {
            "DSA": ["Arrays", "Trees", "Graphs", "Dynamic Programming", "Sliding Window", "BFS/DFS"],
            "Behavioral": ["Leadership Principles (all 16)", "STAR method", "Ownership stories", "Conflict resolution"],
            "System Design": ["URL shortener", "Ride-sharing", "Rate limiter", "Notification system"],
            "Must Know": ["Big O analysis", "Trade-offs in design", "Scalability thinking"],
        },
        "lp_principles": [
            "Customer Obsession", "Ownership", "Invent and Simplify",
            "Are Right A Lot", "Learn and Be Curious", "Hire and Develop the Best",
            "Insist on Highest Standards", "Think Big", "Bias for Action",
            "Frugality", "Earn Trust", "Dive Deep",
            "Have Backbone; Disagree and Commit", "Deliver Results",
            "Strive to be Earth's Best Employer", "Success and Scale Bring Broad Responsibility"
        ],
        "common_questions": {
            "DSA": [
                "Two Sum / Two Pointers problems",
                "LRU Cache implementation",
                "Number of Islands (Graph BFS/DFS)",
                "Merge K sorted lists",
                "Word Break problem (DP)",
            ],
            "Behavioral": [
                "Tell me about a time you had to deliver under a tight deadline (Bias for Action + Deliver Results)",
                "Describe a time you disagreed with your manager (Have Backbone)",
                "Tell me about a project where you took ownership end-to-end (Ownership)",
                "Give an example of when you went above and beyond for a customer (Customer Obsession)",
                "Tell me about a time you failed. What did you learn? (Learn and Be Curious)",
            ],
        },
        "tips": [
            "Every answer must map to at least one Leadership Principle — interviewers score you on LPs",
            "Prepare 3–4 strong STAR stories and reuse them across multiple LPs",
            "Amazon asks 'Tell me more about what YOU did' — have specific personal contributions ready",
            "In OA: solve the easy problem perfectly first, then attempt hard one",
            "Think Big = mention scale/impact in system design (millions of users, not hundreds)",
        ],
        "resources": [
            "Amazon Leadership Principles: amazon.jobs/content/en/our-workplace/leadership-principles",
            "LeetCode Amazon tag (top 50 problems)",
            "Book: 'Cracking the Coding Interview' chapters 1–4",
            "YouTube: Amazon interview prep by Clement Mihailescu",
        ],
        "salary_range": "₹20–45 LPA (SDE-1), ₹40–80 LPA (SDE-2)",
        "study_time": "8–10 weeks",
    },

    "Google": {
        "emoji": "🔍",
        "type": "Product",
        "difficulty": "Very Hard",
        "rounds": [
            {"name": "Recruiter Screen", "duration": "30 min",
             "description": "Background, motivation, basic technical questions. HR-led."},
            {"name": "Technical Phone Screen", "duration": "45 min",
             "description": "1–2 coding problems on Google Docs (shared). Must think aloud."},
            {"name": "Onsite (Virtual)", "duration": "5–6 hours",
             "description": "4–5 rounds: coding (×2–3), system design (×1), behavioral/Googleyness (×1)."},
            {"name": "Hiring Committee Review", "duration": "1–3 weeks",
             "description": "Your interview packet reviewed by committee — not just your interviewer's decision."},
        ],
        "focus_areas": {
            "DSA": ["Graphs (BFS/DFS/Dijkstra)", "Trees (all traversals)", "DP (all patterns)", "Bit Manipulation", "String algorithms"],
            "Problem Solving": ["Always ask: can we do better?", "Discuss time/space trade-offs", "Handle edge cases explicitly"],
            "System Design": ["Google Search", "YouTube", "Google Maps", "Distributed cache", "Pub/Sub system"],
            "Googleyness": ["Ambiguous problem comfort", "Collaboration", "Intellectual humility", "Learning from failure"],
        },
        "common_questions": {
            "DSA": [
                "Word Ladder (BFS on graph)",
                "Serialize/Deserialize Binary Tree",
                "Longest Substring Without Repeating Characters",
                "Alien Dictionary (Topological Sort)",
                "Meeting Rooms II (Interval scheduling)",
            ],
            "Behavioral": [
                "Tell me about a time you worked on an ambiguous problem",
                "Describe a project you're most proud of and why",
                "Tell me about a time you had to learn something quickly",
                "Give an example of giving or receiving difficult feedback",
            ],
        },
        "tips": [
            "Think out loud — Google values thought process more than getting the right answer quickly",
            "Start with brute force, then optimize — never jump to optimal without explaining why",
            "Ask clarifying questions before coding: edge cases, constraints, input types",
            "System design: start with requirements, then capacity estimates, then high-level design",
            "Googleyness = be genuinely curious, collaborative, and humble in every round",
        ],
        "resources": [
            "LeetCode Hard problems (top Google tag)",
            "Book: 'System Design Interview' by Alex Xu (Vol 1 + 2)",
            "YouTube: TechDummies system design playlist",
            "Google's Engineering Practices guide (abseil.io)",
        ],
        "salary_range": "₹25–60 LPA (L3), ₹50–100 LPA (L4)",
        "study_time": "12–16 weeks",
    },

    "Microsoft": {
        "emoji": "🪟",
        "type": "Product",
        "difficulty": "Hard",
        "rounds": [
            {"name": "Online Assessment", "duration": "60–90 min",
             "description": "2 coding problems + multiple choice CS questions."},
            {"name": "Technical Interviews (×3)", "duration": "45 min each",
             "description": "Mix of DSA + OOP design + behavioral. Each interviewer covers one area."},
            {"name": "As-Appropriate (AA) Round", "duration": "45 min",
             "description": "Senior interviewer / hiring manager. Decision round."},
        ],
        "focus_areas": {
            "DSA": ["Arrays/Strings", "Trees/Graphs", "OOP design", "Recursion", "Linked Lists"],
            "OOP & Design": ["SOLID principles", "Design patterns (Factory, Singleton, Observer)", "Class design problems"],
            "System Design": ["Design a parking lot", "Design an elevator system", "Design Microsoft Teams"],
            "Behavioral": ["Growth mindset examples", "Collaboration stories", "Learning from failures"],
        },
        "common_questions": {
            "DSA": [
                "Reverse a linked list (iterative + recursive)",
                "Validate Binary Search Tree",
                "Clone Graph",
                "Find all permutations of a string",
                "Implement a stack with getMin() in O(1)",
            ],
            "Behavioral": [
                "Tell me about a time you had to learn something new quickly (Growth Mindset)",
                "Describe a conflict with a teammate and how you resolved it",
                "What's a project you built that you're proud of?",
                "Tell me about a time you gave or received constructive feedback",
            ],
        },
        "tips": [
            "Microsoft loves OOP — be ready to design classes with proper encapsulation",
            "SOLID principles are heavily tested: explain each with a real code example",
            "Growth mindset is Microsoft's culture — every answer should show eagerness to learn",
            "The AA round is decisive — focus on leadership qualities and impact in this round",
            "Azure knowledge is a plus for cloud/infra roles — read about IaaS/PaaS/SaaS",
        ],
        "resources": [
            "Microsoft Careers Blog",
            "LeetCode Microsoft tag (top 50)",
            "Book: 'Head First Design Patterns'",
            "YouTube: Nick White Microsoft interview solutions",
        ],
        "salary_range": "₹15–40 LPA (SDE-1), ₹35–70 LPA (SDE-2)",
        "study_time": "8–10 weeks",
    },

    "TCS": {
        "emoji": "💼",
        "type": "Service",
        "difficulty": "Easy–Medium",
        "rounds": [
            {"name": "TCS NQT (National Qualifier Test)", "duration": "180 min",
             "description": "Aptitude (Quant/Verbal/Reasoning) + Hands-on Coding (2 problems) + Advanced Coding (optional). Conducted every 3–4 months."},
            {"name": "Technical Interview", "duration": "30–45 min",
             "description": "Based on your resume, academic projects, and CS fundamentals. Very freshers-friendly."},
            {"name": "Managerial Round", "duration": "20–30 min",
             "description": "Situational + behavioral questions. Sometimes skipped."},
            {"name": "HR Round", "duration": "15–20 min",
             "description": "Standard HR: relocation, bond, salary expectations, joining date."},
        ],
        "focus_areas": {
            "Aptitude": ["Number series", "Profit & Loss", "Time & Work", "Probability", "Coding patterns"],
            "Technical": ["Java/Python basics", "OOPS (4 pillars with examples)", "SQL queries", "OS concepts", "Networking basics"],
            "Coding": ["Arrays (sorting, searching)", "String manipulation", "Number patterns", "Basic recursion"],
            "HR": ["Why TCS?", "Relocation willingness", "Bond (2 years)", "Strengths/Weaknesses"],
        },
        "common_questions": {
            "DSA": [
                "Reverse a string / check palindrome",
                "Find second largest element in array",
                "Fibonacci series using recursion",
                "Bubble sort implementation",
                "Find duplicate elements in array",
            ],
            "Technical": [
                "What are the 4 pillars of OOP? Explain with examples.",
                "What is the difference between process and thread?",
                "Explain normalization in DBMS (1NF, 2NF, 3NF).",
                "Write a SQL query for second highest salary.",
                "What is the difference between TCP and UDP?",
            ],
            "HR": [
                "Why do you want to join TCS?",
                "Are you okay with service agreement / 2-year bond?",
                "Are you willing to relocate anywhere in India?",
                "What are your strengths and weaknesses?",
            ],
        },
        "tips": [
            "NQT is the main filter — practice aptitude on PrepInsta and TCS NQT mock tests",
            "Prepare your 2–3 academic projects thoroughly — interviewers go deep on projects",
            "For HR: research TCS's recent news (acquisitions, milestones, revenue) before the interview",
            "Bond question is always asked — be confident saying 'Yes, I'm committed to 2 years'",
            "SQL is heavily tested: practice JOINs, GROUP BY, HAVING, subqueries on HackerRank",
        ],
        "resources": [
            "PrepInsta TCS NQT preparation material",
            "TCS iON Portal: tcsion.com (official mock tests)",
            "HackerRank SQL challenges",
            "IndiaBix for aptitude practice",
        ],
        "salary_range": "₹3.36–7 LPA (fresher), ₹7–15 LPA (with NQT Prime)",
        "study_time": "4–6 weeks",
    },

    "Infosys": {
        "emoji": "🏢",
        "type": "Service",
        "difficulty": "Easy–Medium",
        "rounds": [
            {"name": "Infosys Specialist Programmer / SE Test", "duration": "150 min",
             "description": "Pseudocode/algorithms section + English ability test + code debugging + Math ability."},
            {"name": "Technical Interview", "duration": "30–45 min",
             "description": "OOPS, DBMS, one coding problem, project discussion."},
            {"name": "HR Interview", "duration": "15–20 min",
             "description": "Standard HR questions, relocation, service agreement."},
        ],
        "focus_areas": {
            "Pseudocode Test": ["Algorithm tracing", "Flowchart reading", "Space/time prediction"],
            "Technical": ["OOPS (deep)", "SQL (complex queries)", "OS basics", "One coding problem"],
            "English": ["Reading comprehension", "Email writing", "Fill in the blanks"],
        },
        "common_questions": {
            "Technical": [
                "Explain all 4 OOPS pillars with REAL-WORLD examples (not just definitions)",
                "What is the difference between method overloading and overriding?",
                "Write SQL: find nth highest salary without using LIMIT",
                "What is a deadlock? How do you prevent it?",
                "Difference between abstract class and interface",
            ],
            "HR": [
                "Why Infosys over other companies?",
                "Where do you see yourself in 5 years?",
                "Tell me about your final year project",
                "Are you comfortable with a 1-year service agreement?",
            ],
        },
        "tips": [
            "The pseudocode section is unique to Infosys — practice tracing code logic step by step",
            "OOPS answers must have real-world examples: 'A Car is a Vehicle (inheritance)'",
            "Interviewers often ask to trace your project code — know every line of your project",
            "English section is easy — focus marks here to compensate for technical sections",
            "Infosys SP (Specialist Programmer) role pays much more — aim for that track",
        ],
        "resources": [
            "GeeksForGeeks Infosys interview experiences",
            "PrepInsta Infosys preparation",
            "Infosys SP mock tests on InfyTQ platform",
        ],
        "salary_range": "₹3.6–6.5 LPA (SE), ₹9–11 LPA (SP track)",
        "study_time": "3–5 weeks",
    },

    "Wipro": {
        "emoji": "💡",
        "type": "Service",
        "difficulty": "Easy",
        "rounds": [
            {"name": "NWOT (National Wipro Online Test)", "duration": "60 min",
             "description": "Aptitude + logical reasoning + verbal ability + 1 coding problem."},
            {"name": "Technical Interview", "duration": "30 min",
             "description": "CS fundamentals, one simple coding problem, project discussion."},
            {"name": "HR Interview", "duration": "15 min",
             "description": "Standard HR, relocation, salary, joining timeline."},
        ],
        "focus_areas": {
            "Aptitude": ["Number systems", "Series completion", "Blood relations", "Coding-decoding"],
            "Technical": ["OOP basics", "OS (process/thread/scheduling)", "DBMS (normalization, SQL)", "Networking (OSI model)"],
            "Coding": ["Simple array problems", "String reversal", "Prime numbers", "Fibonacci"],
        },
        "common_questions": {
            "Technical": [
                "What is the difference between a process and a thread?",
                "Explain OSI model layers with examples",
                "What is ACID property in DBMS?",
                "Write a program to check if a number is prime",
                "What is polymorphism? Give an example.",
            ],
            "HR": [
                "Tell me about yourself (structured 2-minute pitch)",
                "Why Wipro?",
                "Are you flexible with location?",
                "Strengths and one weakness with how you're improving it",
            ],
        },
        "tips": [
            "Wipro is the most freshers-friendly — basic CS fundamentals are enough",
            "The 'Tell me about yourself' answer is crucial — keep it structured and confident",
            "Prepare your college project in 2–3 sentences: what problem it solves, tech used, your role",
            "Aptitude section is straightforward — practice 30 min daily for 2 weeks",
            "Mention any internship, hackathon, or open source contribution — it differentiates you",
        ],
        "resources": [
            "PrepInsta Wipro NLTH preparation",
            "IndiaBix aptitude practice",
            "GeeksForGeeks Wipro interview experiences",
        ],
        "salary_range": "₹3.5–6 LPA (fresher)",
        "study_time": "2–4 weeks",
    },

    "Flipkart": {
        "emoji": "🛒",
        "type": "Product",
        "difficulty": "Hard",
        "rounds": [
            {"name": "Online Coding Test", "duration": "90 min",
             "description": "2–3 DSA problems. Usually medium–hard difficulty. HackerRank platform."},
            {"name": "Technical Interview 1", "duration": "60 min",
             "description": "Heavy DSA focus. 1–2 problems with optimization discussion."},
            {"name": "Technical Interview 2", "duration": "60 min",
             "description": "DSA + Low Level Design (OOP class design, design patterns)."},
            {"name": "Technical Interview 3 (HLD)", "duration": "60 min",
             "description": "High Level System Design. E-commerce systems at scale."},
            {"name": "HR + Culture Fit", "duration": "30 min",
             "description": "Behavioral questions, motivation, culture alignment."},
        ],
        "focus_areas": {
            "DSA": ["Advanced graphs", "Segment trees", "Tries", "DP on trees", "Heaps", "Monotonic stack"],
            "LLD": ["Design a Parking Lot", "Design Chess", "Splitwise/expense splitting", "Tic-tac-toe"],
            "HLD": ["Design Flipkart's product catalog", "Search with filters", "Order management", "Flash sale system"],
        },
        "common_questions": {
            "DSA": [
                "Merge K sorted linked lists",
                "Find median from data stream",
                "Word Search II (Trie + Backtracking)",
                "Sliding window maximum",
                "Edit distance (DP)",
            ],
            "Behavioral": [
                "Tell me about the most impactful project you've built",
                "How do you handle disagreements in a team?",
                "What's a technical problem you solved that you're proud of?",
            ],
        },
        "tips": [
            "Flipkart has very strong DSA rounds — practice LeetCode hard problems consistently",
            "LLD is as important as DSA at Flipkart — practice designing systems with SOLID principles",
            "For HLD: always think about e-commerce scale (millions of products, flash sales, inventory)",
            "Interviewers probe on time/space complexity — never skip this analysis",
            "Culture fit = customer-first mindset + data-driven decisions + speed of execution",
        ],
        "resources": [
            "LeetCode Flipkart tag + company-wise questions",
            "GitHub: Shreyas1612/LLD-problems",
            "YouTube: Gaurav Sen system design playlist",
            "Book: 'Designing Data-Intensive Applications' by Martin Kleppmann",
        ],
        "salary_range": "₹22–50 LPA (SDE-1), ₹45–90 LPA (SDE-2)",
        "study_time": "10–14 weeks",
    },
}


# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_company_list() -> list:
    """Return all available companies with basic info."""
    return [
        {
            "name": name,
            "emoji": data["emoji"],
            "type": data["type"],
            "difficulty": data["difficulty"],
            "study_time": data["study_time"],
        }
        for name, data in COMPANY_DATA.items()
    ]


def get_company_profile(company: str) -> dict:
    """
    Get full structured profile for a company.
    Returns all static data (rounds, focus areas, tips, questions).
    No LLM call — instant response.
    """
    data = COMPANY_DATA.get(company)
    if not data:
        return {"error": f"Company '{company}' not found. Available: {list(COMPANY_DATA.keys())}"}
    return {"company": company, **data}


def generate_prep_guide(
    company: str,
    role: str = "Software Engineer",
    experience: str = "fresher",
    weeks_available: int = 8,
    user_skills: Optional[list] = None,
) -> dict:
    """
    Generate a PERSONALIZED preparation guide using Groq/LLM.
    Combines static company data + LLM personalization.
    """
    company_info = COMPANY_DATA.get(company, {})
    if not company_info:
        return {"error": f"Company '{company}' not in database"}

    skills_str = ", ".join(user_skills) if user_skills else "not specified"
    focus = company_info.get("focus_areas", {})
    tips = company_info.get("tips", [])
    rounds = [r["name"] for r in company_info.get("rounds", [])]

    prompt = f"""You are a placement expert creating a personalized interview prep guide.

CANDIDATE DETAILS:
  Target Company: {company}
  Role: {role}
  Level: {experience}
  Time Available: {weeks_available} weeks
  Current Skills: {skills_str}

{company} INTERVIEW PROCESS:
  Rounds: {' → '.join(rounds)}
  DSA Focus: {', '.join(focus.get('DSA', []))}
  Key Tips: {'; '.join(tips[:3])}

Create a PERSONALIZED, ACTIONABLE prep guide with these sections:

## 📋 {company} Interview Overview
[2-3 sentences on what makes {company} unique to prepare for]

## 🗓️ {weeks_available}-Week Study Plan
[Week-by-week breakdown. Be specific about topics each week.
 Adjust based on the {weeks_available} weeks available.]

## 🎯 Must-Do Problems (Top 10 for {company})
[List 10 specific problems with their pattern/technique]

## 💡 {company}-Specific Strategies
[3-4 strategies UNIQUE to {company} that most candidates miss]

## ✅ Final Week Checklist
[What to do in the last 7 days before the interview]

Be specific, practical, and tailored to {company}. Avoid generic advice."""

    guide_text = ask_llm(
        prompt,
        system_prompt="You are a placement coach who has helped 1000+ students get into top tech companies.",
        max_tokens=1500,
        temperature=0.4
    )

    return {
        "company":          company,
        "role":             role,
        "experience":       experience,
        "weeks_available":  weeks_available,
        "prep_guide":       guide_text,
        "salary_range":     company_info.get("salary_range", "N/A"),
        "difficulty":       company_info.get("difficulty", "N/A"),
    }


def get_common_questions(company: str, question_type: str = "all") -> dict:
    """
    Get common interview questions for a company.
    question_type: "all", "dsa", "behavioral", "technical", "hr"
    """
    company_info = COMPANY_DATA.get(company, {})
    if not company_info:
        return {"error": f"Company not found"}

    all_questions = company_info.get("common_questions", {})

    if question_type == "all":
        return {"company": company, "questions": all_questions}

    key_map = {
        "dsa": "DSA", "behavioral": "Behavioral",
        "technical": "Technical", "hr": "HR"
    }
    key = key_map.get(question_type.lower(), question_type)
    filtered = all_questions.get(key, [])

    return {
        "company": company,
        "type": question_type,
        "questions": filtered
    }


def generate_mock_question(company: str, question_type: str, role: str = "Software Engineer") -> dict:
    """
    Generate a fresh interview question for a specific company using LLM.
    Different from the static question bank — generates new ones each time.
    """
    company_info = COMPANY_DATA.get(company, {})
    company_ctx = ""
    if company == "Amazon":
        company_ctx = "The question must relate to a Leadership Principle."
    elif company == "Google":
        company_ctx = "Focus on problem-solving process and optimal solution."
    elif company in ["TCS", "Infosys", "Wipro"]:
        company_ctx = "Keep at BTech fresher level. Not too advanced."

    type_prompts = {
        "dsa":       f"Generate a {company} DSA coding interview question. {company_ctx} Include: problem statement, 2 examples, constraints.",
        "behavioral":f"Generate a {company} behavioral interview question. {company_ctx} Include: the question + what they're really testing + ideal answer structure.",
        "technical": f"Generate a {company} technical concept question for {role}. {company_ctx} Include: question + ideal answer.",
        "system_design": f"Generate a {company} system design interview question. {company_ctx} Include: the problem + key areas to cover.",
    }

    prompt = type_prompts.get(question_type, type_prompts["technical"])

    question = ask_llm(prompt, max_tokens=600, temperature=0.7)

    return {
        "company": company,
        "type": question_type,
        "role": role,
        "question": question,
    }
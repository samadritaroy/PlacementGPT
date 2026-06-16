"""
Answer Evaluator Service
Scores candidate answers on 4 dimensions + gives feedback.
Also computes BLEU and ROUGE-L metrics (Phase 5).
"""

import json
import re
import math
import logging
from collections import Counter
from typing import List, Optional
from app.services.llm_service import ask_llm

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════
# AI-BASED EVALUATION
# ══════════════════════════════════════════════
def evaluate_answer(
    question: str,
    answer: str,
    question_type: str = "technical",
    company: Optional[str] = None
) -> dict:
    """
    Evaluate a candidate's answer using Groq/Llama3.
    Returns scores (1-10) on 4 dimensions + feedback.
    """
    if not answer or len(answer.strip()) < 10:
        return {
            "clarity": 1, "correctness": 1, "depth": 1, "structure": 1,
            "overall": 1.0, "grade": "F",
            "feedback": "No meaningful answer provided.",
            "ideal_points": []
        }
    
    company_ctx = f"This is a {company} interview. " if company else ""
    
    eval_prompt = f"""{company_ctx}Evaluate this {question_type} interview answer strictly.

QUESTION: {question}

CANDIDATE'S ANSWER: {answer}

Rate each dimension 1-10 where:
7 = genuinely good, 9-10 = exceptional (rare)

Return ONLY valid JSON, nothing else:
{{
  "clarity": <1-10 — is answer clearly communicated?>,
  "correctness": <1-10 — is technical/factual content correct?>,
  "depth": <1-10 — does it show deep understanding?>,
  "structure": <1-10 — is it well-organized? STAR for behavioral, approach→code→complexity for DSA>,
  "feedback": "<2-3 sentences of specific, actionable feedback>",
  "ideal_points": ["<key point that was missing or weak>", "<key point>", "<key point>"],
  "what_was_good": "<1 sentence on what they did right>"
}}"""
    
    raw = ask_llm(eval_prompt, temperature=0.1, max_tokens=600)
    
    try:
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in response")
        
        result = json.loads(json_match.group())
        
        # Compute overall
        result["overall"] = round(
            (result.get("clarity",5) + result.get("correctness",5) +
             result.get("depth",5) + result.get("structure",5)) / 4, 2
        )
        result["grade"] = _get_grade(result["overall"])
        result["percentile"] = _estimate_percentile(result["overall"])
        
        return result
    
    except (json.JSONDecodeError, ValueError, AttributeError) as e:
        logger.warning(f"Evaluator JSON parse failed: {e}")
        return _fallback_evaluation(raw)


def _fallback_evaluation(raw_text: str = "") -> dict:
    return {
        "clarity": 5, "correctness": 5, "depth": 5, "structure": 5,
        "overall": 5.0, "grade": "C",
        "feedback": raw_text[:300] if raw_text else "Evaluation temporarily unavailable.",
        "ideal_points": [], "what_was_good": "Unable to assess"
    }


def _get_grade(score: float) -> str:
    if score >= 9.0: return "A+"
    if score >= 8.0: return "A"
    if score >= 7.0: return "B+"
    if score >= 6.0: return "B"
    if score >= 5.0: return "C"
    return "D"


def _estimate_percentile(score: float) -> str:
    if score >= 8.5: return "Top 10%"
    if score >= 7.5: return "Top 25%"
    if score >= 6.5: return "Top 50%"
    return "Bottom 50%"


# ══════════════════════════════════════════════
# NLP METRICS (Phase 5)
# ══════════════════════════════════════════════

def compute_bleu(reference: str, hypothesis: str) -> float:
    """BLEU-2 score: measures content similarity to ideal answer."""
    def ngrams(tokens, n):
        return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    
    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())
    
    ref = tokenize(reference)
    hyp = tokenize(hypothesis)
    
    if not hyp or not ref:
        return 0.0
    
    bp = min(1.0, math.exp(1 - len(ref) / max(len(hyp), 1)))
    
    scores = []
    for n in range(1, 3):
        ref_ng  = Counter(ngrams(ref, n))
        hyp_ng  = Counter(ngrams(hyp, n))
        if not hyp_ng:
            scores.append(0.0)
            continue
        clipped   = sum(min(c, ref_ng[g]) for g, c in hyp_ng.items())
        precision = clipped / sum(hyp_ng.values())
        scores.append(precision)
    
    if not scores or all(s == 0 for s in scores):
        return 0.0
    
    log_avg = sum(math.log(s + 1e-10) for s in scores) / len(scores)
    return round(bp * math.exp(log_avg), 4)


def compute_rouge_l(reference: str, hypothesis: str) -> dict:
    """ROUGE-L: Longest Common Subsequence based F1."""
    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())
    
    def lcs(a, b):
        m, n = len(a), len(b)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if a[i-1] == b[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        return dp[m][n]
    
    ref = tokenize(reference)
    hyp = tokenize(hypothesis)
    
    if not ref or not hyp:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    lcs_len   = lcs(ref, hyp)
    precision = lcs_len / len(hyp)
    recall    = lcs_len / len(ref)
    f1        = (2*precision*recall / (precision+recall)) if (precision+recall) else 0
    
    return {
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
        "f1":        round(f1, 4)
    }


def compute_full_metrics(
    ideal_answer: str,
    candidate_answer: str,
    ideal_keywords: List[str] = None
) -> dict:
    """
    Full NLP metrics bundle for a Q&A pair.
    Call this for Phase 5 evaluation dashboard.
    """
    bleu  = compute_bleu(ideal_answer, candidate_answer)
    rouge = compute_rouge_l(ideal_answer, candidate_answer)
    
    # Keyword recall
    kw_recall = 0.0
    if ideal_keywords:
        ans_lower = candidate_answer.lower()
        found     = sum(1 for k in ideal_keywords if k.lower() in ans_lower)
        kw_recall = round(found / len(ideal_keywords), 4)
    
    # Composite score (0-100)
    composite = round(bleu * 30 + rouge["f1"] * 40 + kw_recall * 30, 2)
    
    return {
        "bleu_score":      bleu,
        "rouge_l":         rouge,
        "keyword_recall":  kw_recall,
        "composite_score": composite,
        "interpretation": {
            "bleu":   "Content similarity to ideal (0-1)",
            "rouge":  "Information overlap with ideal (F1)",
            "kw_rec": "Technical term coverage (0-1)",
            "composite": "Overall NLP score (0-100)"
        }
    }
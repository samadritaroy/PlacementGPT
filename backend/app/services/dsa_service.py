import random
import json
import re
import logging
from typing import Optional, List
from app.data.dsa_questions import QUESTION_BANK
from app.services.llm_service import ask_llm
from app.services.answer_evaluator_service import evaluate_answer
logger = logging.getLogger(__name__)
def get_question(
    topic: str,
    difficulty: str
):
    topic = topic.lower()

    if topic not in QUESTION_BANK:
        return None

    levels = QUESTION_BANK[topic]

    if difficulty not in levels:
        return None

    return random.choice(
        levels[difficulty]
    )
def generate_dsa_question(
    topic: str,
    difficulty: str = "easy"
):
    question = get_question(
        topic,
        difficulty
    )

    if not question:
        return {
            "error": f"No questions found for {topic} ({difficulty})"
        }

    return {
        "id": question["id"],
        "title": question["title"],
        "problem": question["problem"],
        "topic": topic,
        "difficulty": difficulty,
        "companies": question.get("companies", [])
    }
def get_dsa_hint(
    topic: str,
    difficulty: str,
    question_id: str
):
    question = get_question_by_id(
    question_id
)

    if not question:
        return {
            "error": "Question not found"
        }

    return {
        "id": question["id"],
        "title": question["title"],
        "hints": question.get("hints", [])
    }


def get_dsa_solution(
    topic: str,
    difficulty: str,
    question_id: str
):
    question = get_question_by_id(
    question_id
    )

    if not question:
        return {
            "error": "Question not found"
        }

    return {
        "id": question["id"],
        "title": question["title"],
        "approach": question.get("approach"),
        "time_complexity": question.get("time_complexity"),
        "space_complexity": question.get("space_complexity"),
        "solution": question.get("solution")
    }


def evaluate_dsa_answer(
    question: str,
    answer: str
):
    return evaluate_answer(
        question=question,
        answer=answer,
        question_type="dsa"
    )
def get_question_by_id(
    question_id: str
):
    for topic in QUESTION_BANK.values():

        for difficulty in topic.values():

            for question in difficulty:

                if question["id"] == question_id:
                    return question

    return None
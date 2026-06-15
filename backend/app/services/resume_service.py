from pathlib import Path
import re

SKILL_DATABASE = set()

SKILLS_FILE = (
    Path(__file__).parent.parent
    / "data"
    / "skills.txt"
)

with open(
    SKILLS_FILE,
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        skill = line.strip().lower()

        if skill:
            SKILL_DATABASE.add(skill)


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILL_DATABASE:

        if re.search(
            rf"\b{re.escape(skill)}\b",
            text
        ):

            found_skills.append(
                skill
            )

    return sorted(
        list(
            set(found_skills)
        )
    )
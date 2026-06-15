from app.services.resume_service import extract_skills
print("ATS SERVICE LOADED")
resume_skills = []


def save_resume_skills(skills):

    global resume_skills

    resume_skills = skills


def get_resume_skills():

    return resume_skills


def calculate_ats_score(
    resume_skills,
    jd_skills
):

    resume_set = set(
        skill.lower()
        for skill in resume_skills
    )

    jd_set = set(
        skill.lower()
        for skill in jd_skills
    )

    matched = list(
        resume_set.intersection(jd_set)
    )

    missing = list(
        jd_set - resume_set
    )

    score = 0

    if len(jd_set) > 0:

        score = round(
            len(matched)
            / len(jd_set)
            * 100
        )

    return {
        "ats_score": score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }
def generate_skill_gap_report(
    ats_result
):

    score = ats_result["ats_score"]

    missing = ats_result["missing_skills"]

    recommendations = []

    for skill in missing:

        recommendations.append(
            f"Learn {skill}"
        )

    return {
        "ats_score": score,
        "missing_skills": missing,
        "recommendations": recommendations
    }
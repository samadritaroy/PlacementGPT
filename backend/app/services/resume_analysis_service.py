def analyze_resume(text, skills):

    text_lower = text.lower()

    projects_count = text_lower.count("project")

    internships_count = (
        text_lower.count("internship")
        + text_lower.count("intern")
    )

    certifications_count = (
        text_lower.count("certificate")
        + text_lower.count("certification")
    )

    strengths = []

    improvements = []

    if len(skills) >= 10:
        strengths.append(
            "Strong technical skill set"
        )
    else:
        improvements.append(
            "Add more technical skills"
        )

    if projects_count > 0:
        strengths.append(
            "Has project experience"
        )
    else:
        improvements.append(
            "Add projects section"
        )

    if internships_count > 0:
        strengths.append(
            "Has internship experience"
        )
    else:
        improvements.append(
            "Gain internship experience"
        )

    return {
        "projects_count": projects_count,
        "internships_count": internships_count,
        "certifications_count": certifications_count,
        "skills_count": len(skills),
        "strengths": strengths,
        "improvements": improvements
    }
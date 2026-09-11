from typing import Any


def _list(value: Any):
    if isinstance(value, str):
        import json
        try:
            value = json.loads(value)
        except Exception:
            value = [value] if value else []
    return value or []


def _norm(items):
    return {str(x).strip().lower(): str(x).strip() for x in _list(items) if str(x).strip()}


def _education_score(candidate_education: str, requirement: str) -> float:
    if not requirement:
        return 100.0
    c = (candidate_education or "").lower()
    r = (requirement or "").lower()
    if not c:
        return 0.0
    degree_terms = ["phd", "doctor", "master", "m.tech", "mca", "mba", "bachelor", "b.tech", "b.e", "bsc", "bca", "degree"]
    req_level = next((i for i, term in enumerate(["bachelor", "master", "phd"]) if term in r), None)
    if req_level is None:
        return 100.0 if any(t in c for t in degree_terms) else 50.0
    levels = {"bachelor": 1, "master": 2, "phd": 3}
    cand_level = max((levels[k] for k in levels if k in c), default=0)
    return 100.0 if cand_level >= req_level + 1 else 100.0 if cand_level == req_level else 0.0


def calculate_match_score(candidate, job):
    required = _norm(job.required_skills)
    candidate_skills = _norm(candidate.skills)
    matched = set(required) & set(candidate_skills)
    skill_score = 100.0 if not required else len(matched) / len(required) * 100

    minimum = float(job.minimum_experience or 0)
    experience = float(candidate.experience or 0)
    experience_score = 100.0 if minimum <= 0 else min(experience / minimum, 1.0) * 100

    education_score = _education_score(candidate.education, job.education_requirements)

    other_requirements = _list(job.other_requirements)
    if not other_requirements:
        other_fit_score = 100.0
    else:
        text = " ".join([candidate.raw_resume_text or "", *candidate.projects, *candidate.certifications, *candidate.relevant_experience]).lower()
        hits = sum(1 for req in other_requirements if str(req).lower() in text)
        other_fit_score = hits / len(other_requirements) * 100

    score = skill_score * 0.50 + experience_score * 0.25 + education_score * 0.15 + other_fit_score * 0.10
    return {
        "score": round(score, 2),
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "education_score": round(education_score, 2),
        "other_fit_score": round(other_fit_score, 2),
    }

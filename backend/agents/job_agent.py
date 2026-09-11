import re
from schemas import AgentJobOutput
from services.llm_service import LLMService, LLMServiceError


COMMON_SKILLS = ["python", "java", "javascript", "typescript", "react", "next.js", "fastapi", "django", "sql", "sqlite", "postgresql", "mysql", "mongodb", "aws", "docker", "kubernetes", "git", "machine learning", "pytorch", "tensorflow", "nlp", "pandas", "numpy", "rest api"]


def _fallback(raw: str) -> AgentJobOutput:
    lower = raw.lower()
    found = [s for s in COMMON_SKILLS if s in lower]
    exp = 0.0
    m = re.search(r"(\d+)\s*\+?\s*(?:years?|yrs?)", lower)
    if m:
        exp = float(m.group(1))
    education = ""
    for pattern in [r"bachelor(?:'s)?[^.\n]*", r"master(?:'s)?[^.\n]*", r"degree[^.\n]*"]:
        m = re.search(pattern, raw, re.I)
        if m:
            education = m.group(0).strip()
            break
    return AgentJobOutput(
        title="Extracted Job",
        required_skills=found,
        preferred_skills=[],
        minimum_experience=exp,
        education_requirements=education,
        other_requirements=[]
    )


def extract_job_requirements(raw_job_description: str) -> AgentJobOutput:
    service = LLMService()
    if not service.enabled:
        return _fallback(raw_job_description)
    try:
        data = service.request_json(
            "Extract job requirements. Return only JSON with title, required_skills, preferred_skills, minimum_experience, education_requirements, other_requirements.",
            raw_job_description,
        )
        return AgentJobOutput.model_validate(data)
    except LLMServiceError:
        return _fallback(raw_job_description)

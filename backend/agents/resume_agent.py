import re
from schemas import AgentResumeOutput
from services.llm_service import LLMService, LLMServiceError


def _fallback(text: str) -> AgentResumeOutput:
    email_m = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone_m = re.search(r"(?:\+?\d[\d ()-]{7,}\d)", text)
    years_m = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", text, re.I)
    skills = []
    known = ["python", "java", "javascript", "typescript", "react", "next.js", "fastapi", "django", "sql", "sqlite", "postgresql", "mysql", "mongodb", "aws", "docker", "kubernetes", "git", "machine learning", "pytorch", "tensorflow", "nlp", "pandas", "numpy", "rest api"]
    lower = text.lower()
    skills = [s for s in known if s in lower]
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    name = lines[0] if lines and "@" not in lines[0] else "Unknown Candidate"
    education = next((x for x in lines if any(k in x.lower() for k in ["bachelor", "master", "b.tech", "m.tech", "degree"])), "")
    return AgentResumeOutput(
        name=name[:255], email=email_m.group(0) if email_m else "", phone=phone_m.group(0) if phone_m else "",
        education=education, experience=float(years_m.group(1)) if years_m else 0,
        skills=skills, projects=[], certifications=[], relevant_experience=[]
    )


def extract_candidate_profile(resume_text: str) -> AgentResumeOutput:
    service = LLMService()
    if not service.enabled:
        return _fallback(resume_text)
    try:
        data = service.request_json(
            "Extract a resume into JSON with name, email, phone, education, experience, skills, projects, certifications, relevant_experience.",
            resume_text,
        )
        return AgentResumeOutput.model_validate(data)
    except LLMServiceError:
        return _fallback(resume_text)

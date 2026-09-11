import re

from schemas import AgentJobOutput
from services.llm_service import LLMService, LLMServiceError


COMMON_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "next.js",
    "fastapi",
    "django",
    "sql",
    "sqlite",
    "postgresql",
    "mysql",
    "mongodb",
    "aws",
    "docker",
    "kubernetes",
    "git",
    "machine learning",
    "pytorch",
    "tensorflow",
    "nlp",
    "pandas",
    "numpy",
    "rest api",
]


def _find_skills(text: str):
    lower = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, lower):
            found.append(skill)

    return found


def _extract_experience(text: str) -> float:
    lower = text.lower()

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        lower
    )

    if match:
        return float(match.group(1))

    return 0.0


def _extract_education(text: str) -> str:
    patterns = [
        r"bachelor(?:'s)?[^\.\n]*",
        r"master(?:'s)?[^\.\n]*",
        r"degree[^\.\n]*",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0).strip()

    return ""


def _fallback(raw: str) -> AgentJobOutput:

    found = _find_skills(raw)

    exp = _extract_experience(raw)

    education = _extract_education(raw)

    return AgentJobOutput(
        title="Extracted Job",
        required_skills=found,
        preferred_skills=[],
        minimum_experience=exp,
        education_requirements=education,
        other_requirements=[],
    )


def extract_job_requirements(
    raw_job_description: str
) -> AgentJobOutput:

    service = LLMService()

    if not service.enabled:
        return _fallback(raw_job_description)

    try:

        data = service.request_json(
            """
            Extract the job requirements.

            Return ONLY valid JSON with:

            title
            required_skills
            preferred_skills
            minimum_experience
            education_requirements
            other_requirements
            """,
            raw_job_description,
        )

        return AgentJobOutput.model_validate(data)

    except LLMServiceError:

        return _fallback(raw_job_description)
from schemas import AgentMatchingOutput
from services.llm_service import LLMService, LLMServiceError


def _norm(items):
    return {str(x).strip().lower(): str(x).strip() for x in items if str(x).strip()}


def compare_candidate_to_job(candidate, job) -> AgentMatchingOutput:
    cskills = _norm(candidate.skills)
    required = _norm(job.required_skills)
    matched = [cskills[k] for k in required if k in cskills]
    missing = [required[k] for k in required if k not in cskills]
    fit = "Strong skill alignment" if len(required) == 0 or len(matched) / len(required) >= 0.7 else "Partial skill alignment"
    fallback = AgentMatchingOutput(
        matched_skills=matched,
        candidate_job_fit=fit,
        skill_observations=[f"Matched {len(matched)} of {len(required)} required skills."],
        experience_observations=[f"Candidate experience: {candidate.experience} years; required: {job.minimum_experience} years."],
        education_observations=[f"Candidate education: {candidate.education or 'Not provided'}; requirement: {job.education_requirements or 'Not specified'}."],
    )
    service = LLMService()
    if not service.enabled:
        return fallback
    try:
        data = service.request_json(
            "Compare candidate and job. Return JSON with matched_skills, candidate_job_fit, skill_observations, experience_observations, education_observations. Do not produce a numerical score.",
            f"JOB:\n{job.description}\nPROFILE:\n{candidate.raw_resume_text}",
        )
        return AgentMatchingOutput.model_validate(data)
    except LLMServiceError:
        return fallback

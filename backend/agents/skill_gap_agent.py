from schemas import AgentSkillGapOutput
from services.llm_service import LLMService, LLMServiceError


def _norm(items):
    return {str(x).strip().lower(): str(x).strip() for x in items if str(x).strip()}


def analyze_skill_gaps(candidate, job, matching_result) -> AgentSkillGapOutput:
    c = _norm(candidate.skills)
    required = _norm(job.required_skills)
    preferred = _norm(job.preferred_skills)
    matched = [c[k] for k in required if k in c]
    missing = [required[k] for k in required if k not in c]
    weak = [preferred[k] for k in preferred if k not in c]
    improvement = [f"Develop {x}." for x in missing[:5]]
    fallback = AgentSkillGapOutput(matched_skills=matched, missing_skills=missing, weak_skills=weak, improvement_areas=improvement)
    service = LLMService()
    if not service.enabled:
        return fallback
    try:
        data = service.request_json(
            "Identify candidate skill gaps. Return JSON with matched_skills, missing_skills, weak_skills, improvement_areas. Base claims only on supplied data.",
            f"JOB REQUIREMENTS:\n{job.description}\nCANDIDATE:\n{candidate.raw_resume_text}\nMATCHING:\n{matching_result.model_dump_json()}",
        )
        return AgentSkillGapOutput.model_validate(data)
    except LLMServiceError:
        return fallback

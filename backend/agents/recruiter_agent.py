from schemas import AgentRecruiterOutput
from services.llm_service import LLMService, LLMServiceError


def generate_recruiter_analysis(candidate, job, score, matching_result, skill_gap_result) -> AgentRecruiterOutput:
    strengths = []
    concerns = []
    if matching_result.matched_skills:
        strengths.append("Matches required skills: " + ", ".join(matching_result.matched_skills[:5]))
    if candidate.experience >= job.minimum_experience:
        strengths.append("Meets the stated experience requirement.")
    else:
        concerns.append("Does not meet the stated minimum experience requirement.")
    if skill_gap_result.missing_skills:
        concerns.append("Missing required skills: " + ", ".join(skill_gap_result.missing_skills[:5]))
    recommendation = "Strong Match" if score >= 80 else "Consider" if score >= 60 else "Review" if score >= 45 else "Low Match"
    fallback = AgentRecruiterOutput(
        strengths=strengths, concerns=concerns, recommendation=recommendation,
        explanation=f"Deterministic match score is {score:.1f}/100 based on skills, experience, education, and other fit.",
        recruiter_summary=f"{recommendation}: {candidate.name} scored {score:.1f}/100."
    )
    service = LLMService()
    if not service.enabled:
        return fallback
    try:
        data = service.request_json(
            "Write concise recruiter-friendly analysis. Return JSON with strengths, concerns, recommendation, explanation, recruiter_summary. Do not change or invent the supplied numerical score.",
            f"SCORE: {score:.1f}\nJOB: {job.description}\nCANDIDATE: {candidate.raw_resume_text}\nMATCHING: {matching_result.model_dump_json()}\nSKILL GAPS: {skill_gap_result.model_dump_json()}",
        )
        result = AgentRecruiterOutput.model_validate(data)
        result.recommendation = result.recommendation or recommendation
        return result
    except LLMServiceError:
        return fallback

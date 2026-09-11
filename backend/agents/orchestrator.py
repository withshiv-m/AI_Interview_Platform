import json
from sqlalchemy.orm import Session
from agents.matching_agent import compare_candidate_to_job
from agents.recruiter_agent import generate_recruiter_analysis
from agents.skill_gap_agent import analyze_skill_gaps
from services.scoring import calculate_match_score
from models import Analysis, Candidate, Job, Match


def _loads(value):
    try:
        return json.loads(value or "[]")
    except Exception:
        return []


def run_screening(db: Session, job: Job):
    candidates = db.query(Candidate).order_by(Candidate.candidate_id.asc()).all()
    results = []
    for candidate in candidates:
        matching = compare_candidate_to_job(candidate, job)
        score = calculate_match_score(candidate, job)
        gaps = analyze_skill_gaps(candidate, job, matching)
        recruiter = generate_recruiter_analysis(candidate, job, score["score"], matching, gaps)

        existing = db.query(Match).filter(Match.job_id == job.job_id, Match.candidate_id == candidate.candidate_id).first()
        if existing:
            match = existing
            db.query(Analysis).filter(Analysis.match_id == match.match_id).delete(synchronize_session=False)
        else:
            match = Match(job_id=job.job_id, candidate_id=candidate.candidate_id, **score)
            db.add(match)
            db.flush()
        match.score = score["score"]
        match.skill_score = score["skill_score"]
        match.experience_score = score["experience_score"]
        match.education_score = score["education_score"]
        match.other_fit_score = score["other_fit_score"]
        match.matched_skills = json.dumps(gaps.matched_skills)
        match.missing_skills = json.dumps(gaps.missing_skills)
        match.weak_skills = json.dumps(gaps.weak_skills)
        db.add(Analysis(
            match_id=match.match_id, job_id=job.job_id, candidate_id=candidate.candidate_id,
            strengths=json.dumps(recruiter.strengths), concerns=json.dumps(recruiter.concerns),
            skill_gaps=json.dumps(gaps.improvement_areas), recommendation=recruiter.recommendation,
            explanation=recruiter.explanation, recruiter_summary=recruiter.recruiter_summary,
        ))
        results.append({
            "candidate_id": candidate.candidate_id,
            "candidate_name": candidate.name,
            **score,
            "matched_skills": gaps.matched_skills,
            "missing_skills": gaps.missing_skills,
            "weak_skills": gaps.weak_skills,
            "strengths": recruiter.strengths,
            "concerns": recruiter.concerns,
            "recommendation": recruiter.recommendation,
            "explanation": recruiter.explanation,
            "recruiter_summary": recruiter.recruiter_summary,
        })
    db.commit()
    return sorted(results, key=lambda x: (-x["score"], x["candidate_id"]))

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Candidate
from schemas import APIResponse

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])


def serialize(c):
    return {
        "candidate_id": c.candidate_id, "name": c.name, "email": c.email, "phone": c.phone,
        "education": c.education, "experience": c.experience, "skills": json.loads(c.skills or "[]"),
        "projects": json.loads(c.projects or "[]"), "certifications": json.loads(c.certifications or "[]"),
        "relevant_experience": json.loads(c.relevant_experience or "[]"), "resume_filename": c.resume_filename,
        "resume_path": c.resume_path, "raw_resume_text": c.raw_resume_text, "created_at": c.created_at, "updated_at": c.updated_at,
    }


@router.get("", response_model=APIResponse, summary="List candidates")
def list_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).order_by(Candidate.created_at.desc()).all()
    return {"success": True, "data": [serialize(c) for c in candidates], "message": "Candidates retrieved successfully."}


@router.get("/{candidate_id}", response_model=APIResponse, summary="Get a candidate")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Candidate not found.", "error": "CANDIDATE_NOT_FOUND"})
    return {"success": True, "data": serialize(candidate), "message": "Candidate retrieved successfully."}


@router.delete("/{candidate_id}", response_model=APIResponse, summary="Delete a candidate")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Candidate not found.", "error": "CANDIDATE_NOT_FOUND"})
    db.delete(candidate); db.commit()
    return {"success": True, "data": None, "message": "Candidate deleted successfully."}

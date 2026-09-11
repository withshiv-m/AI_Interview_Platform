from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Job
from schemas import APIResponse
from agents.orchestrator import run_screening

router = APIRouter(prefix="/api/matching", tags=["Matching"])


@router.post("/run/{job_id}", response_model=APIResponse, summary="Run screening for a job")
def run_matching(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Job not found.", "error": "JOB_NOT_FOUND"})
    try:
        results = run_screening(db, job)
        return {"success": True, "data": {"job_id": job_id, "results": results}, "message": f"Screened {len(results)} candidate(s)."}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail={"success": False, "data": None, "message": "Matching pipeline failed.", "error": str(exc)})

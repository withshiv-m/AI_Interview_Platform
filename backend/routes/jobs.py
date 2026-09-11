import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Job
from schemas import APIResponse, JobCreate
from agents.job_agent import extract_job_requirements

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


def serialize(job):
    return {
        "job_id": job.job_id, "title": job.title, "description": job.description,
        "extracted_requirements": json.loads(job.extracted_requirements or "{}"),
        "required_skills": json.loads(job.required_skills or "[]"),
        "preferred_skills": json.loads(job.preferred_skills or "[]"),
        "minimum_experience": job.minimum_experience, "education_requirements": job.education_requirements,
        "other_requirements": json.loads(job.other_requirements or "[]"),
        "created_at": job.created_at, "updated_at": job.updated_at,
    }


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED, summary="Create a job")
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    extracted = extract_job_requirements(payload.description)
    job = Job(title=payload.title, description=payload.description,
              extracted_requirements=extracted.model_dump_json(),
              required_skills=json.dumps(extracted.required_skills), preferred_skills=json.dumps(extracted.preferred_skills),
              minimum_experience=extracted.minimum_experience, education_requirements=extracted.education_requirements,
              other_requirements=json.dumps(extracted.other_requirements))
    db.add(job); db.commit(); db.refresh(job)
    return {"success": True, "data": serialize(job), "message": "Job created successfully."}


@router.get("", response_model=APIResponse, summary="List jobs")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return {"success": True, "data": [serialize(j) for j in jobs], "message": "Jobs retrieved successfully."}


@router.get("/{job_id}", response_model=APIResponse, summary="Get a job")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Job not found.", "error": "JOB_NOT_FOUND"})
    return {"success": True, "data": serialize(job), "message": "Job retrieved successfully."}


@router.delete("/{job_id}", response_model=APIResponse, summary="Delete a job")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Job not found.", "error": "JOB_NOT_FOUND"})
    db.delete(job); db.commit()
    return {"success": True, "data": None, "message": "Job deleted successfully."}

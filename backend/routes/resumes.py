import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models import Candidate
from schemas import APIResponse
from services.parser import DocumentParseError, extract_text
from services.storage import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, build_resume_path, ensure_upload_dirs
from agents.resume_agent import extract_candidate_profile

router = APIRouter(prefix="/api/resumes", tags=["Resumes"])


def serialize(c):
    return {
        "candidate_id": c.candidate_id, "name": c.name, "email": c.email, "phone": c.phone,
        "education": c.education, "experience": c.experience, "skills": json.loads(c.skills or "[]"),
        "projects": json.loads(c.projects or "[]"), "certifications": json.loads(c.certifications or "[]"),
        "relevant_experience": json.loads(c.relevant_experience or "[]"), "resume_filename": c.resume_filename,
        "resume_path": c.resume_path, "raw_resume_text": c.raw_resume_text, "created_at": c.created_at, "updated_at": c.updated_at,
    }


@router.post("/upload", response_model=APIResponse, summary="Upload one or more PDF/DOCX resumes")
async def upload_resumes(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    ensure_upload_dirs()
    if not files:
        raise HTTPException(status_code=400, detail={"success": False, "data": None, "message": "No files supplied.", "error": "NO_FILES"})
    if len(files) > 20:
        raise HTTPException(status_code=400, detail={"success": False, "data": None, "message": "Maximum 20 files per request.", "error": "TOO_MANY_FILES"})

    created = []
    for upload in files:
        suffix = __import__("pathlib").Path(upload.filename or "").suffix.lower()
        if suffix not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail={"success": False, "data": None, "message": f"Unsupported file type: {upload.filename}", "error": "INVALID_FILE_TYPE"})
        path = build_resume_path(upload.filename)
        size = 0
        try:
            with path.open("wb") as out:
                while chunk := await upload.read(1024 * 1024):
                    size += len(chunk)
                    if size > MAX_FILE_SIZE:
                        out.close(); path.unlink(missing_ok=True)
                        raise HTTPException(status_code=413, detail={"success": False, "data": None, "message": f"File too large: {upload.filename}", "error": "FILE_TOO_LARGE"})
                    out.write(chunk)
            raw = extract_text(path)
            profile = extract_candidate_profile(raw)
            candidate = Candidate(
                name=profile.name, email=profile.email, phone=profile.phone, education=profile.education,
                experience=profile.experience, skills=json.dumps(profile.skills), projects=json.dumps(profile.projects),
                certifications=json.dumps(profile.certifications), relevant_experience=json.dumps(profile.relevant_experience),
                resume_filename=upload.filename or path.name, resume_path=str(path.relative_to(path.parents[2])), raw_resume_text=raw,
            )
            db.add(candidate); db.flush(); created.append(serialize(candidate))
        except HTTPException:
            raise
        except DocumentParseError as exc:
            path.unlink(missing_ok=True)
            raise HTTPException(status_code=422, detail={"success": False, "data": None, "message": str(exc), "error": "DOCUMENT_PARSE_ERROR"})
        except Exception as exc:
            path.unlink(missing_ok=True)
            db.rollback()
            raise HTTPException(status_code=500, detail={"success": False, "data": None, "message": "Resume processing failed.", "error": str(exc)})
    db.commit()
    return {"success": True, "data": created, "message": f"Processed {len(created)} resume(s) successfully."}

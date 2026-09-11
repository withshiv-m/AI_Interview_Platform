import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine, init_db
from routes import candidates, jobs, matching, resumes
from services.storage import ensure_upload_dirs

init_db()
ensure_upload_dirs()

app = FastAPI(
    title="PS03 Multi-Agent Resume Screening & Job Matching API",
    version="1.0.0",
    description="Hackathon MVP backend for resume screening and job matching.",
)
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(candidates.router)
app.include_router(matching.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"success": False, "data": None, "message": str(exc.detail), "error": "HTTP_ERROR"}
    return JSONResponse(status_code=exc.status_code, content=detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"success": False, "data": None, "message": "Invalid request data.", "error": str(exc.errors())})


@app.get("/api/health", tags=["Health"], summary="Check API and database health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"success": True, "data": {"database": "connected"}, "message": "PS03 backend is running"}
    except Exception as exc:
        return {"success": False, "data": None, "message": "PS03 backend database is unavailable", "error": str(exc)}

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app
from database import Base, engine, SessionLocal
from models import Job, Candidate
from services.scoring import calculate_match_score
from services.parser import extract_text_from_docx, extract_text_from_pdf

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["success"] is True


def test_job_creation_and_get():
    r = client.post("/api/jobs", json={"title": "Backend Engineer", "description": "Python FastAPI SQL, 2 years experience, bachelor's degree."})
    assert r.status_code == 201
    data = r.json()["data"]
    assert data["title"] == "Backend Engineer"
    r2 = client.get(f"/api/jobs/{data['job_id']}")
    assert r2.status_code == 200


def test_score_calculation():
    db = SessionLocal()
    try:
        job = Job(title="Test", description="test", required_skills=json.dumps(["python", "sql"]), preferred_skills="[]", minimum_experience=2, education_requirements="bachelor", other_requirements="[]")
        candidate = Candidate(name="Test Candidate", resume_filename="x.docx", resume_path="x", skills=json.dumps(["python", "sql"]), experience=2, education="Bachelor's degree", raw_resume_text="Python SQL")
        db.add_all([job, candidate]); db.commit(); db.refresh(job); db.refresh(candidate)
        s = calculate_match_score(candidate, job)
        assert s["skill_score"] == 100
        assert s["score"] == 100
    finally:
        db.close()


def test_matching_one_candidate():
    client.post("/api/jobs", json={"title": "Backend", "description": "Python FastAPI SQL, 2 years experience."})
    db = SessionLocal()
    c = Candidate(name="Alice", email="alice@example.com", resume_filename="alice.docx", resume_path="uploads/resumes/alice.docx", skills=json.dumps(["python", "fastapi", "sql"]), experience=3, education="Bachelor's degree", raw_resume_text="Alice Python FastAPI SQL")
    db.add(c); db.commit(); db.close()
    r = client.post("/api/matching/run/1")
    assert r.status_code == 200
    assert len(r.json()["data"]["results"]) == 1
    assert r.json()["data"]["results"][0]["score"] > 0

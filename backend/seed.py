import json
from database import SessionLocal, init_db
from models import Candidate, Job
from agents.job_agent import extract_job_requirements

init_db()

def seed():
    db = SessionLocal()
    try:
        if db.query(Job).count() or db.query(Candidate).count():
            print("Seed skipped: database already contains data.")
            return
        jobs = [
            ("Python Backend Developer", "Build APIs using Python, FastAPI, SQL, Git and Docker. 2 years experience. Bachelor's degree preferred."),
            ("Frontend Engineer", "Develop React and TypeScript applications with Next.js, JavaScript and Git. 1 year experience. Bachelor's degree."),
            ("ML Engineer", "Work on machine learning and NLP using Python, PyTorch, pandas and SQL. 2 years experience. Master's degree preferred."),
        ]
        for title, desc in jobs:
            ext = extract_job_requirements(desc)
            db.add(Job(title=title, description=desc, extracted_requirements=ext.model_dump_json(), required_skills=json.dumps(ext.required_skills), preferred_skills=json.dumps(ext.preferred_skills), minimum_experience=ext.minimum_experience, education_requirements=ext.education_requirements, other_requirements=json.dumps(ext.other_requirements)))
        skills = [
            ["python", "fastapi", "sql", "git", "docker"], ["python", "django", "sql", "git"], ["python", "fastapi", "postgresql", "git", "docker"],
            ["react", "typescript", "next.js", "javascript", "git"], ["react", "javascript", "git"], ["typescript", "react", "next.js", "git"],
            ["python", "machine learning", "pytorch", "pandas", "numpy", "nlp"], ["python", "machine learning", "pandas", "sql"], ["python", "nlp", "pytorch", "sql"], ["python", "sql", "git"],
        ]
        for i, sk in enumerate(skills, 1):
            db.add(Candidate(name=f"Synthetic Candidate {i}", email=f"candidate{i}@example.com", phone=f"+91-90000000{i:02d}", education="Bachelor's degree" if i != 7 else "Master's degree", experience=float((i % 5) + 1), skills=json.dumps(sk), projects=json.dumps(["Synthetic demo project"]), certifications=json.dumps([]), relevant_experience=json.dumps(["Synthetic experience for demo testing"]), resume_filename=f"synthetic_candidate_{i}.docx", resume_path=f"uploads/resumes/synthetic_candidate_{i}.docx", raw_resume_text=f"Synthetic Candidate {i}\nSkills: {', '.join(sk)}\nExperience: {(i % 5) + 1} years\nEducation: Bachelor's degree"))
        db.commit()
        print("Seeded 3 synthetic jobs and 10 synthetic candidates.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

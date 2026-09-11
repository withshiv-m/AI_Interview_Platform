# PS03 — Multi-Agent Resume Screening & Job Matching Platform

A simple hackathon MVP backend built with Python 3.11+, FastAPI, SQLAlchemy and SQLite. It exposes a stable JSON API for a React/Next.js frontend and keeps the final match score deterministic in Python.

## Architecture

```text
Recruiter
   │
   ├── POST /api/jobs
   │       ↓
   │   Job Agent → SQLite
   │
   ├── POST /api/resumes/upload
   │       ↓
   │   Parser → Resume Agent → SQLite
   │
   └── POST /api/matching/run/{job_id}
           ↓
      Matching Agent
           ↓
      Deterministic Scoring
           ↓
      Skill Gap Agent
           ↓
      Recruiter Agent
           ↓
      SQLite → Ranked JSON
```

Agents never access the database directly. The routes/orchestrator pass data to agents and persist their outputs.

## Folder structure

```text
backend/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── database.py
├── models.py
├── schemas.py
├── seed.py
├── routes/{jobs,resumes,candidates,matching}.py
├── services/{parser,llm_service,scoring,storage}.py
├── agents/{orchestrator,job_agent,resume_agent,matching_agent,skill_gap_agent,recruiter_agent}.py
├── tests/test_backend.py
└── uploads/{resumes,jobs}/
```

## Installation

From the `backend` directory:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` to `.env` and set:

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_here
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_TIMEOUT_SECONDS=30
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001
```

The API key is never hardcoded. When no LLM credentials are configured, the agents use small local fallback extractors so the hackathon demo and tests remain runnable; this fallback is intentionally simple and should not be treated as production-grade NLP.

## Database

SQLite is created automatically at:

`backend/ps03.db`

No manual database creation is needed. `main.py` initializes tables at startup.

## Run

```bash
uvicorn main:app --reload
```

Open `http://localhost:8000/docs` for Swagger UI or `http://localhost:8000/redoc` for ReDoc.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API + database health |
| POST | `/api/jobs` | Create and analyze a job |
| GET | `/api/jobs` | List jobs |
| GET | `/api/jobs/{job_id}` | Get a job |
| DELETE | `/api/jobs/{job_id}` | Delete job + related records |
| POST | `/api/resumes/upload` | Upload multiple PDF/DOCX resumes |
| GET | `/api/candidates` | List candidates |
| GET | `/api/candidates/{candidate_id}` | Get candidate details |
| DELETE | `/api/candidates/{candidate_id}` | Delete candidate + related records |
| POST | `/api/matching/run/{job_id}` | Screen all candidates and return ranking |

## Example requests

### Create job

```bash
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Backend Developer","description":"Build APIs using Python, FastAPI and SQL. 2 years experience. Bachelor degree."}'
```

### Upload resumes

```bash
curl -X POST http://localhost:8000/api/resumes/upload \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.docx"
```

Up to 20 files are accepted per request, with a 5 MB limit per file.

### Run screening

```bash
curl -X POST http://localhost:8000/api/matching/run/1
```

## Matching score

The numerical score is independent of the LLM:

- Skills: 50%
- Experience: 25%
- Education: 15%
- Other Fit: 10%

Scores are calculated deterministically by `services/scoring.py`. LLM agents can explain observations, but they cannot overwrite the numerical score.

## Seed demo data

```bash
python seed.py
```

This creates 3 synthetic jobs and 10 synthetic candidates. The seed command skips itself if the database already contains data.

Then run:

```bash
uvicorn main:app --reload
```

and call:

```bash
curl -X POST http://localhost:8000/api/matching/run/1
```

## Tests

```bash
pytest -q
```

The tests cover health, database initialization, job creation, scoring and a one-job/one-candidate matching workflow. Parser behavior is covered by the parser functions and can be exercised directly with PDF/DOCX fixtures.

## Frontend connection

The frontend can use `fetch`/Axios against `http://localhost:8000` and consume the consistent envelope:

```json
{"success": true, "data": {}, "message": "..."}
```

Use the job list/create endpoints for job selection, the multipart upload endpoint for resumes, the matching endpoint for ranked candidates, and candidate endpoints for detail pages. CORS origins are configured with `CORS_ORIGINS`.

## Limitations

- The local fallback extraction is heuristic; configure an LLM for richer structured extraction and recruiter explanations.
- SQLite is appropriate for the MVP, not a high-concurrency production deployment.
- PDF text extraction will not reliably process scanned/image-only PDFs without OCR.
- Authentication/authorization is outside the requested MVP scope.

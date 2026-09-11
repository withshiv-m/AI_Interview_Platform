# PS03 Frontend — HireMind AI

React + Vite frontend for the supplied PS03 FastAPI backend.

## 1. Start the backend

From the backend folder:

```powershell
uvicorn main:app --reload
```

Backend should run at:

http://localhost:8000

## 2. Start this frontend

```powershell
npm install
npm run dev
```

Open:

http://localhost:3000

## API connection

By default the frontend calls `http://localhost:8000`.

To change it, create `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## Implemented workflow

- Dashboard
- Create job
- Job Agent-backed job requirement extraction
- Upload multiple PDF/DOCX resumes
- Resume Agent-backed candidate extraction
- Candidate list/search/details
- Run multi-agent screening
- Deterministic match score display
- Matched/missing skills
- Recruiter recommendation, strengths and concerns
- Responsive desktop/mobile UI
- Delete jobs/candidates
- API refresh and error toasts

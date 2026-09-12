# PS03 — Multi-Agent Resume Screening & Job Matching Platform

> An AI-powered multi-agent platform that automates resume screening, compares candidates against job requirements, identifies skill gaps, and provides recruiter-friendly recommendations.

## About The Project

**PS03 — Multi-Agent Resume Screening & Job Matching Platform** is a full-stack hackathon solution designed to make the recruitment screening process faster, more consistent, and easier for recruiters.

The system accepts a job description and multiple candidate resumes, extracts structured information using AI agents, calculates an explainable deterministic match score, identifies skill gaps, and generates recruiter-friendly candidate summaries.

The application is divided into two major parts:

* **Frontend** — Interactive recruiter interface
* **Backend** — FastAPI APIs, AI agents, document processing, scoring, and database management

The frontend communicates with the backend through REST APIs.

---

# Problem Statement

Recruiters often need to screen a large number of resumes for a single job opening.

Manual screening can be:

* Time-consuming
* Repetitive
* Difficult to scale
* Inconsistent across candidates
* Challenging when comparing skills and experience
* Difficult when identifying skill gaps

A recruiter may have to manually compare job requirements with information spread across many resumes.

### Our Goal

To build an intelligent screening platform that can:

* Process multiple resumes
* Extract candidate information automatically
* Understand job requirements
* Compare candidates against a selected job
* Calculate an explainable match score
* Identify matched, missing, and weak skills
* Generate recruiter-friendly recommendations
* Provide ranked candidates through an API

---

# Solution

Our solution uses a **multi-agent AI workflow** combined with deterministic Python-based scoring.

The system separates AI-based analysis from numerical scoring so that the final match score remains consistent and explainable.

### Application Flow

```text
Recruiter
    │
    ├── Job Description
    │       ↓
    │   Job Agent
    │
    └── Resume Upload
            ↓
        Resume Parser
            ↓
        Resume Agent
            │
            ▼
       Candidate + Job
            │
            ▼
       Matching Agent
            │
            ▼
   Deterministic Scoring
            │
            ▼
     Skill Gap Agent
            │
            ▼
     Recruiter Agent
            │
            ▼
    Ranked Candidates
            │
            ▼
     Recruiter Review
```

---

# AI Multi-Agent System

The platform uses five specialized AI agents.

### 1. Job Agent

Extracts structured requirements from a job description.

It identifies:

* Required skills
* Preferred skills
* Minimum experience
* Education requirements
* Other requirements

### 2. Resume Agent

Processes extracted resume text and creates a structured candidate profile.

It extracts:

* Name
* Email
* Phone
* Education
* Experience
* Skills
* Projects
* Certifications
* Relevant experience

### 3. Matching Agent

Compares the candidate profile with the selected job profile.

It produces observations about:

* Skill compatibility
* Experience compatibility
* Education compatibility
* Overall candidate-job fit

The agent does **not** directly control the final numerical score.

### 4. Skill Gap Agent

Identifies:

* Matched skills
* Missing skills
* Weak skills
* Improvement areas

### 5. Recruiter Agent

Converts the analysis into a recruiter-friendly result containing:

* Strengths
* Concerns
* Recommendation
* Explanation
* Recruiter summary

---

# Deterministic Matching Score

The final numerical score is calculated in Python and is independent of the LLM.

| Factor     | Weight |
| ---------- | -----: |
| Skills     |    50% |
| Experience |    25% |
| Education  |    15% |
| Other Fit  |    10% |

This separation makes the scoring process more deterministic and explainable.

```text
Final Score
     │
     ├── Skills       → 50%
     ├── Experience   → 25%
     ├── Education    → 15%
     └── Other Fit    → 10%
```

The LLM agents provide qualitative analysis and explanations, while Python calculates the final numerical score.

---

# Technical Architecture

```text
                    ┌─────────────────┐
                    │    Recruiter    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ React / Next.js │
                    │    Frontend     │
                    └────────┬────────┘
                             │ REST API
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │     Backend     │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
        Job Routes      Resume Routes    Matching Routes
             │               │                │
             └───────────────┼────────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Orchestrator  │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
        AI Agents       Services          Scoring
             │               │                │
             └───────────────┼────────────────┘
                             ▼
                    ┌─────────────────┐
                    │ SQLite Database │
                    └─────────────────┘
```

---

# Technology Stack

## Frontend

* React / Next.js
* HTML
* CSS
* JavaScript
* REST API integration

## Backend

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* SQLAlchemy
* SQLite
* python-multipart

## AI & Document Processing

* LLM API
* Structured JSON responses
* PDF parsing
* DOCX parsing
* python-docx
* pypdf

## Development Tools

* Git
* GitHub
* VS Code
* REST APIs
* FastAPI Swagger UI

---

# Project Structure

```text
KH096-Tech_pluse/
│
├── frontend/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   │
│   ├── routes/
│   │   ├── jobs.py
│   │   ├── resumes.py
│   │   ├── candidates.py
│   │   └── matching.py
│   │
│   ├── services/
│   │   ├── parser.py
│   │   ├── llm_service.py
│   │   ├── scoring.py
│   │   └── storage.py
│   │
│   ├── agents/
│   │   ├── orchestrator.py
│   │   ├── job_agent.py
│   │   ├── resume_agent.py
│   │   ├── matching_agent.py
│   │   ├── skill_gap_agent.py
│   │   └── recruiter_agent.py
│   │
│   ├── tests/
│   │   ├── test_backend.py
│   │   └── test_acceptance.py
│   │
│   └── uploads/
│       ├── resumes/
│       └── jobs/
│
└── README.md
```

---

# Backend Setup

## 1. Clone the Repository

```bash
git clone https://github.com/withshiv-m/KH096-Tech_pluse.git
cd KH096-Tech_pluse
```

## 2. Open Backend

```bash
cd backend
```

## 3. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the `backend` directory.

Use `.env.example` as the template.

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_here
LLM_API_URL=https://api.openai.com/v1/chat/completions
LLM_TIMEOUT_SECONDS=30

CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001
```

**Never commit `.env` or real API keys to GitHub.**

---

# Database

The project uses **SQLite** with SQLAlchemy ORM.

The database is automatically initialized when the FastAPI application starts.

```text
backend/ps03.db
```

No manual database creation is required.

The database contains:

* Jobs
* Candidates
* Matches
* Analyses

---

# Run the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# API Endpoints

| Method | Endpoint                         | Purpose                                    |
| ------ | -------------------------------- | ------------------------------------------ |
| GET    | `/api/health`                    | Check API and database health              |
| POST   | `/api/jobs`                      | Create and analyze a job                   |
| GET    | `/api/jobs`                      | Get all jobs                               |
| GET    | `/api/jobs/{job_id}`             | Get a specific job                         |
| DELETE | `/api/jobs/{job_id}`             | Delete a job and related records           |
| POST   | `/api/resumes/upload`            | Upload multiple PDF/DOCX resumes           |
| GET    | `/api/candidates`                | Get all candidates                         |
| GET    | `/api/candidates/{candidate_id}` | Get candidate details                      |
| DELETE | `/api/candidates/{candidate_id}` | Delete candidate and related records       |
| POST   | `/api/matching/run/{job_id}`     | Run screening and return ranked candidates |

---

# Example API Workflow

### Step 1 — Create a Job

```bash
curl -X POST http://localhost:8000/api/jobs \
-H "Content-Type: application/json" \
-d "{\"title\":\"Python Backend Developer\",\"description\":\"Looking for a Python developer with FastAPI, SQL and Docker experience.\"}"
```

### Step 2 — Upload Resumes

```bash
curl -X POST http://localhost:8000/api/resumes/upload \
-F "files=@resume1.pdf" \
-F "files=@resume2.docx"
```

Multiple resumes can be uploaded in one request.

### Step 3 — Run Matching

```bash
curl -X POST http://localhost:8000/api/matching/run/1
```

The API returns ranked candidates with:

* Match score
* Skill score
* Experience score
* Education score
* Other fit score
* Matched skills
* Missing skills
* Weak skills
* Strengths
* Concerns
* Recommendation
* Explanation
* Recruiter summary

---

# Seed Demo Data

The project includes synthetic demo data for testing the complete workflow.

Run:

```bash
python seed.py
```

This generates:

* 3 sample jobs
* 10 synthetic candidates

Then start the backend:

```bash
uvicorn main:app --reload
```

Run matching for a job:

```bash
curl -X POST http://localhost:8000/api/matching/run/1
```

---

# Testing

Run the test suite:

```bash
pytest -q
```

Tests cover:

* Database initialization
* API health
* Job creation
* Resume upload
* Candidate creation
* PDF/DOCX parsing
* Deterministic score calculation
* Matching workflow
* Skill-gap analysis
* Error handling
* Acceptance workflow

The complete MVP workflow can be tested using synthetic data.

---

# Frontend Connection

The frontend communicates with the FastAPI backend through REST APIs.

For local development:

```text
Frontend
http://localhost:3000

        ↓ REST API

Backend
http://localhost:8000
```

Example JavaScript request:

```javascript
const response = await fetch(
  "http://localhost:8000/api/jobs"
);

const result = await response.json();
console.log(result);
```

The backend uses a consistent response structure:

### Success

```json
{
  "success": true,
  "data": {},
  "message": "Request completed successfully"
}
```

### Error

```json
{
  "success": false,
  "data": null,
  "message": "Request failed",
  "error": "ERROR_CODE"
}
```

---

# Complete Screening Workflow

```text
Recruiter
    ↓
Create Job
    ↓
Job Agent
    ↓
Extract Job Requirements
    ↓
Upload Resumes
    ↓
PDF/DOCX Parser
    ↓
Resume Agent
    ↓
Create Candidate Profiles
    ↓
Matching Agent
    ↓
Deterministic Scoring
    ↓
Skill Gap Agent
    ↓
Recruiter Agent
    ↓
Save Matches & Analysis
    ↓
Rank Candidates
    ↓
Recruiter Review
```

---

# Security

The backend implements basic MVP security practices:

* API keys stored in environment variables
* `.env` excluded from Git
* Uploaded file type validation
* File size limits
* Filename sanitization
* Malformed document handling
* Pydantic request validation
* Uploaded files are not executed

---

# Current Limitations

This is a hackathon MVP.

* SQLite is intended for local/MVP usage rather than high-concurrency production workloads.
* Scanned image-only PDFs require OCR for reliable extraction.
* The local fallback extraction is heuristic and less capable than an LLM.
* Authentication and authorization are outside the current MVP scope.

---

# Team

**Project:** PS03 — Multi-Agent Resume Screening & Job Matching Platform

**Hackathon:** Kurukshetra 2.0 — Hackfest 2026

**Problem ID:** PS03

**Team:** KH096 Tech Pluse

**GitHub:**
https://github.com/withshiv-m/KH096-Tech_pluse

---

# License

This project was developed as a hackathon prototype.

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will then be available on the local development URL shown in your terminal.

---

#  Backend Setup

Open a new terminal and navigate to the backend:

```bash
cd backend
```

Install the required backend dependencies according to the backend configuration.

Then start the backend server.

Example:

```bash
python app.py
```

or, if your project uses another backend entry point:

```bash
python main.py
```

---

#  Environment Variables

If the project requires environment variables, create a `.env` file inside the appropriate directory.

Example:

```env
API_KEY=your_api_key
DATABASE_URL=your_database_url
```

###  Important

Never commit your real API keys, passwords, or secret credentials to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
```

---

#  Frontend ↔ Backend

The frontend communicates with the backend through API requests.

```text
Frontend
   │
   │ HTTP Request
   ▼
Backend API
   │
   │ Processing
   ▼
Data / Services
   │
   ▼
Backend Response
   │
   ▼
Frontend UI
```

Make sure the backend server is running before testing frontend features that depend on APIs.

---

#  Screenshots

Add screenshots of the application here.

Example:

```markdown
![Home Page](screenshots/home.png)

![Dashboard](screenshots/dashboard.png)
```

Recommended screenshots:

*  Home page
*  Dashboard
*  Login/Register
*  Mobile responsive view
*  Main application functionality

---

#  Deployment

The project can be deployed using modern cloud hosting platforms.

### Frontend

Possible platforms:

* GitHub Pages
* Vercel
* Netlify

### Backend

Possible platforms:

* Render
* Railway
* AWS
* Other cloud platforms


#  Future Improvements

Future versions of Tech Pulse can include:

*  AI-powered features
*  Advanced authentication
*  Analytics dashboard
*  Real-time notifications
*  Progressive Web App support
*  Cloud database integration
*  Improved performance
*  Real-time API updates
*  Intelligent automation
*  Advanced data visualization

---

#  Testing

Before deployment, test:

* Frontend navigation
* API connectivity
* Form validation
* Backend endpoints
* Error handling
* Responsive design
* Different screen sizes
* Invalid user inputs

---

#  Team

### Tech Pulse Team

| Member           | Role                |
| ---------------- | ------------------- |
| Shivprasad Mugle | frontend Developer  |
| Aryan Bhosale    | Backend Developer   |
| Siddesh Tavhare  | Database manager    |
| Sarthak Tekale   | presentation expert |

> Update the team members and their roles according to your actual team.

---

#🌟 Why Tech Pulse?

Tech Pulse focuses on combining:

```text
 Innovation
      +
 Modern Web Development
      +
 Scalable Backend
      +
 Future AI Integration
      =
 Practical Technology Solution
```

The project is designed with scalability and real-world usability in mind.

---

#  License

This project is developed for educational, hackathon, and demonstration purposes.

---

**Repository:**
https://github.com/withshiv-m/KH096-Tech_pluse





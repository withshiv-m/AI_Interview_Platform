from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIResponse(BaseModel):
    success: bool
    data: Any = None
    message: str
    error: Optional[str] = None


class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=10)


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    job_id: int
    title: str
    description: str
    extracted_requirements: Any
    required_skills: List[str]
    preferred_skills: List[str]
    minimum_experience: float
    education_requirements: str
    other_requirements: List[str]
    created_at: Any
    updated_at: Any


class CandidateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    candidate_id: int
    name: str
    email: str
    phone: str
    education: str
    experience: float
    skills: List[str]
    projects: List[str]
    certifications: List[str]
    relevant_experience: List[str]
    resume_filename: str
    resume_path: str
    raw_resume_text: str
    created_at: Any
    updated_at: Any


class MatchResult(BaseModel):
    candidate_id: int
    candidate_name: str
    score: float
    skill_score: float
    experience_score: float
    education_score: float
    other_fit_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    weak_skills: List[str]
    strengths: List[str]
    concerns: List[str]
    recommendation: str
    explanation: str
    recruiter_summary: str


class ScreeningResponse(BaseModel):
    job_id: int
    results: List[MatchResult]


class AgentJobOutput(BaseModel):
    title: str = ""
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    minimum_experience: float = 0
    education_requirements: str = ""
    other_requirements: List[str] = []

    @field_validator("minimum_experience", mode="before")
    @classmethod
    def parse_experience(cls, value):
        try:
            return max(0.0, float(value))
        except (TypeError, ValueError):
            return 0.0


class AgentResumeOutput(BaseModel):
    name: str = "Unknown Candidate"
    email: str = ""
    phone: str = ""
    education: str = ""
    experience: float = 0
    skills: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []
    relevant_experience: List[str] = []

    @field_validator("experience", mode="before")
    @classmethod
    def parse_experience(cls, value):
        try:
            return max(0.0, float(value))
        except (TypeError, ValueError):
            return 0.0


class AgentMatchingOutput(BaseModel):
    matched_skills: List[str] = []
    candidate_job_fit: str = ""
    skill_observations: List[str] = []
    experience_observations: List[str] = []
    education_observations: List[str] = []


class AgentSkillGapOutput(BaseModel):
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    weak_skills: List[str] = []
    improvement_areas: List[str] = []


class AgentRecruiterOutput(BaseModel):
    strengths: List[str] = []
    concerns: List[str] = []
    recommendation: str = "Review"
    explanation: str = ""
    recruiter_summary: str = ""

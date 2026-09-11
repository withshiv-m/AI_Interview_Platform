from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    extracted_requirements = Column(Text, default="{}")
    required_skills = Column(Text, default="[]")
    preferred_skills = Column(Text, default="[]")
    minimum_experience = Column(Float, default=0)
    education_requirements = Column(Text, default="")
    other_requirements = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    matches = relationship("Match", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"
    candidate_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, default="Unknown Candidate")
    email = Column(String(320), default="")
    phone = Column(String(50), default="")
    education = Column(Text, default="")
    experience = Column(Float, default=0)
    skills = Column(Text, default="[]")
    projects = Column(Text, default="[]")
    certifications = Column(Text, default="[]")
    relevant_experience = Column(Text, default="[]")
    resume_filename = Column(String(255), nullable=False)
    resume_path = Column(String(1000), nullable=False)
    raw_resume_text = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    matches = relationship("Match", back_populates="candidate", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"
    match_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    other_fit_score = Column(Float, nullable=False)
    matched_skills = Column(Text, default="[]")
    missing_skills = Column(Text, default="[]")
    weak_skills = Column(Text, default="[]")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    job = relationship("Job", back_populates="matches")
    candidate = relationship("Candidate", back_populates="matches")
    analysis = relationship("Analysis", back_populates="match", uselist=False, cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"
    analysis_id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.match_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False, index=True)
    strengths = Column(Text, default="[]")
    concerns = Column(Text, default="[]")
    skill_gaps = Column(Text, default="[]")
    recommendation = Column(String(100), default="Review")
    explanation = Column(Text, default="")
    recruiter_summary = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    match = relationship("Match", back_populates="analysis")
    job = relationship("Job")
    candidate = relationship("Candidate")

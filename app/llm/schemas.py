from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class JobAnalysis(BaseModel):
    core_responsibilities: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    seniority_level: Optional[str] = None


class ResumeExperience(BaseModel):
    experience_title: str
    company: Optional[str] = None
    duration: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)


class ResumeProject(BaseModel):
    project_name: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class ResumeData(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experiences: List[ResumeExperience] = Field(default_factory=list)
    projects: List[ResumeProject] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)


class ExperienceMatchItem(BaseModel):
    experience_title: str
    relevance_score: int
    matched_skills: List[str] = Field(default_factory=list)
    reason: str


class MatchedExperienceResponse(BaseModel):
    matched_experiences: List[ExperienceMatchItem] = Field(default_factory=list)


class TailoredExperience(BaseModel):
    experience_title: str
    original_bullets: List[str] = Field(default_factory=list)
    rewritten_bullets: List[str] = Field(default_factory=list)
    target_skills_emphasized: List[str] = Field(default_factory=list)


class RewriteBulletsResponse(BaseModel):
    tailored_experiences: List[TailoredExperience] = Field(default_factory=list)


class DraftEmailResponse(BaseModel):
    subject: str
    email_body: str
    key_points_used: List[str] = Field(default_factory=list)


class InterviewQuestion(BaseModel):
    question: str
    why_this_might_be_asked: str
    candidate_angle: str


class StoryBankItem(BaseModel):
    experience_title: str
    topic: str
    why_it_matters_for_this_job: str
    key_points_to_mention: List[str] = Field(default_factory=list)


class SkillGapItem(BaseModel):
    area: str
    reason: str
    how_to_handle_in_interview: str


class InterviewPrepResponse(BaseModel):
    likely_interview_topics: List[str] = Field(default_factory=list)
    likely_questions: List[InterviewQuestion] = Field(default_factory=list)
    story_bank: List[StoryBankItem] = Field(default_factory=list)
    skill_gaps_or_risky_areas: List[SkillGapItem] = Field(default_factory=list)

from .client import call_llm_and_parse
from .prompts import (
    build_draft_email_prompt,
    build_interview_prep_prompt,
    build_job_analysis_prompt,
    build_match_experience_prompt,
    build_parse_resume_prompt,
    build_rewrite_bullets_prompt,
)

from .schemas import (
    JobAnalysis,
    ResumeData,
    MatchedExperienceResponse,
    RewriteBulletsResponse,
    DraftEmailResponse,
    InterviewPrepResponse,
)


def analyze_job_description(text: str) -> JobAnalysis:
    prompt = build_job_analysis_prompt(text)
    return call_llm_and_parse(prompt, JobAnalysis)


def parse_resume(text: str) -> ResumeData:
    prompt = build_parse_resume_prompt(text)
    return call_llm_and_parse(prompt, ResumeData)


def match_experience(text: str) -> MatchedExperienceResponse:
    prompt = build_match_experience_prompt(text)
    return call_llm_and_parse(prompt, MatchedExperienceResponse)


def rewrite_bullets(text: str) -> RewriteBulletsResponse:
    prompt = build_rewrite_bullets_prompt(text)
    return call_llm_and_parse(prompt, RewriteBulletsResponse)


def draft_email(text: str) -> DraftEmailResponse:
    prompt = build_draft_email_prompt(text)
    return call_llm_and_parse(prompt, DraftEmailResponse)


def interview_prep(text: str) -> InterviewPrepResponse:
    prompt = build_interview_prep_prompt(text)
    return call_llm_and_parse(prompt, InterviewPrepResponse)

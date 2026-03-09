from app.llm.helpers import analyze_job_description, parse_resume
from app.llm.schemas import JobAnalysis, ResumeData
from unittest.mock import patch


def test_analyze_job_description(sample_job_description):
    fake_result = JobAnalysis(
        core_responsibilities=[
            "Build backend services",
            "Develop frontend features",
        ],
        required_skills=["Python", "React", "REST APIs"],
        preferred_skills=["AWS"],
        technologies=["Python", "React", "REST APIs", "AWS"],
        seniority_level="Mid-level",
    )

    with patch(
        "app.llm.helpers.call_llm_and_parse", return_value=fake_result
    ) as mock_call:
        result = analyze_job_description(sample_job_description)
        print(result)
        assert isinstance(result, JobAnalysis)
        assert "Python" in result.required_skills
        mock_call.assert_called_once()

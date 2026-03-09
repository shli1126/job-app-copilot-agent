import json


def build_job_analysis_prompt(job_text: str) -> str:
    return f"""
You are a job analysis assistant.

Analyze the following job description and extract:
1. Core responsibilities
2. Required skills
3. Preferred skills
4. Technologies mentioned
5. Seniority level

Return ONLY valid JSON in this format:
{{
  "core_responsibilities": ["string"],
  "required_skills": ["string"],
  "preferred_skills": ["string"],
  "technologies": ["string"],
  "seniority_level": "string"
}}

RULES:
- Return ONLY JSON.
- Do not include markdown.
- Do not include explanation.
- If a field is missing, return null or an empty list.
- Extract information exactly from the job description text.
- Do not invent responsibilities, skills, technologies, and seniority level

Job description:
{job_text}
"""


def build_parse_resume_prompt(resume_text: str) -> str:
    return f"""
You are a resume parsing assistant.

Extract structured information from the resume.

Return ONLY valid JSON in the following format:

{{
  "full_name": "string or null",
  "email": "string or null",
  "skills": ["string"],
  "experiences": [
    {{
      "experience_title": "string",
      "company": "string or null",
      "duration": "string or null",
      "bullets": ["string"]
    }}
  ],
  "projects": [
    {{
      "project_name": "string",
      "description": "string or null",
      "technologies": ["string"]
    }}
  ],
  "education": ["string"]
}}

RULES:
- Return ONLY JSON.
- Do not include markdown.
- Do not include explanation.
- If a field is missing, return null or an empty list.
- Extract information exactly from the resume text.
- Do not invent experiences, projects, or skills.

Resume text:
{resume_text}
"""


def build_match_experience_prompt(parsed_resume, job_analysis) -> str:
    return f"""
You are a career assistant helping match a candidate's resume to a job description.

Your task is to analyze the candidate's experiences and determine which experiences best match the job requirements.

------------------------
JOB REQUIREMENTS
------------------------

Required skills:
{job_analysis["required_skills"]}

Technologies:
{job_analysis["technologies"]}

Core responsibilities:
{job_analysis["core_responsibilities"]}

------------------------
CANDIDATE RESUME
------------------------

Skills:
{parsed_resume["skills"]}

Experiences:
{parsed_resume["experiences"]}

Projects:
{parsed_resume["projects"]}

------------------------
TASK
------------------------

1. Identify which resume experiences are most relevant to the job.
2. For each relevant experience:
   - explain why it matches the job
   - identify which job skills it demonstrates
3. Rank the experiences by relevance.

------------------------
OUTPUT FORMAT (JSON)
------------------------

Return ONLY valid JSON in the following format:

{{
  "matched_experiences": [
    {{
      "experience_title": "...",
      "relevance_score": 1-10,
      "matched_skills": ["skill1", "skill2"],
      "reason": "short explanation"
    }}
  ]
}}

Do not include any text outside the JSON.
"""


def build_rewrite_bullets_prompt(
    parsed_resume, job_analysis, matched_experience
) -> str:
    resume_json = json.dumps(parsed_resume, indent=2, ensure_ascii=False)
    job_json = json.dumps(job_analysis, indent=2, ensure_ascii=False)
    match_json = json.dumps(matched_experience, indent=2, ensure_ascii=False)

    return f"""
You are an expert resume tailoring assistant.

Your job is to rewrite resume bullets so they better match the target job, while remaining fully truthful to the candidate's actual background.

TARGET JOB ANALYSIS:
{job_json}

CANDIDATE RESUME:
{resume_json}

MATCHED EXPERIENCE ANALYSIS:
{match_json}

TASK:
Rewrite the bullets for the matched experiences so they align more closely with the target job.

RULES:
1. Do not invent tools, projects, metrics, ownership, or achievements.
2. Do not claim the candidate did something not supported by the resume.
3. Keep bullets concise, strong, and professional.
4. Prefer action + scope + outcome format when possible.
5. Emphasize the most relevant skills, technologies, and responsibilities from the job analysis.
6. Preserve the original meaning of each bullet.
7. Improve clarity, impact, and job relevance.
8. Use language appropriate for a real resume, not a cover letter.
9. Each rewritten bullet should be one bullet only, not multiple sentences unless needed.
10. Return only valid JSON.

OUTPUT FORMAT:
{{
  "tailored_experiences": [
    {{
      "experience_title": "string",
      "original_bullets": [
        "string"
      ],
      "rewritten_bullets": [
        "string"
      ],
      "target_skills_emphasized": [
        "string"
      ]
    }}
  ]
}}

IMPORTANT:
- Rewrite only bullets for experiences that appear in the matched experience analysis.
- Keep the number of rewritten bullets aligned with the original bullets you choose to rewrite.
- If a bullet is already strong and relevant, you may keep it close to the original.
- Return JSON only, with no markdown and no extra commentary.
"""


def build_draft_email_prompt(job_analysis, matched_experience, tailored_bullets) -> str:
    job_json = json.dumps(job_analysis, indent=2, ensure_ascii=False)
    match_json = json.dumps(matched_experience, indent=2, ensure_ascii=False)
    bullets_json = json.dumps(tailored_bullets, indent=2, ensure_ascii=False)

    return f"""
You are an expert job application assistant.

Your task is to draft a concise, professional outreach email for a job application.

TARGET JOB ANALYSIS:
{job_json}

MATCHED EXPERIENCE:
{match_json}

TAILORED RESUME BULLETS:
{bullets_json}

TASK:
Write a short job application or recruiter outreach email that highlights the candidate's strongest fit for the role.

RULES:
1. Keep the tone professional, confident, and human.
2. Keep the email concise.
3. Use the candidate's most relevant experience and tailored bullets as supporting evidence.
4. Do not invent facts, names, or achievements.
5. Do not use overly generic or exaggerated language.
6. Mention only the most relevant qualifications.
7. Avoid sounding robotic or overly formal.
8. Return only valid JSON.

OUTPUT FORMAT:
{{
  "subject": "string",
  "email_body": "string",
  "key_points_used": [
    "string"
  ]
}}

EMAIL GOAL:
- Express interest in the role
- Briefly explain why the candidate is a good fit
- Reference 2 to 3 relevant strengths from the experience/bullets
- End with a polite close

IMPORTANT:
- Do not include placeholders like [Company Name] or [Hiring Manager] unless that information is truly unavailable from the inputs.
- If company name is unavailable, keep the wording natural without forcing it.
- Return JSON only, with no markdown and no extra commentary.
"""


def build_interview_prep_prompt(job_analysis, matched_experience) -> str:
    job_json = json.dumps(job_analysis, indent=2, ensure_ascii=False)
    match_json = json.dumps(matched_experience, indent=2, ensure_ascii=False)

    return f"""
You are an interview preparation assistant.

Your task is to prepare the candidate for interviews based on the target job and the candidate's most relevant matched experience.

TARGET JOB ANALYSIS:
{job_json}

MATCHED EXPERIENCE:
{match_json}

TASK:
Create a practical interview prep package tailored to this job and the candidate's likely strongest stories.

RULES:
1. Focus on likely interview areas based on the job requirements.
2. Ground all suggested talking points in the matched candidate experience.
3. Do not invent unsupported projects or accomplishments.
4. Include both technical and behavioral preparation where appropriate.
5. Keep content practical and specific.
6. Return only valid JSON.

OUTPUT FORMAT:
{{
  "likely_interview_topics": [
    "string"
  ],
  "likely_questions": [
    {{
      "question": "string",
      "why_this_might_be_asked": "string",
      "candidate_angle": "string"
    }}
  ],
  "story_bank": [
    {{
      "experience_title": "string",
      "topic": "string",
      "why_it_matters_for_this_job": "string",
      "key_points_to_mention": [
        "string"
      ]
    }}
  ],
  "skill_gaps_or_risky_areas": [
    {{
      "area": "string",
      "reason": "string",
      "how_to_handle_in_interview": "string"
    }}
  ]
}}

IMPORTANT:
- likely_interview_topics should reflect the main job requirements.
- likely_questions should be realistic questions a recruiter, hiring manager, or engineer might ask.
- candidate_angle should explain how the candidate can answer based on their real background.
- story_bank should help the candidate prepare strong examples.
- skill_gaps_or_risky_areas should identify places where the job asks for something stronger than the candidate background, if any.
- Return JSON only, with no markdown and no extra commentary.
"""

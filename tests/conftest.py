import pytest


@pytest.fixture
def sample_job_description():
    return """
    We are hiring a Full Stack Engineer to build and maintain web applications.
    Requirements:
    - Strong Python experience
    - Experience with React
    - Familiarity with REST APIs
    - Experience with AWS is a plus
    Responsibilities:
    - Build backend services
    - Develop frontend features
    - Collaborate with product and design
    """


@pytest.fixture
def sample_resume():
    return """
    Shaolong Li
    shaolong@example.com

    Skills:
    Python, React, Node.js, AWS

    Experience:
    Full Stack Developer
    - Built REST APIs using Python and Node.js
    - Developed frontend components using React

    Education:
    UC San Diego, MS in Computer Science
    """
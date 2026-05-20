import pytest

@pytest.fixture
def valid_job():
    return {
        "external_id": "job-1001",
        "title": "Backend Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "description": "A" * 50,
        "url": "https://example.com/jobs/1001",
        "posted_at": "2026-05-01T10:00:00Z"
    }

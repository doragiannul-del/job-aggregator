from main import VALID_SCHEMA
from jsonschema import validate, ValidationError, FormatChecker
import pytest


def test_valid_job_passes_validation(valid_job):
    validate(instance=valid_job, schema=VALID_SCHEMA, format_checker=FormatChecker())


def test_job_missing_title_fails():
    job = {
        "external_id": "job-1001",
        "company": "TechCorp",
        "location": "Remote",
        "description": "A" * 50,
        "url": "https://example.com/jobs/1001"
    }
    with pytest.raises(ValidationError):
        validate(instance=job, schema=VALID_SCHEMA, format_checker=FormatChecker())


def test_job_invalid_url_fails():
    job = {
        "external_id": "job-1001",
        "title": "Backend Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "description": "A" * 50,
        "url": "not-a-valid-url",
        "posted_at": "2026-05-01T10:00:00Z"
    }
    with pytest.raises(ValidationError):
        validate(instance=job, schema=VALID_SCHEMA, format_checker=FormatChecker())


def test_job_short_description_fails():
    job = {
        "external_id": "job-1001",
        "title": "Backend Engineer",
        "company": "TechCorp",
        "location": "Remote",
        "description": "Too short",
        "url": "https://example.com/jobs/1001",
        "posted_at": "2026-05-01T10:00:00Z"
    }
    with pytest.raises(ValidationError):
        validate(instance=job, schema=VALID_SCHEMA, format_checker=FormatChecker())

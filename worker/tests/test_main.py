from main import normalise_job

def test_normalise_job():
    job = {"title": "  Backend Engineer  ", "company": "TechCorp ", "location": "remote"}
    result = normalise_job(job)
    assert result["title"] == "Backend Engineer"
    assert result["company"] == "TechCorp"
    assert result["location"] == "Remote"
    
def test_normalise_salary():
    job = {"title": "Engineer", "company": "TechCorp ", "location": "remote", "salary_min": 90000, "salary_max": 50000}
    result = normalise_job(job)
    assert result["salary_min"] == 50000
    assert result["salary_max"] == 90000

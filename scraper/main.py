from jsonschema import validate, ValidationError, FormatChecker
import json

valid_schema = {
    "type": "object",
    "properties": {
        "external_id": {"type": "string", "minLength": 1},
        "title": {"type": "string", "minLength": 1},
        "company": {"type": "string", "minLength": 1},
        "location": {"type": "string", "minLength": 1},
        "description": {"type": "string", "minLength": 50},
        "salary_min": {"type": ["number", "null"], "minimum": 0},
        "salary_max": {"type": ["number", "null"], "minimum": 0},
        "url": {"type": "string", "format": "uri"},
        "posted_at": {"type": "string", "format": "date-time"}
},
    "required": ["external_id", "title", "company", "location", "description", "url"]
}

with open('data/mock_jobs.json', 'r') as file:
    jobs = json.load(file)
    #print(json.dumps(jobs, indent=4))

valid_jobs = 0
invalid_jobs = 0
for job in jobs:
    # validate job item
    try:
        validate(instance=job, schema=valid_schema, format_checker=FormatChecker())
        valid_jobs += 1
    except ValidationError as error:
        job_id = job.get("external_id", "unknown")
        print(f"Invalid job: {job_id}")
        print(f"Reason: {error.message}")
        invalid_jobs += 1
        continue
    
print(f"Found {valid_jobs} valid jobs and {invalid_jobs} invalid jobs")


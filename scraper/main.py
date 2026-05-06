import json
import os

import pika
from dotenv import load_dotenv
from jsonschema import FormatChecker, ValidationError, validate

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs_raw")

# connect to RMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
)
channel = connection.channel()

# create queue
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# schema to use for validating ingesting jobs
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
        "posted_at": {"type": "string", "format": "date-time"},
    },
    "required": ["external_id", "title", "company", "location", "description", "url"],
}

# read jobs from mock data in json file
with open("data/mock_jobs.json", "r") as file:
    jobs = json.load(file)
    # print(json.dumps(jobs, indent=4))

valid_jobs = 0
invalid_jobs = 0
for job in jobs:
    # validate & publish job item
    try:
        validate(instance=job, schema=valid_schema, format_checker=FormatChecker())

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(job),
            properties=pika.BasicProperties(),
        )
        print(f"Published: {job['external_id']}")
        valid_jobs += 1
    except ValidationError as error:
        job_id = job.get("external_id", "unknown")
        print(f"Invalid job: {job_id}")
        print(f"Reason: {error.message}")
        invalid_jobs += 1
        continue

connection.close()
print("Done. Connection to RMQ closed.")
print(f"Found {valid_jobs} valid jobs and {invalid_jobs} invalid jobs")

import json
import os

import pika
from dotenv import load_dotenv
from jsonschema import FormatChecker, ValidationError, validate

load_dotenv(dotenv_path="../.env")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
QUEUE_NAME = os.getenv("QUEUE_NAME")

# schema to use for validating ingesting jobs
VALID_SCHEMA = {
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


# connect to RMQ
def get_rabbitmq_channel():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel


def load_jobs(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def publish_jobs(channel, jobs):
    valid_jobs = 0
    invalid_jobs = 0

    for job in jobs:
        try:
            validate(instance=job, schema=VALID_SCHEMA, format_checker=FormatChecker())
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=json.dumps(job),
                properties=pika.BasicProperties(delivery_mode=2),
            )
            print(f"Published: {job['external_id']}")
            valid_jobs += 1
        except ValidationError as error:
            job_id = job.get("external_id", "unknown")
            print(f"Invalid job: {job_id} - {error.message}")
            invalid_jobs += 1

    return valid_jobs, invalid_jobs


def main():
    connection, channel = get_rabbitmq_channel()

    try:
        # read jobs from mock data in json file
        jobs = load_jobs("data/mock_jobs.json")
        valid_jobs, invalid_jobs = publish_jobs(channel, jobs)
    finally:
        connection.close()
        print("Done. Connection to RMQ closed.")

    print(f"Published {valid_jobs} valid jobs, skipped {invalid_jobs} invalid jobs")


if __name__ == "__main__":
    main()

import json
import os

import pika
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs")


def normalise_job(job):
    job["title"] = job["title"].strip()
    job["company"] = job["company"].strip()
    job["location"] = job["location"].strip().title()

    if job.get("salary_min") and job.get("salary_max"):
        if job["salary_min"] > job["salary_max"]:
            job["salary_min"], job["salary_max"] = job["salary_max"], job["salary_min"]

    return job


def process_job(channel, method, properties, body):
    try:
        job = json.loads(body)
        print(f"Received: {job['external_id']} - {job['title']}")

        job = normalise_job(job)

        channel.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Acknowledged: {job['external_id']}")

    except Exception as e:
        print(f"Failed to process message: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_job)

    print("Worker is running. Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()

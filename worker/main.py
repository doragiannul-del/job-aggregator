import json
import os

import pika
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
QUEUE_NAME = os.getenv("QUEUE_NAME")


def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
    )


def normalise_job(job):
    job["title"] = job["title"].strip()
    job["company"] = job["company"].strip()
    job["location"] = job["location"].strip().title()

    if job.get("salary_min") and job.get("salary_max"):
        if job["salary_min"] > job["salary_max"]:
            job["salary_min"], job["salary_max"] = job["salary_max"], job["salary_min"]

    return job


def save_job(job):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO jobs (
                    external_id, title, company, location,
                    description, salary_min, salary_max, url, posted_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (external_id) DO NOTHING
            """,
                (
                    job["external_id"],
                    job["title"],
                    job["company"],
                    job["location"],
                    job["description"],
                    job.get("salary_min"),
                    job.get("salary_max"),
                    job["url"],
                    job["posted_at"],
                ),
            )
        conn.commit()
        print(f"Saved: {job['external_id']}")
    except Exception as e:
        conn.rollback()
        print(f"DB error: {e}")
        raise
    finally:
        conn.close()


def process_job(channel, method, properties, body):
    try:
        job = json.loads(body)
        print(f"Received: {job['external_id']} - {job['title']}")

        job = normalise_job(job)
        save_job(job)

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

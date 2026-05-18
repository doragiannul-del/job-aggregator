# Job Aggregator

This project simulates a real-world job aggregation pipeline.
A simplified event-driven backend system that collects, processes, and serves job postings.

---

## Why this project?

The goal is to explore event-driven architecture and build a small distributed system using Python and Go.

---

## Features

- Job ingestion (from mock data initially)
- Asynchronous processing via message queue
- Storage in a relational database
- API for querying job listings

---

## Architecture

The system will consist of:

- Scraper (Python)
- Queue (RabbitMQ)
- Worker (Python)
- Database (PostgreSQL)
- API (FastAPI)

For a more detailed explanation, see [ARCHITECTURE.md](ARCHITECTURE.md).

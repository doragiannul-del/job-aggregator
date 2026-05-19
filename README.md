# Job Aggregator

This project simulates a real-world job aggregation pipeline.
A simplified event-driven backend system that collects, processes, and serves job postings.

---

## Why this project?

The goal is to explore event-driven architecture and build a small distributed system using Python.

---

## Features

- Job ingestion (from mock data initially)
- Asynchronous processing via message queue
- Storage in a relational database
- API for querying job listings

---

## Architecture

The system consist of:

- Scraper (Python)
- Queue (RabbitMQ)
- Worker (Python)
- Database (PostgreSQL)
- API (FastAPI)

For a more detailed explanation, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Running Locally

### Prerequisites
- Docker Desktop
- Python 3.11+
- uv

### Setup

1. Clone the repo
```bash
   git clone 
   cd job-aggregator
```

2. Copy the example env file and fill in your values
```bash
   cp .env.example .env
```

3. Start infrastructure
```bash
   make up
```

4. Run the worker (in a new terminal)
```bash
   make worker
```

5. Run the scraper (in a new terminal)
```bash
   make scraper
```

### Code Quality

```bash
make lint      # check for issues
make format    # auto-fix formatting
```

---

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make up` | Start RabbitMQ and PostgreSQL |
| `make down` | Stop all containers |
| `make logs` | Follow container logs |
| `make scraper` | Run the scraper |
| `make worker` | Run the worker |
| `make db-connect` | Connect to PostgreSQL shell |
| `make lint` | Check code quality with ruff on all services |
| `make format` | Format code with ruff on all services |

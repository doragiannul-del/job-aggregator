# Architecture

## Overview

This project implements a simplified job aggregation system using an event-driven architecture.

The system is designed to simulate how job data is collected, processed asynchronously, and made available through a search API.

---

## High-Level Architecture


+-------------+       +----------+       +-------------+       +------------+
| Scraper     | ----> | RabbitMQ | ----> | Worker      | ----> | PostgreSQL |
| (Python)    |       |          |       | (Go)        |       |            |
+-------------+       +----------+       +-------------+       +------------+
                                                              |
                                                              v
                                                        +-------------+
                                                        | FastAPI API |
                                                        | (Python)    |
                                                        +-------------+


---

## Components

### Scraper (Python)
Generates job data (currently from mock JSON) and publishes messages to RabbitMQ.

### Queue (RabbitMQ)
Acts as a buffer between producers and consumers, enabling asynchronous processing.

### Worker (Go)
Consumes job messages, validates and normalizes them, and stores them in PostgreSQL.

### Database (PostgreSQL)
Stores job postings and supports querying by the API.

### API (FastAPI)
Provides endpoints to search and retrieve job postings.

## Data Flow

1. Scraper produces job messages
2. Messages are sent to RabbitMQ
3. Worker consumes and processes messages
4. Jobs are stored in PostgreSQL
5. API queries the database and returns results

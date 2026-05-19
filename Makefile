.PHONY: up down logs scraper worker db-connect db-check lint format

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

scraper:
	cd scraper && uv run python main.py

worker:
	cd worker && uv run python main.py

db-connect:
	docker exec -it postgres psql -U jobuser -d jobsdb

lint:
	cd scraper && uv run ruff check .
	cd worker && uv run ruff check .

format:
	cd scraper && uv run ruff format .
	cd worker && uv run ruff format .
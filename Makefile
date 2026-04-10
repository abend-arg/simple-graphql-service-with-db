.PHONY: install run migrate migrate-local new-migration seed

install:
	uv sync

run:
	uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload

migrate:
	uv run python -m scripts.apply_migrations

migrate-local:
	uv run python -m scripts.create_local_db

new-migration:
	uv run alembic revision --autogenerate -m "$(msg)"

seed:
	uv run python -m scripts.seed

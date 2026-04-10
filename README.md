# Simple GraphQL Service With DB

GraphQL service built with FastAPI, Strawberry, and SQLAlchemy.

## Requirements

- Python 3.12
- `uv`

## Local setup

Create the virtual environment and install dependencies:

```bash
uv sync
```

This creates `.venv` if it does not exist and installs both runtime and development dependencies.

If you prefer shorthand commands, the project also includes a `Makefile`:

```bash
make install
```

## Local database

This project no longer creates the database automatically when the service starts. Schema management is handled through Alembic.

### 1. Apply existing migrations

For local development with SQLite:

```bash
uv run python -m scripts.create_local_db
make migrate-local
```

This script is intended for local SQLite usage and applies all migrations to the default `app.db` database.

### 2. Apply migrations in any environment

Use this command when you want to apply migrations in CI, CD, staging, or production:

```bash
uv run python -m scripts.apply_migrations
make migrate
```

It uses the current `DATABASE_URL` and runs `alembic upgrade head`.

### 3. Create a new migration

Whenever you change the models and want to version that schema change:

```bash
uv run alembic revision --autogenerate -m "describe schema change"
make new-migration msg="describe schema change"
```

Review the generated migration file under `alembic/versions/` before committing it.

### 4. Seed demo data

Load sample records:

```bash
uv run python -m scripts.seed
make seed
```

The seed is idempotent at the `ConstructModel.name` level, so it will not insert the same constructs again if you run it multiple times.

## Run the service locally

Once the database has been migrated:

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
make run
```

Endpoints:

- `GET /health`
- `POST /graphql`
- `GET /graphql`

## Recommended local workflow

For the first local run:

```bash
uv sync
uv run python -m scripts.create_local_db
uv run python -m scripts.seed
uv run uvicorn main:app --reload
```

Using `make`:

```bash
make install
make migrate-local
make seed
make run
```

For subsequent schema changes:

```bash
uv run alembic revision --autogenerate -m "describe schema change"
uv run python -m scripts.create_local_db
uv run uvicorn main:app --reload
```

Using `make`:

```bash
make new-migration msg="describe schema change"
make migrate-local
make run
```

## Production

In production, the standard approach is to avoid creating tables from the application at startup. The service should assume that the database already exists and that the schema is managed through migrations.

Recommended flow:

1. Provision the database.
2. Configure `DATABASE_URL`.
3. Run Alembic migrations.
4. Only then start the service.

Example:

```bash
DATABASE_URL="postgresql+psycopg://user:password@host/dbname" uv run python -m scripts.apply_migrations
DATABASE_URL="postgresql+psycopg://user:password@host/dbname" uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

With `make`:

```bash
DATABASE_URL="postgresql+psycopg://user:password@host/dbname" make migrate
DATABASE_URL="postgresql+psycopg://user:password@host/dbname" make run
```

Notes:

- `scripts.apply_migrations` is the environment-agnostic entrypoint for schema upgrades.
- `scripts.create_local_db` is only a local SQLite convenience wrapper.
- If the migration process runs in the same environment, that environment must have `alembic` installed.
- If you want a smaller runtime environment, a common approach is to run migrations in a separate image or job with development dependencies, and keep the web process limited to runtime dependencies only.
- The migration command usually runs in a deploy job, entrypoint, or release phase that is separate from the web process.
- Demo seed data should not be loaded in production.
- If you need required system data, handle it separately through controlled, idempotent migrations or seed routines.

## Environment variables

- `DATABASE_URL`: defaults to `sqlite:///./app.db`

## Make targets

- `make install`: create the virtual environment and install dependencies
- `make run`: run the application locally with auto-reload
- `make migrate`: apply migrations using the current `DATABASE_URL`
- `make migrate-local`: apply migrations to the local SQLite database
- `make new-migration msg="..."`: generate a new Alembic migration
- `make seed`: load demo seed data

import os

DEFAULT_SYNC_DATABASE_URL = "sqlite:///./app.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_SYNC_DATABASE_URL)


def get_async_database_url() -> str:
    database_url = get_database_url()
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    return database_url


def get_sync_database_url() -> str:
    database_url = get_database_url()
    if database_url.startswith("sqlite+aiosqlite:///"):
        return database_url.replace("sqlite+aiosqlite:///", "sqlite:///", 1)
    return database_url

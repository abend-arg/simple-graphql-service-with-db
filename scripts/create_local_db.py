import os

from scripts.apply_migrations import apply_migrations


def create_local_db() -> None:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    if not database_url.startswith("sqlite"):
        raise ValueError(
            "scripts.create_local_db is intended for local SQLite databases only. "
            "Use scripts.apply_migrations for shared environments."
        )

    apply_migrations()


if __name__ == "__main__":
    create_local_db()

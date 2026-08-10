"""
create_tables.py
----------------
Create all SQLAlchemy-mapped tables in the database (idempotent).

Also ensures the pgvector extension exists, which is required by
the embedding columns, and patches any missing column defaults that
SQLAlchemy's server_default cannot set retroactively on existing tables.

Usage (run from the backend/ directory):
    python -m app.scripts.create_tables
"""

from sqlalchemy import text

from app.database.session import engine
from app.database.base import Base

# Import every model so Base.metadata knows about all tables.
import app.models  # noqa: F401 — side-effect import registers all models

# Tables whose created_at/updated_at need a server default applied after
# create_all (handles tables created before the default was in the ORM model).
_TIMESTAMPED_TABLES = [
    "knowledge_documents",
    "disease_detections",
    "farms",
    "crops",
    "users",
    "refresh_tokens",
]


def main() -> None:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
        print("pgvector extension ready.")

    Base.metadata.create_all(bind=engine)
    print("All tables created (or already exist).")

    # Ensure server defaults exist on timestamp columns for all known tables.
    with engine.connect() as conn:
        for table in _TIMESTAMPED_TABLES:
            conn.execute(text(
                f"ALTER TABLE IF EXISTS {table} "
                f"ALTER COLUMN created_at SET DEFAULT now(), "
                f"ALTER COLUMN updated_at SET DEFAULT now()"
            ))
        conn.commit()
    print("Timestamp defaults ensured.")


if __name__ == "__main__":
    main()

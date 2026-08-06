"""
load_knowledge.py
-----------------
Ingest a knowledge file into the knowledge_documents table.

Supported formats
  .pdf  – parsed with pypdf and split into chunks
  .txt  – plain-text blocks separated by blank lines (crop/disease/symptoms/treatment)
  .json – JSON array of knowledge record dicts

Usage (run from the backend/ directory):
    python -m app.scripts.load_knowledge
    python -m app.scripts.load_knowledge data/pdfs/my_guide.pdf
    python -m app.scripts.load_knowledge data/pdfs/records.json
"""

import sys
from pathlib import Path

from app.database.session import SessionLocal
from app.services.pdf_ingestion import ingest_pdf
from app.services.knowledge_ingestion import ingest_from_text, ingest_from_json

# backend/ — resolved from this file's location so it never depends on cwd
BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_FILE = BASE_DIR / "app" / "data" / "pdfs" / "tomato_disease_guide.txt"


def main() -> None:
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if not file_path.is_absolute():
            file_path = Path.cwd() / file_path
    else:
        file_path = DEFAULT_FILE

    if not file_path.exists():
        print(f"Error: file not found at {file_path}")
        print(
            "Place the file there, or pass a path as an argument:\n"
            "  python -m app.scripts.load_knowledge <path/to/file>"
        )
        sys.exit(1)

    db = SessionLocal()
    try:
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            inserted = ingest_pdf(db=db, pdf_path=file_path)
            print(f"Done — inserted {inserted} chunk(s) from '{file_path.name}'.")

        elif suffix == ".txt":
            summary = ingest_from_text(db=db, path=file_path)
            print(
                f"Done — inserted {summary['inserted']}, "
                f"skipped {summary['skipped']}, "
                f"errors {summary['errors']} "
                f"from '{file_path.name}'."
            )

        elif suffix == ".json":
            summary = ingest_from_json(db=db, path=file_path)
            print(
                f"Done — inserted {summary['inserted']}, "
                f"skipped {summary['skipped']}, "
                f"errors {summary['errors']} "
                f"from '{file_path.name}'."
            )

        else:
            print(f"Error: unsupported file type '{suffix}'. Use .pdf, .txt, or .json.")
            sys.exit(1)

    finally:
        db.close()


if __name__ == "__main__":
    main()

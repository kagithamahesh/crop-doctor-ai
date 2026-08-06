"""
document_ingestion.py
---------------------
Populates the `disease_knowledge` table from structured knowledge documents.

Supported input formats
  - List[dict]  – Python dicts already in memory (used by tests / seeding scripts)
  - JSON file   – a JSON array of knowledge records (path as str | Path)
  - Plain-text  – one record per block, separated by a blank line, each block
                  having the shape:
                      crop: <name>
                      disease: <name>
                      symptoms: <free text>
                      treatment: <free text>

Each record is embedded with the same sentence-transformer model used by
vector_search.py (all-MiniLM-L6-v2, 384 dims) and upserted into the DB.
Duplicate records (same crop + disease name) are skipped by default.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.disease_knowledge import DiseaseKnowledge
from app.services.embedding_service import generate_embedding

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_embedding_text(record: dict) -> str:
    """Concatenate the fields that capture semantic meaning for embedding."""
    parts = [
        record.get("crop_name", ""),
        record.get("disease_name", ""),
        record.get("symptoms", ""),
        record.get("treatment", ""),
    ]
    return " ".join(p for p in parts if p).strip()


def _parse_text_block(block: str) -> dict | None:
    """
    Parse a single blank-line-separated text block into a knowledge record.
    Returns None if required keys are missing.
    """
    record: dict = {}
    key_map = {
        "crop": "crop_name",
        "disease": "disease_name",
        "symptoms": "symptoms",
        "treatment": "treatment",
    }
    for line in block.strip().splitlines():
        if ":" not in line:
            continue
        raw_key, _, value = line.partition(":")
        canonical = key_map.get(raw_key.strip().lower())
        if canonical:
            record[canonical] = value.strip()

    required = {"crop_name", "disease_name", "symptoms", "treatment"}
    if not required.issubset(record):
        return None
    return record


def _records_from_text(text: str) -> list[dict]:
    """Split a plain-text document into per-record dicts."""
    blocks = [b for b in text.split("\n\n") if b.strip()]
    records = []
    for block in blocks:
        parsed = _parse_text_block(block)
        if parsed:
            records.append(parsed)
        else:
            logger.warning("Skipping malformed text block:\n%s", block[:120])
    return records


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ingest_records(
    db: Session,
    records: Iterable[dict],
    *,
    skip_duplicates: bool = True,
) -> dict[str, int]:
    """
    Embed and persist an iterable of knowledge record dicts.

    Each dict must contain the keys:
        crop_name, disease_name, symptoms, treatment

    Returns a summary dict: {"inserted": N, "skipped": N, "errors": N}
    """
    inserted = skipped = errors = 0

    for record in records:
        crop_name    = record.get("crop_name", "").strip()
        disease_name = record.get("disease_name", "").strip()
        symptoms     = record.get("symptoms", "").strip()
        treatment    = record.get("treatment", "").strip()

        if not all([crop_name, disease_name, symptoms, treatment]):
            logger.warning(
                "Skipping incomplete record: %s",
                {k: record.get(k) for k in ("crop_name", "disease_name")},
            )
            errors += 1
            continue

        if skip_duplicates:
            exists = (
                db.query(DiseaseKnowledge)
                .filter(
                    DiseaseKnowledge.crop_name == crop_name,
                    DiseaseKnowledge.disease_name == disease_name,
                )
                .first()
            )
            if exists:
                logger.debug(
                    "Duplicate skipped: %s / %s", crop_name, disease_name
                )
                skipped += 1
                continue

        text_for_embedding = _build_embedding_text(record)
        embedding = generate_embedding(text_for_embedding)

        entry = DiseaseKnowledge(
            crop_name=crop_name,
            disease_name=disease_name,
            symptoms=symptoms,
            treatment=treatment,
            embedding=embedding,
        )
        db.add(entry)
        inserted += 1
        logger.info("Ingested: %s / %s", crop_name, disease_name)

    db.commit()
    summary = {"inserted": inserted, "skipped": skipped, "errors": errors}
    logger.info("Ingestion complete: %s", summary)
    return summary


def ingest_from_json(
    db: Session,
    path: str | Path,
    *,
    skip_duplicates: bool = True,
) -> dict[str, int]:
    """
    Load a JSON file containing an array of knowledge records and ingest them.

    Example JSON structure:
    [
        {
            "crop_name": "Tomato",
            "disease_name": "Early Blight",
            "symptoms": "Brown spots with concentric rings on lower leaves.",
            "treatment": "Apply mancozeb-based fungicide; remove infected leaves."
        },
        ...
    ]
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a JSON array at the top level, got {type(data).__name__}"
        )

    logger.info(
        "Loading %d records from %s", len(data), file_path.name
    )
    return ingest_records(db, data, skip_duplicates=skip_duplicates)


def ingest_from_text(
    db: Session,
    path: str | Path,
    *,
    skip_duplicates: bool = True,
) -> dict[str, int]:
    """
    Load a plain-text file and ingest records.

    Records are separated by blank lines.  Each record must follow this format:

        crop: Tomato
        disease: Late Blight
        symptoms: Dark water-soaked lesions on leaves and stems.
        treatment: Remove infected plants; apply copper-based fungicide.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    records = _records_from_text(text)

    logger.info(
        "Parsed %d records from %s", len(records), file_path.name
    )
    return ingest_records(db, records, skip_duplicates=skip_duplicates)

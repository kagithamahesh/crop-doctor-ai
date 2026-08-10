from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session

from app.models.knowledge_document import KnowledgeDocument
from app.services.embedding_service import generate_embedding


def ingest_pdf(
    db: Session,
    pdf_path: str | Path,
):
    file_path = Path(pdf_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    # Validate PDF magic bytes before handing to pypdf
    with file_path.open("rb") as _f:
        header = _f.read(5)
    if header != b"%PDF-":
        raise ValueError(
            f"'{file_path.name}' is not a valid PDF file "
            f"(header: {header!r}). "
            "Use ingest_from_text() for plain-text knowledge files."
        )

    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(text)

    title = file_path.stem

    inserted = 0

    try:
        for chunk in chunks:
            embedding = generate_embedding(chunk)

            db.add(
                KnowledgeDocument(
                    title=title,
                    source=str(file_path),
                    chunk_text=chunk,
                    embedding=embedding,
                )
            )

            inserted += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    return inserted
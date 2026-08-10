from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge_document import KnowledgeDocument
from app.services.embedding_service import generate_embedding


def search_similar(
    db: Session,
    query: str,
    limit: int = 3,
):
    query_embedding = generate_embedding(query)

    stmt = (
        select(KnowledgeDocument)
        .order_by(
            KnowledgeDocument.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(limit)
    )

    return db.execute(stmt).scalars().all()
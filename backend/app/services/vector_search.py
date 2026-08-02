from sqlalchemy import select
from sqlalchemy.orm import Session


from app.models.disease_knowledge import DiseaseKnowledge
from app.services.embedding_service import generate_embedding

def search_similar(
    db: Session,
    query: str,
    limit: int = 3,
):
    query_embedding = generate_embedding(query)

    stmt = (
        select(DiseaseKnowledge)
        .order_by(
            DiseaseKnowledge.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(limit)
    )

    return db.execute(stmt).scalars().all()
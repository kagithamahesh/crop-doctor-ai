from app.database.session import SessionLocal
from app.services.vector_search import search_similar

async def knowledge_node(state: dict):
    db = SessionLocal()

    query = (
        f"{state['crop']} {state['disease']}"
    )

    docs = search_similar(
        db,
        query,
        limit=3,
    )

    state["knowledge"] = [
        {
            "disease": d.disease_name,
            "treatment": d.treatment,
        }
        for d in docs
    ]

    db.close()

    return state
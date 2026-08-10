from app.database.session import SessionLocal
from app.services.vector_search import search_similar


def main():
    db = SessionLocal()

    docs = search_similar(
        db=db,
        query="tomato late blight treatment",
        limit=3,
    )

    print(f"Retrieved {len(docs)} documents")
    print()

    for doc in docs:
        print(doc.title)
        print(doc.chunk_text)
        print("-" * 50)

    db.close()


if __name__ == "__main__":
    main()
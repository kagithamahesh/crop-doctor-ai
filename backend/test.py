from app.services.embedding_service import generate_embedding

vector = generate_embedding(
    "Tomato late blight causes brown leaf spots and fungal infection"
)

print(len(vector))
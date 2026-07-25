from app.core.auth import create_access_token

token = create_access_token(
    {"sub": "jack@gmail.com"}
)

print(token)
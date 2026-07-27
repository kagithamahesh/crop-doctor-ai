from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from app.core.config import settings

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except JWTError:
        return None

def create_refersh_token(data:dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = data.copy()

    payload.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.core.auth import create_access_token,create_refersh_token


def refresh_access_token(db: Session,
    refresh_token: str):

    token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == refresh_token,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if token is None:
        raise ValueError("Invalid refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise ValueError("Invalid refresh token")
    if payload.get("type") != "refresh":
        raise ValueError("Invalid token type")
    user_id = payload.get("sub")
    return {
        "access_token": create_access_token(
            {"sub": user_id}
        ),
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import verify_password
from app.core.auth import create_access_token,create_refersh_token

def login_User(db:Session,user:UserLogin):
     db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

     if not db_user:
        raise ValueError("Invalid email or password")

     if not verify_password(
        user.password,
        db_user.password_hash,
        ):
      raise ValueError("Invalid email or password")

     token = create_access_token(
            {"sub": str(db_user.id)}
        )
     refresh_token = create_refersh_token(
        {"sub": str(db_user.id)}
        )
   #   save the refresh token
     db_token = RefreshToken(
         token=refresh_token,
         user_id=db_user.id,
         expires_at=datetime.now(timezone.utc) + timedelta(days=7),
         )
     db.add(db_token)
     db.commit()
     return {
        "access_token": token,
        "refresh_token":refresh_token,
        "token_type": "bearer",
    }

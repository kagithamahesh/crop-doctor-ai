from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.models.user import User
from app.core.security import verify_password
from app.core.auth import create_access_token

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
     return {
        "access_token": token,
        "token_type": "bearer",
    }

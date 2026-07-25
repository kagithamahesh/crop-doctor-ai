from fastapi import APIRouter,Depends, HTTPException
from app.schemas.user import UserLogin, UserResponse,UserRegister,Token
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.services.auth_service import register_user
from app.services.login_service import login_User

router = APIRouter()

@router.post(
    "/login",
    response_model=Token,
)
def login(
    user:UserLogin ,
    db: Session = Depends(get_db),
):
    try:
        return login_User(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
    
@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
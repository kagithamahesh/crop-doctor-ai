from fastapi import APIRouter,Depends, HTTPException
from app.schemas.user import UserLogin, UserResponse,UserRegister,Token,RefreshTokenRequest
from sqlalchemy.orm import Session
from app.database.dependency import get_db
from app.services.auth_service import register_user
from app.services.login_service import login_User
from app.core.dependencies.auth import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from app.services.refresh_service import refresh_access_token
from app.models.refresh_token import RefreshToken
from app.core.dependencies.roles import require_roles
from app.services.user_service import get_all_users

router = APIRouter()


@router.get(
    "/users",
    response_model=list[UserResponse],
)
def users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    return get_all_users(db)

@router.post("/logout")
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    token = (
    db.query(RefreshToken)
    .filter(
        RefreshToken.token == request.refresh_token
    )
    .first()
)

    if token:
        token.revoked = True
        db.commit()

    return {
        "message": "Logged out successfully"
    }


    
@router.post(
    "/refresh",
    response_model=Token,
)

def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        db,
        request.refresh_token,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
  return current_user

@router.post(
    "/login",
    response_model=Token,
)
def login(
     form_data: OAuth2PasswordRequestForm = Depends(),
     db: Session = Depends(get_db),
    #user: UserLogin,
    #db: Session = Depends(get_db),
):

    user = UserLogin(
         email=form_data.username,
         password=form_data.password,
        #email=user.email,
        #password=user.password,
    )

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
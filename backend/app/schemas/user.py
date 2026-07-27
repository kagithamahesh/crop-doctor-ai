from pydantic import BaseModel, EmailStr

from uuid import UUID

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str
    role: str = "farmer"
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str | None = None
    language: str
    role: str
    model_config = {
        "from_attributes": True
    }



class RefreshTokenRequest(BaseModel):
    refresh_token :str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type:str
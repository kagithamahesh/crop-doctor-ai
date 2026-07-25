from pydantic import BaseModel, EmailStr

from uuid import UUID

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str | None = None
    language: str

    model_config = {
        "from_attributes": True
    }
class Token(BaseModel):
    access_token: str
    token_type: str 
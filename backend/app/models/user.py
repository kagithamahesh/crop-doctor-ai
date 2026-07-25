from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,Boolean
from app.models.basemodel import BaseModel
class User(BaseModel):
    __tablename__ = "users"
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )
    password_hash: Mapped[str] = mapped_column(
            String(255),
            nullable=False,
        )
    language: Mapped[str] = mapped_column(
        String(30),
        default="en",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

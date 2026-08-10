from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import String,Boolean,Enum
from app.models.basemodel import BaseModel
import enum

class UserRole(str, enum.Enum):
    farmer = "farmer"
    agronomist = "agronomist"
    admin = "admin"

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
    role: Mapped[UserRole] = mapped_column(
    Enum(UserRole),
    default=UserRole.farmer,
    )
    farms: Mapped[list["Farm"]] = relationship(
        "Farm",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

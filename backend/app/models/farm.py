from uuid import UUID

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basemodel import BaseModel


class Farm(BaseModel):
    __tablename__ = "farms"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    area: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="farms",
    )
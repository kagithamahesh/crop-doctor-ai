from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basemodel import BaseModel


class Crop(BaseModel):
    __tablename__ = "crops"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    variety: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    season: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    farm_id: Mapped[UUID] = mapped_column(
        ForeignKey("farms.id"),
        nullable=False,
    )

    farm: Mapped["Farm"] = relationship(
        "Farm",
        back_populates="crops",
    )
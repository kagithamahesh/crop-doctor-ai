from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.basemodel import BaseModel

class Farm(BaseModel):
    __tablename__="farms"

    name:Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(255))
    area: Mapped[float] = mapped_column(Float)

    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id")
    )

    owner = relationship("User")
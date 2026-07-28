from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.basemodel import BaseModel

class Crop(BaseModel):
    __tablename__="crops"
    name: Mapped[str] = mapped_column(String(100))
    variety: Mapped[str] = mapped_column(String(100))
    season: Mapped[str] = mapped_column(String(50))

    farm_id: Mapped[str] = mapped_column(
        ForeignKey("farms.id")
    )

    farm = relationship("Farm")
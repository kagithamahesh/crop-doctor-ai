from uuid import UUID

from sqlalchemy import String, ForeignKey, Float,Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from app.models.basemodel import BaseModel
from sqlalchemy.dialects.postgresql import JSONB

class DiseaseDetection(BaseModel):
    __tablename__ = "disease_detections"

    crop_id: Mapped[UUID] = mapped_column(
        ForeignKey("crops.id"),
        nullable=False,
    )

    image_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    disease_name: Mapped[str] = mapped_column(
        String(255),
        default="Unknown",
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    recommendation = mapped_column(Text, nullable=True)
    location = mapped_column(String(255), nullable=True)
    crop: Mapped["Crop"] = relationship(
        "Crop",
    )
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from pgvector.sqlalchemy import Vector

from app.models.basemodel import BaseModel


class DiseaseKnowledge(BaseModel):
    __tablename__ = "disease_knowledge"

    crop_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    disease_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    symptoms: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    treatment: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384)
    )
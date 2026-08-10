from sqlalchemy.orm import Session

from app.models.disease_detection import DiseaseDetection
from app.models.corp import Crop
from app.agents.diagnosis_graph import build_graph

diagnosis_graph = build_graph()


async def analyze_detection(db: Session, detection_id: str):
    detection = (
        db.query(DiseaseDetection)
        .filter(DiseaseDetection.id == detection_id)
        .first()
    )

    if not detection:
        raise ValueError("Detection not found")

    crop = (
        db.query(Crop)
        .filter(Crop.id == detection.crop_id)
        .first()
    )

    if not crop:
        raise ValueError("Crop not found")

    result = await diagnosis_graph.ainvoke(
        {
            "image_path": detection.image_path,
            "crop": crop.name,
            "location": "",
            "disease": detection.disease_name or "",
            "confidence": detection.confidence or 0.0,
        }
    )

    detection.disease_name = result.get("disease", detection.disease_name)
    detection.confidence = result.get("confidence", detection.confidence)
    detection.recommendation = str(result.get("recommendation", ""))

    db.commit()
    db.refresh(detection)

    return {
        "detection_id": str(detection.id),
        "crop": crop.name,
        "disease": detection.disease_name,
        "confidence": detection.confidence,
        "weather": result.get("weather"),
        "market": result.get("market"),
        "knowledge": result.get("knowledge"),
        "recommendation": result.get("recommendation"),
    }

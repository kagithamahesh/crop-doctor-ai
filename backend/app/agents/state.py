from typing import TypedDict


class DiagnosisState(TypedDict):
    image_path: str
    crop: str
    location: str
    disease: str
    confidence: float

    weather: dict
    market: dict
    knowledge: list

    recommendation: dict
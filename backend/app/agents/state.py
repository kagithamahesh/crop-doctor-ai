from typing import TypedDict


class DiagnosisState(TypedDict):
    crop: str
    disease: str
    confidence: float
    location: str
    disease: str

    weather: dict
    market: dict
    knowledge: list
    recommendation: dict

    recommendation: str
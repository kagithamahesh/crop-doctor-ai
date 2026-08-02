from typing import TypedDict

class DiagnosisState(TypedDict):
    crop: str
    location: str
    disease: str

    weather: dict
    market: dict
    knowledge: list

    recommendation: str
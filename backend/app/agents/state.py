from typing import TypedDict


class DiagnosisState(TypedDict, total=False):
    image_path: str
    crop: str
    disease: str
    confidence: float
    location: str

    weather: dict
    market: dict
    knowledge: list
    recommendation: dict

    route: str
    needs_human_review: bool
    additional_context_required: bool
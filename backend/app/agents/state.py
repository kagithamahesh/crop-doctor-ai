from typing import TypedDict, Optional


class DiagnosisState(TypedDict):
    image_path: str
    location: Optional[str]

    crop: Optional[str]
    disease: Optional[str]
    confidence: Optional[float]

    weather: Optional[dict]
    market: Optional[dict]
    knowledge: Optional[list]

    recommendation: Optional[dict]

    # supervisor fields
    route: Optional[str]
    priority: Optional[str]
    needs_human_review: Optional[bool]
    additional_context_required: Optional[bool]
    image_quality: Optional[str]
    severity: Optional[str]

    supervisor_decision: Optional[dict]

    execution_trace: Optional[list]

    weather_required: bool
    market_required: bool
    knowledge_required: bool
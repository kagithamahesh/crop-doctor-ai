from pathlib import Path

from app.agents.state import DiagnosisState


async def image_analysis_node(state: DiagnosisState) -> DiagnosisState:
    """
    Analyze uploaded crop image and predict disease.

    Input state:
    {
        "image_path": "uploads/abc.jpeg"
    }

    Output state:
    {
        "crop": "Tomato",
        "disease": "Late Blight",
        "confidence": 0.94
    }
    """

    image_path = Path(state["image_path"])

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Placeholder AI model
    crop = "Tomato"
    disease = "Late Blight"
    confidence = 0.94

    state["crop"] = crop
    state["disease"] = disease
    state["confidence"] = confidence

    return state
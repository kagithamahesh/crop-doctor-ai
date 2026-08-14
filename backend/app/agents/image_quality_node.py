from app.agents.state import DiagnosisState


async def image_quality_node(state: DiagnosisState) -> DiagnosisState:
    """
    Simulated image quality assessment.
    Later this can use a CNN or Vision Transformer.
    """

    confidence = state.get("confidence", 0)

    if confidence >= 0.90:
        state["image_quality"] = "excellent"

    elif confidence >= 0.75:
        state["image_quality"] = "good"

    elif confidence >= 0.60:
        state["image_quality"] = "acceptable"

    else:
        state["image_quality"] = "poor"

    return state
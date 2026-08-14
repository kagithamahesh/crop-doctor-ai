from app.agents.state import DiagnosisState

async def human_review_node(state: DiagnosisState) -> DiagnosisState:
    state["recommendation"] = {
        "status": "human_review_required",
        "message": (
            "The AI confidence is too low for an automatic diagnosis. "
            "Please upload another image with better lighting and focus."
        ),
    }

    return state
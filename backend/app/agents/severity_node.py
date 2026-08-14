from app.agents.state import DiagnosisState


HIGH_RISK = {
    "Late Blight",
    "Bacterial Wilt",
}


async def severity_node(state: DiagnosisState) -> DiagnosisState:
    disease = state.get("disease", "")

    if disease in HIGH_RISK:
        state["severity"] = "high"

    elif disease:
        state["severity"] = "medium"

    else:
        state["severity"] = "unknown"

    return state
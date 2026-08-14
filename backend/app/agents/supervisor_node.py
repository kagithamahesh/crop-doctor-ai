from app.agents.state import DiagnosisState


async def supervisor_node(state: DiagnosisState) -> DiagnosisState:
    confidence = state.get("confidence", 0)
    quality = state.get("image_quality", "unknown")
    severity = state.get("severity", "medium")
    location = state.get("location")

    decision = {
        "route": None,
        "priority": "normal",
        "reason": None,
        "requires_weather": True,
        "requires_market": True,
        "requires_rag": True,
    }

    if quality == "poor":
        decision["route"] = "human_review"
        decision["reason"] = "Image quality too poor"
        state["needs_human_review"] = True

    elif confidence < 0.60:
        decision["route"] = "human_review"
        decision["reason"] = "Low confidence diagnosis"
        state["needs_human_review"] = True

    else:
        decision["route"] = "parallel_data"
        state["needs_human_review"] = False

        if severity == "high":
            decision["priority"] = "urgent"
            decision["reason"] = "High-risk disease detected"

    if not location:
        state["additional_context_required"] = True
        decision["requires_weather"] = False

    state["route"] = decision["route"]
    state["priority"] = decision["priority"]
    state["supervisor_decision"] = decision

    trace = state.get("execution_trace") or []
    trace.append({
        "node": "supervisor",
        "decision": decision,
    })
    state["execution_trace"] = trace

    return state
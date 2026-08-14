from app.agents.state import DiagnosisState


async def supervisor_node(state: DiagnosisState) -> DiagnosisState:
     """
    Supervisor validates whether diagnosis can continue.

    Sets:
        state["route"]
        state["needs_human_review"]
    """
     confidence = state.get("confidence", 0)

     if confidence >= 0.90:
          state["route"] = "parallel_data"
          state["needs_human_review"] = False

     elif confidence >= 0.60:
           state["route"] = "parallel_data"
           state["needs_human_review"] = False
           state["additional_context_required"] = True
     else:
          state["route"] = "human_review"
          state["needs_human_review"] = True

     return state


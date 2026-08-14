from app.agents.state import DiagnosisState
from app.services.image_classifier import predict_disease

async def image_analysis_node(state: DiagnosisState) -> DiagnosisState:
    """
    Mock image analysis node.
    Later this will call your vision model.
    """
    image_path = state["image_path"]

    result = predict_disease(image_path)
    
    state["crop"] = result["crop"]
    state["disease"] = result["disease"]
    state["confidence"] = result["confidence"]
    


    return state
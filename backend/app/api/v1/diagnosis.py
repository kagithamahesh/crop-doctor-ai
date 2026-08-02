from fastapi import APIRouter

from app.agents.agronomist_graph import agronomist_agent

router = APIRouter()


@router.post("/analyze")
async def analyze(
    crop: str,
    location: str,
    disease: str,
):
    result = await agronomist_agent.ainvoke(
        {
            "crop": crop,
            "location": location,
            "disease": disease,
        }
    )

    return result
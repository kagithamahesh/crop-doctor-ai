import asyncio

from app.services.mcp_weather_client import fetch_weather
from app.services.mcp_market_client import get_market_prices
from app.database.session import SessionLocal
from app.services.vector_search import search_similar
from app.agents.state import DiagnosisState


async def parallel_data_node(state: DiagnosisState) -> DiagnosisState:
    """
    Fetch weather, market prices, and knowledge base results concurrently.

    Reads from state:  crop, disease, location
    Writes to state:   weather, market, knowledge
    """

    async def get_knowledge():
        db = SessionLocal()
        try:
            docs = search_similar(
                db,
                f"{state['crop']} {state['disease']}",
                limit=3,
            )
            return [
                {"disease": d.disease_name, "treatment": d.treatment}
                for d in docs
            ]
        finally:
            db.close()

    weather, market, knowledge = await asyncio.gather(
        fetch_weather(state.get("location", "")),
        get_market_prices(state["crop"]),
        get_knowledge(),
    )

    state["weather"] = weather
    state["market"] = market
    state["knowledge"] = knowledge

    return state

import asyncio
import time

from app.services.mcp_weather_client import fetch_weather
from app.services.mcp_market_client import get_market_prices
from app.database.session import SessionLocal
from app.services.vector_search import search_similar
from app.agents.state import DiagnosisState


async def parallel_data_node(state: DiagnosisState) -> DiagnosisState:
    """
    Fetch weather, market prices, and RAG knowledge concurrently.

    Reads:
        crop, disease, location

    Writes:
        weather, market, knowledge
    """

    start = time.perf_counter()

    async def get_knowledge():
        db = SessionLocal()
        try:
            docs = search_similar(
                db=db,
                query=f"{state['crop']} {state['disease']}",
                limit=3,
            )
            return [
                {
                    "title": d.title,
                    "content": d.chunk_text,
                    "source": d.source,
                }
                for d in docs
            ]
        finally:
            db.close()

    weather, market, knowledge = await asyncio.gather(
        fetch_weather(state.get("location", "")),
        get_market_prices(state["crop"]),
        get_knowledge(),
    )
    print(f"Parallel execution: {time.perf_counter() - start:.2f}s")
    state["weather"] = weather
    state["market"] = market
    state["knowledge"] = knowledge

    return state
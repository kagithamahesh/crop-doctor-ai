import asyncio

from app.services.mcp_weather_client import fetch_weather
from app.services.mcp_market_client import get_market_prices
from app.database.session import SessionLocal
from app.services.vector_search import search_similar

async def parallel_data_node(state: dict):
    db = SessionLocal()

    try:
            query = f"{state['crop']} {state['disease']}"

            weather_task = fetch_weather(state["location"])
            market_task = get_market_prices(state["crop"])

            async def knowledge_task():
                docs = search_similar(
                    db,
                    query,
                    limit=3,
                )

                return [
                    {
                        "disease": d.disease_name,
                        "treatment": d.treatment,
                    }
                    for d in docs
                ]

            weather, market, knowledge = await asyncio.gather(
                weather_task,
                market_task,
                knowledge_task(),
            )

            state["weather"] = weather
            state["market"] = market
            state["knowledge"] = knowledge

            return state

    finally:
            db.close()
from app.services.mcp_weather_client import fetch_weather


async def weather_node(state: dict):
    weather = await fetch_weather(
        state["location"]
    )

    state["weather"] = weather

    return state
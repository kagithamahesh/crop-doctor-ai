from app.services.mcp_market_client import get_market_prices


async def market_node(state: dict):
    market = await get_market_prices(
        state["crop"]
    )

    state["market"] = market

    return state
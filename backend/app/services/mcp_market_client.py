from fastmcp import Client

async def get_market_prices(crop: str):
    async with Client(
    "http://127.0.0.1:8002/mcp"
    ) as client:
        result = await client.call_tool(
        "get_market_price",
        {"crop": crop},
        )

    if hasattr(result, "data") and result.data:
        return result.data

    if hasattr(result, "structured_content") and result.structured_content:
        return result.structured_content

    return {"error": "No market data returned"}
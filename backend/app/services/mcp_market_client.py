import asyncio

from fastmcp import Client

async def fetch_market_price(crop: str):
    async with Client(
        "http://127.0.0.1:8002/mcp"
    ) as client:
        result = await client.call_tool(
            "get_market_price",
            {"crop": crop},
        )
        return result.data
    
# def get_market_prices(crop: str):
#     return asyncio.run(fetch_market_price(crop))
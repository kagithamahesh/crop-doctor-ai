import asyncio

from fastmcp import Client

async def fetch_weather(location:str):
    async with Client(
        "http://127.0.0.1:8001/mcp"
    ) as client:
         result = await client.call_tool(
            "get_weather",
            {"location": location},
        )

         return result.data



def get_weather(location:str):
         return asyncio.run(fetch_weather(location))
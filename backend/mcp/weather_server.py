from fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(location:str) -> dict:
    """
    Get weather information for a farm location.
    """
    return {
        "location": location,
        "temperature": 31,
        "humidity": 82,
        "rain_probability": 65,
        "wind_speed": 12,
        "recommendation": "Avoid spraying pesticide today.",
    }

if __name__ =="__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001,
    )
    
from fastmcp import FastMCP

mcp = FastMCP("Market Server")

MARKET_PRICES = {
    "tomato": {
        "price_per_quintal": 2200,
        "trend": "increasing",
        "recommended_action": "Hold for 3-5 days if possible."
    },
    "rice": {
        "price_per_quintal": 1850,
        "trend": "stable",
        "recommended_action": "Can sell immediately."
    },
    "cotton": {
        "price_per_quintal": 7100,
        "trend": "decreasing",
        "recommended_action": "Sell soon before further decline."
    }
}
@mcp.tool
def get_market_price(crop: str):
    crop = crop.lower()

    if crop not in MARKET_PRICES:
        return {
            "error": f"No market data for {crop}"
        }

    return MARKET_PRICES[crop]

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8002,
    )
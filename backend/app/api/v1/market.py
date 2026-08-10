from fastapi import APIRouter
from app.services.mcp_market_client import get_market_prices

router = APIRouter()

@router.get("/{crop}")
async def market(crop: str):
    return await get_market_prices(crop)
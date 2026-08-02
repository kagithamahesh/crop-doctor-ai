from fastapi import APIRouter
from app.services.mcp_market_client import fetch_market_price

router = APIRouter()

@router.get("/{crop}")
async def market(crop: str):
    return await fetch_market_price(crop)
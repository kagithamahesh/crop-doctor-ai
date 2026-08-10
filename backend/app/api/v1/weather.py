from fastapi import APIRouter

from app.services.mcp_weather_client import get_weather

router = APIRouter()


@router.get("/{location}")
def weather(location: str):
    return get_weather(location)
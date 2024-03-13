from fastapi import APIRouter, HTTPException

from app.openweather.controller import get_weather, get_weather_asnyc
from app.openweather.schema import OpenweatherData

router = APIRouter()


@router.get(
    "/get_openweather", response_model=OpenweatherData, response_model_exclude_none=True
)
async def get_openweather(lat: str, long: str) -> OpenweatherData | None:
    print("\n")
    x = get_weather(lat, long)
    if x is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return x


@router.get(
    "/async_get_openweather",
    response_model=OpenweatherData,
    response_model_exclude_none=True,
)
async def async_get_openweather(lat: str, long: str) -> OpenweatherData | None:
    a = await get_weather_asnyc(lat, long)
    if a is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return a

from fastapi import APIRouter

from app.openweather.controller import get_weather, get_weather_asnyc
from app.openweather.models.sqlite import get_from_db
from app.openweather.schema import OpenweatherData

router = APIRouter()


@router.get("/get_openweather")
async def get_openweather(lat: str, long: str) -> OpenweatherData | None:
	print("\n")
	x = get_weather(lat, long)
	if x is None:
		return None
	return x


@router.get("/async_get_openweather")
async def async_get_openweather(lat: str, long: str) -> OpenweatherData | None:
	a = await get_weather_asnyc(lat, long)
	if a is None:
		return None
	return a

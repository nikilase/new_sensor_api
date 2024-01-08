from fastapi import APIRouter

from app.openweather.controller import get_weather
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


@router.get("/async_get")
async def get_async_get(lat: str, long: str) -> OpenweatherData | None:
	a = await get_from_db(lat, long)
	if a is None:
		return None
	return a.json_data

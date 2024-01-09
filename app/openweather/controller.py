import decimal
from datetime import datetime, timezone, timedelta
from decimal import Decimal

import requests

from app.openweather.models.sqlite import OWWeather, get_from_sqlite, get_from_db
from app.conf.config import openweathermap as ow
from app.openweather.schema import OpenweatherData, openweather_data_from_json


def get_from_openweather_api(lat: Decimal, long: Decimal):
	appid = ow["api_key"]
	base_url = ow["base_url"]
	only_allowed_coords = ow["only_allowed_coords"]
	allowed_coords = ow["allowed_coords"]

	lat, long = round_coord(lat, long)

	if only_allowed_coords:
		found = False
		for coord in allowed_coords:
			a_lat, a_long = round_coord(coord["lat"], coord["long"])
			if lat == a_lat and long == a_long:
				found = True
				break
		if not found:
			return

	lat = f"{lat:.7f}"
	long = f"{long:.7f}"
	req_url = base_url + f"?lat={lat}&lon={long}&appid={appid}&units=metric&lang=de"

	last_update = get_from_sqlite(lat, long)
	if last_update is None or datetime.now(tz=timezone.utc) - last_update.last_updated_utc > timedelta(minutes=5):
		# Make request
		req = requests.get(req_url)
		data = req.json()

		upd_time = datetime.now(tz=timezone.utc)
		ow_data = openweather_data_from_json(data)
		# Create OWWeather Object and update SQLite DB with it
		weather = OWWeather(lat=lat, long=long, json_data=ow_data, last_updated_utc=upd_time)
		if last_update is None:
			weather.insert_into_sqlite()
		else:
			weather.update_sqlite()
	else:
		print("Data already new enough")


def parse_coord(lat: str, long: str) -> tuple | None:
	try:
		lat = Decimal(lat)
		long = Decimal(long)
	except decimal.InvalidOperation:
		return None
	lat, long = round_coord(lat, long)
	if -90 <= lat <= 90 and -180 <= long <= 180:
		return lat, long
	else:
		return None


def round_coord(lat: Decimal, long: Decimal):
	lat = round(lat, 7)
	long = round(long, 7)
	return lat, long


def get_weather(lat: str, long: str) -> OpenweatherData | None:
	coord = parse_coord(lat, long)
	if coord is None:
		return None
	lat, long = coord
	# First Update the local db if it is outdated
	get_from_openweather_api(lat, long)

	# Then get the data
	x = get_from_sqlite(str(lat), str(long))
	if x is None:
		return None
	return x.json_data


async def get_weather_asnyc(lat: str, long: str) -> OpenweatherData | None:
	# First Update the local db if it is outdated
	x = await get_from_openweather_api_async()
	if x is not None:
		return x.json_data

	# Then get the data
	x = await get_from_db(lat, long)
	if x is None:
		return None
	return x.json_data


async def get_from_openweather_api_async() -> OWWeather | None:
	appid = ow["api_key"]
	lat = ow["lat"]
	long = ow["long"]
	base_url = ow["base_url"]

	req_url = base_url + f"?lat={lat}&lon={long}&appid={appid}&units=metric&lang=de"

	last_update = get_from_sqlite(lat, long).last_updated_utc
	if datetime.now(tz=timezone.utc) - last_update > timedelta(minutes=5):
		# Make request
		req = requests.get(req_url)
		data = req.json()

		upd_time = datetime.now(tz=timezone.utc)
		ow_data = openweather_data_from_json(data)
		# Create OWWeather Object and update SQLite DB with it
		weather = OWWeather(lat=lat, long=long, json_data=ow_data, last_updated_utc=upd_time)

		weather.update_sqlite()
		return weather
	else:
		print("Data already new enough")
		return None

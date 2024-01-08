from datetime import datetime, timezone, timedelta
import json
import requests

from app.openweather.models.sqlite import OWWeather, get_from_sqlite
from app.conf.config import openweathermap as ow
from app.openweather.schema import OpenweatherData, openweather_data_from_json


def get_from_openweather_api():
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
		data_string = json.dumps(data, indent=4, sort_keys=True)
		upd_time = datetime.now(tz=timezone.utc)
		ow_data = openweather_data_from_json(data)
		# Create OWWeather Object and update SQLite DB with it
		weather = OWWeather(lat=lat, long=long, json_data=ow_data, last_updated_utc=upd_time)

		weather.update_sqlite()
	else:
		print("Data already new enough")


#Todo: Create openweather router:
#	For getting openweatherdata, first check local db for version that is more recent than 5 minutes ago
#	If no recent file, get from OpenweatherAPI and save in local db
#	Finally deliver to client from local db

def get_weather(lat: str, long: str) -> OpenweatherData | None:
	# First Update the local db if it is outdated
	get_from_openweather_api()

	# Then get the data
	x = get_from_sqlite(lat, long)
	if x is None:
		return None
	return x.json_data

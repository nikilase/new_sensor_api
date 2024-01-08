import json
from datetime import datetime
import sqlite3
import os.path
import time
import aiosqlite
from pydantic import BaseModel
from app.openweather.schema import OpenweatherData, openweather_data_from_json


class OWWeather(BaseModel):
	lat: str
	long: str
	json_data: OpenweatherData
	last_updated_utc: datetime

	def get_localtime(self):
		epoch = time.mktime(self.last_updated_utc.timetuple())
		offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
		return self.last_updated_utc + offset

	def open_weater_to_str(self):
		return json.dumps(self.json_data.__dict__)

	def update_sqlite(self):
		conn = sqlite3.connect(db_path())
		c = conn.cursor()
		print(self.last_updated_utc)
		print(self.lat)
		print(self.long)
		query = "update openweather set last_update_utc = ?, weather_data = ? where lat=? and long=?"
		c.execute(query, (self.last_updated_utc, self.open_weater_to_str(), self.lat, self.long))
		conn.commit()
		c.close()
		conn.close()


def db_path() -> str:
	base_dir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(base_dir, "openweather.db")


def get_from_sqlite(lat: str, long: str) -> OWWeather | None:
	conn = sqlite3.connect(db_path())
	c = conn.cursor()

	query = "select last_update_utc, weather_data from openweather where lat=? and long=?"
	c.execute(query, (lat, long))
	res = c.fetchone()

	c.close()
	conn.close()

	if res is None:
		return None
	last_update, weather_data = res
	ow = openweather_data_from_json(json.loads(weather_data))
	return OWWeather(lat=lat, long=long, json_data=ow, last_updated_utc=last_update)


async def get_from_db(lat: str, long: str) -> OWWeather | None:
	async with aiosqlite.connect(db_path()) as db:
		query = "select last_update_utc, weather_data from openweather where lat=? and long=?"
		async with db.execute(query, (lat, long)) as cursor:
			res = await cursor.fetchone()

	if res is None:
		return None

	last_update, weather_data = res
	ow = openweather_data_from_json(json.loads(weather_data))

	return OWWeather(lat=lat, long=long, json_data=ow, last_updated_utc=last_update)


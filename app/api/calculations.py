import math

from app.conf import config
from app.conf.config import sensors
from app.api.models.influx import write_line
from app.helpers.my_logger import log_info, log_warn, log_error
from app.conf.config import influxdb


def get_height(chip_id: str):
	heights = [sensor["elevation"] for sensor in sensors if sensor["sensor"] == chip_id]
	if heights:
		return heights[0]
	else:
		return None


def normalize_pressure(pressure: float, height: float, temperature: float):
	p = 1 - ((0.0065 * height) / (temperature + 0.0065 * height + 273.15))
	p = pressure * math.pow(p, -5.257)
	return round(p * 100) / 100


def str_to_float(value_str: str) -> float | None:
	try:
		value_float = float(value_str)
	except Exception as e:
		print(e)
		return None
	return value_float


def str_to_float_validate(value_str: str, min_val: float, max_val: float, value_type: str = "value") -> float | None:
	try:
		value_float = float(value_str)
	except Exception as e:
		print(e)
		return None
	if value_float < min_val or value_float > max_val or math.isnan(value_float):
		log_warn("POST /Send", f"Inconsistent {value_type} reading of {value_float}! Discarding value!")
		return None
	return value_float


def extract_and_send_sensor_data(sensor_data_json: dict):
	# Important variables for sensor data and Influx string
	chip_id: str = ""
	sensor_data_values: list = [dict]
	tags: dict = {}
	fields: dict = {}
	fields_water: dict = {}
	measurement: str = config.influxdb["msrmt"]
	measurement_water: str = "water"

	# Extract Chip ID and sensor data from json
	for k, v in sensor_data_json.items():
		match k:
			case "esp8266id":
				chip_id = f"esp{v}"
			case "sensorId":
				chip_id = f"gen_{v}"
			case "id":
				chip_id = v
			case "sensordatavalues":
				sensor_data_values = v
			case "software_version":
				pass
			case _:
				log_warn("POST /Send", f"Found new element in json with key {k} and value {v}")

	# Test if we have Chip ID and sensor data
	if chip_id == "":
		log_error("POST /Send", f"Received no chip ID!")
		return 1
	tags.update({"sensorID": chip_id})

	if not sensor_data_values:
		log_error("POST /Send", f"Received no valid sensor data value array!\n"
								f"Instead received {sensor_data_values}")
		return 2

	# Try to retrieve height of the sensor via Chip ID
	height: float | None = get_height(chip_id)
	pressure: float | None = None
	temperature: float | None = None

	# Go through all sensor data
	for elem in sensor_data_values:
		val = elem["value"]
		typ = elem["value_type"]
		match typ:
			case "BME280_temperature":
				temperature = str_to_float_validate(val, -50, 50, "temperature")
				if temperature is not None:
					fields.update({"temperature": temperature})

			case "BME280_pressure":
				pressure = str_to_float_validate(val, 85000, 115000, "pressure")
				if pressure is not None:
					fields.update({"pressure": pressure})

			case "BME280_humidity":
				humidity = str_to_float_validate(val, 0, 100, "humidity")
				if humidity is not None:
					fields.update({"humidity": humidity})

			case "DS18B20_temperature":
				ds18b20 = str_to_float_validate(val, -50, 50, "ds18b20")
				if ds18b20 is not None:
					fields.update({"temperature_ds18b20": ds18b20})

			case "samples" | "min_micro" | "max_micro" | "interval":
				pass

			case "signal":
				signal = str_to_float(val)
				if signal is not None:
					fields.update({"signal": signal})

			case "miflora_temperature":
				miflora_temperature = str_to_float_validate(val, -50, 50, "miflora_temperature")
				if miflora_temperature is not None:
					fields.update({"flora_temperature": miflora_temperature})
			case "miflora_moisture":
				fields.update({"flora_moisture": val})
			case "miflora_ec":
				fields.update({"flora_ec": val})
			case "miflora_lumen":
				fields.update({"flora_lumen": val})
			case "miflora_battery":
				fields.update({"flora_battery": val})

			case "water_height_percent":
				fields_water.update({"percent": val})
			case "water_height_volume":
				fields_water.update({"volume": val})
			case "water_height_height":
				fields_water.update({"height": val})
			case "water_height_voltage":
				fields_water.update({"voltage": val})
			case "water_height_location":
				tags.update({"location": val})

			case _:
				log_warn("POST /Send", f"Received new sensor type {typ} with value {val}")

	# Now calculate the normalized ASL pressure
	if None not in [height, pressure, temperature]:
		normal_pressure = normalize_pressure(pressure, height, temperature)
		fields.update({"pressure_ASL": normal_pressure})

	# Finally write the influx line if we have at least one tag and one field
	if tags and fields:
		ret = 0
		log_info(f"{tags} {fields} {measurement}")
		if not write_line(tags, fields, measurement, influxdb):
			log_error("POST /Send", "Could not write data to Influx.")
			ret = 3
		if ret == 3:
			return 3

	# Finally write the influx line if we have at least one tag and one field
	elif tags and fields_water:
		ret = 0
		tags.pop("sensorID")
		tags.update({"id": chip_id})
		if not write_line(tags, fields_water, measurement_water, influxdb):
			log_error("POST /Send", "Could not write data to Influx.")
			ret = 3
		if ret == 3:
			return 3
	else:
		log_error("POST /Send", "No data to write")
		return 3
	return 0


def extract_and_send_stat_data(sensor_stat_json: dict):
	# Important variables for sensor data and Influx string
	chip_id: str = ""
	sensor_type: str = ""
	tags: dict = {}
	fields: dict = {}

	# Extract Chip ID and sensor data from json
	for k, v in sensor_stat_json.items():
		match k:
			case "esp8266id":
				chip_id = f"esp{v}"
			case "sensorId":
				chip_id = f"gen_{v}"
			case "type":
				sensor_type = v
			case "software_version":
				pass
			case _:
				log_warn("POST /post_stat", f"Found new element in json with key {k} and value {v}")

	# Test if we have Chip ID and sensor data
	if chip_id == "":
		log_error("POST /post_stat", f"Received no chip ID!")
		return 1
	tags.update({"sensorID": chip_id})

	# Go through data
	if sensor_type == "restart":
		fields.update({"restart": 1})
	elif sensor_type == "ping":
		fields.update({"ping": 1})
	else:
		log_error("POST /post_stat", f"Received no valid message type!\n"
									 f"Instead received {sensor_type}")
		return 2

	# Finally write the influx line if we have at least one tag and one field
	if tags and fields:
		ret = 0
		if not write_line(tags, fields, "", influxdb):
			ret = 3
		if ret == 3:
			log_error("POST /post_stat", "Could not write data to Influx.")
			return 3
		else:
			return 0
	log_error("POST /post_stat", "No data found")
	return 3

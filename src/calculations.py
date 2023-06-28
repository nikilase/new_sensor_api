import math

from conf import config
from conf.config import sensors
from src.influx import write_line
from src.my_logger import log_info, log_warn, log_error
def get_height(chip_id: str):
	heights = [sensor["elevation"] for sensor in sensors if sensor["sensor"]==chip_id]
	if heights:
		return heights[0]
	else:
		return None

def normalize_pressure(pressure: float, height: float, temperature: float):
	p = 1 - ((0.0065 * height) / (temperature + 0.0065 * height + 273.15))
	p = pressure * math.pow(p, -5.257)
	return round(p*100) / 100

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
				try:
					temperature = float(val)
				except Exception as e:
					print(e)
					temperature = None
					continue
				if temperature < -50.0 or temperature > 50.0:
					log_warn("POST /Send", f"Inconsistent temperature reading of {temperature}! Discarding value!")
					temperature = None
					continue
				fields.update({"temperature": temperature})

			case "BME280_pressure":
				try:
					pressure = float(val)
				except Exception as e:
					print(e)
					pressure = None
					continue
				if pressure < 85000 or pressure > 115000:
					log_warn("POST /Send", f"Inconsistent pressure reading of {pressure}! Discarding value!")
					pressure = None
					continue
				fields.update({"pressure": pressure})

			case "BME280_humidity":
				try:
					humidity = float(val)
				except Exception as e:
					print(e)
					humidity = None
					continue
				if humidity < 0 or humidity > 100:
					log_warn("POST /Send", f"Inconsistent humidity reading of {humidity}! Discarding value!")
					humidity = None
					continue
				fields.update({"humidity": humidity})

			case "DS18B20_temperature":
				try:
					ds18b20 = float(val)
				except Exception as e:
					print(e)
					ds18b20 = None
					continue
				if ds18b20 < -50.0 or ds18b20 > 50.0:
					log_warn("POST /Send", f"Inconsistent ds18b20 temperature reading of {ds18b20}! Discarding value!")
					ds18b20 = None
					continue
				fields.update({"temperature_ds18b20": ds18b20})

			case "samples" | "min_micro" | "max_micro" | "interval":
				pass

			case "signal":
				try:
					signal = float(val)
				except Exception as e:
					print(e)
					continue
				fields.update({"signal": signal})

			case "miflora_temperature":
				fields.update({"flora_temperature": float(val)})
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
		if not write_line(tags, fields, measurement):
			log_error("POST /Send", "Could not write data to Influx.")
			return 3

	# Finally write the influx line if we have at least one tag and one field
	elif tags and fields_water:
		if not write_line(tags, fields_water, measurement_water):
			log_error("POST /Send", "Could not write data to Influx.")
			return 3
	else:
		log_error("POST /Send", "No data to write")
		return 3
	return 0

def extract_and_send_stat_data(sensor_stat_json: dict):
	# Important variables for sensor data and Influx string
	chip_id: str = ""
	type: str = ""
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
				type = v
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
	if type == "restart":
		fields.update({"restart": 1})
	elif type == "ping":
		fields.update({"ping": 1})
	else:
		log_error("POST /post_stat", f"Received no valid message type!\n"
									 f"Instead received {type}")
		return 2

	# Finally write the influx line if we have at least one tag and one field
	if tags and fields:
		if write_line(tags, fields):
			return 0
	log_error("POST /post_stat", "Could not write data to Influx.")
	return 3
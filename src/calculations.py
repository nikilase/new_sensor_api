import math
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

	# Extract Chip ID and sensor data from json
	for k, v in sensor_data_json.items():
		match k:
			case "esp8266id":
				chip_id = f"esp{v}"
			case "sensorId":
				chip_id = f"gen{v}"
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
					continue
				if -50 < temperature > 50:
					log_warn("POST /Send", f"Inconsistent temperature reading of {temperature}! Discarding value!")
					continue
				fields.update({"temperature": temperature})

			case "BME280_pressure":
				try:
					pressure = float(val)
				except Exception as e:
					print(e)
					continue
				fields.update({"pressure": pressure})

			case "BME280_humidity":
				try:
					humidity = float(val)
				except Exception as e:
					print(e)
					continue
				fields.update({"humidity": humidity})

			case "DS18B20_temperature":
				try:
					ds18b20 = float(val)
				except Exception as e:
					print(e)
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

			case _:
				log_warn("POST /Send", f"Received new sensor type {typ} with value {val}")

	# Now calculate the normalized ASL pressure
	if None not in [height, pressure, temperature]:
		normal_pressure = normalize_pressure(pressure, height, temperature)
		fields.update({"pressure_ASL": normal_pressure})

	# Finally write the influx line if we have at least one tag and one field
	if tags and fields:
		if write_line(tags, fields):
			return 0
	log_error("POST /Send", "Could not write data to Influx.")
	return 3
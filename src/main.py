from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import logging
from src.my_logger import log_info, log_warn, log_error
from src.supplementary import get_height, normalize_pressure
from src.influx import write_line, get_latest_data

app = FastAPI(
	title="API for former Sensorwebsite",
	description="Ability to send well structured sensor data from luftdaten.info sensor node to my influx database. "
				"Only BME280 and DS18B20 sensor values currently supported. "
				"This is a private API/Mini Website made by Niklas Eichenberg",
	contact={
        "name": "nikilase",
        "url": "https://github.com/nikilase",
    },
	version="1.0.0",
)
logger = logging.getLogger("uvicorn.error")
favicon_path = '../images/favicon.ico'
templates = Jinja2Templates(directory="templates/")


#ToDo: Sample Arduino program for sending stuff via HTTP POST JSON: https://www.techcoil.com/blog/how-to-post-json-data-to-a-http-server-endpoint-from-your-esp32-development-board-with-arduinojson/
#ToDo: In HTML, create a button to enable auto refresh and check for that in the setInterval function

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
	print("\n")
	return FileResponse(favicon_path)

@app.get("/")
async def home(request: Request):
	print("\n")
	return templates.TemplateResponse('root.html', context={'request': request})

@app.get("/get_latest")
async def get_latest():
	print("\n")
	x = get_latest_data()
	return x

@app.get("/hello/{name}")
async def say_hello(name: str):
	print("\n")
	log_info(f"GET /hello/{name}")
	return {"message": f"Hello {name}"}

@app.post("/Send")
async def send_sensor_data(req: Request):
	##################################################
	# Retrieve Request and JSON data
	##################################################
	print("\n")
	log_info("POST /Send", "Received Request")
	try:
		sensor_data_json: dict = await req.json()
	except Exception as err:
		body = await req.body()
		log_error("POST /Send", f"Error: {err} \n"
								f"\tInvalid JSON body: {body}")
		return {"message": "Failed to receive Sensor Data JSON Object!"}

	log_info("POST /Send", f"Received Data: \n"
						   f"{sensor_data_json}")

	##################################################
	# Go through the JSON and retrieve our values
	##################################################

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
		return {"message": "Error: No Chip ID was sent!"}
	tags.update({"sensorID": chip_id})

	if not sensor_data_values:
		log_error("POST /Send", f"Received no valid sensor data value array!\n"
								f"Instead received {sensor_data_values}")
		return {"message": "Error: No sensor data was sent!"}

	# Try to retrieve height of the sensor via Chip ID
	height: float|None = get_height(chip_id)
	pressure: float|None = None
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
			return {"message": "Successfully received and written Sensor Data"}
	log_error("POST /Send", "Could not write data to Influx.")
	return {"message": "Did not write the data to influx"}

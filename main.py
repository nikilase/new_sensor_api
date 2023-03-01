# External modules
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

# Internal modules
from src.my_logger import log_info, log_warn, log_error
from src.calculations import  extract_and_send_sensor_data
from src.influx import get_latest_data, write_line


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



favicon_path = "images/favicon.ico"
templates = Jinja2Templates(directory="templates/")


#ToDo: Sample Arduino program for sending stuff via HTTP POST JSON: https://www.techcoil.com/blog/how-to-post-json-data-to-a-http-server-endpoint-from-your-esp32-development-board-with-arduinojson/


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

#ToDo: Maybe merge /ping and /restart to /post_stat
@app.get("/ping/{chip_type}/{chip_id}")
async def ping(chip_type: str, chip_id: str):
	print("\n")
	log_info(f"GET /ping/{chip_type}/{chip_id}")
	match chip_type:
		case "esp8266id":
			chip_id = f"esp{chip_id}"
		case"sensorId":
			chip_id = f"gen_{chip_id}"

	tags = {"sensorID": chip_id}
	fields = {"ping": 1}
	write_line(tags, fields)
	return {"message": f"Received Ping"}

@app.get("/restart/{chip_type}/{chip_id}")
async def restart(chip_type: str, chip_id: str):
	print("\n")
	log_info(f"GET /restart/{chip_type}/{chip_id}")
	match chip_type:
		case "esp8266id":
			chip_id = f"esp{chip_id}"
		case"sensorId":
			chip_id = f"gen_{chip_id}"

	tags = {"sensorID": chip_id}
	fields = {"restart": 1}
	write_line(tags, fields)
	return {"message": f"Received Restart"}

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
	else:
		log_info("POST /Send", f"Received Data: \n"
							   f"{sensor_data_json}")

		failed: int = extract_and_send_sensor_data(sensor_data_json)
		if not failed:
			return {"message": "Successfully received and sent Sensor Data to Influx DB!"}
		else:
			match failed:
				case 1:
					return {"message": "Error: No Chip ID was sent!"}
				case 2:
					return {"message": "Error: No sensor data was sent!"}
				case 3:
					return {"message": "Could not write the data to Influx DB!"}
				case _:
					return {"message": "Unknown error occurred. Could not extract data or send to Influx DB!"}